package main

import (
	"bytes"
	cryptorand "crypto/rand"
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"crypto/x509/pkix"
	"encoding/base64"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"math/big"
	"net"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"
	"unicode/utf8"
)

type Config struct {
	ListenAddr   string
	TargetAddr   string
	CertFile     string
	KeyFile      string
	LogDir       string
	ForwardHTTPS bool
	ForwardPort  string
}

type RequestLog struct {
	RequestID       string            `json:"request_id"`
	Timestamp       time.Time         `json:"timestamp"`
	Method          string            `json:"method"`
	URL             string            `json:"url"`
	Path            string            `json:"path"`
	Query           string            `json:"query,omitempty"`
	Proto           string            `json:"proto"`
	Host            string            `json:"host"`
	Headers         map[string]string `json:"headers"`
	Body            string            `json:"body,omitempty"`
	BodyEncoding    string            `json:"body_encoding,omitempty"`
	BodyTruncated   bool              `json:"body_truncated,omitempty"`
	ClientIP        string            `json:"client_ip"`
	DestinationIP   string            `json:"destination_ip,omitempty"`
	DestinationPort string            `json:"destination_port,omitempty"`
	UserAgent       string            `json:"user_agent,omitempty"`
	ForwardedTo     string            `json:"forwarded_to"`
	Classification  string            `json:"classification"`
	ExperimentGroup string            `json:"experiment_group"`
	TLS             *TLSInfo          `json:"tls,omitempty"`
}

type TLSInfo struct {
	Version            string `json:"version"`
	CipherSuite        string `json:"cipher_suite"`
	ServerName         string `json:"server_name,omitempty"`
	NegotiatedProtocol string `json:"negotiated_protocol,omitempty"`
}

type ResponseLog struct {
	Timestamp     time.Time         `json:"timestamp"`
	StatusCode    int               `json:"status_code"`
	Status        string            `json:"status"`
	Headers       map[string]string `json:"headers"`
	Body          string            `json:"body,omitempty"`
	BodyEncoding  string            `json:"body_encoding,omitempty"`
	BodyTruncated bool              `json:"body_truncated,omitempty"`
	DurationMs    int64             `json:"duration_ms"`
}

var (
	logMutex sync.Mutex
)

// certRotator holds the active TLS certificate and swaps it on a timer.
// Every rotation generates a brand-new RSA key pair with a randomised serial number and validity window
type certRotator struct {
	mu   sync.RWMutex
	cert *tls.Certificate
}

// newCertRotator generates an initial certificate and, if interval > 0,
// starts a background goroutine that rotates it on that time
func newCertRotator(interval time.Duration) (*certRotator, error) {
	cr := &certRotator{}
	if err := cr.rotate(); err != nil {
		return nil, fmt.Errorf("initial cert generation: %w", err)
	}
	if interval > 0 {
		go func() {
			ticker := time.NewTicker(interval)
			defer ticker.Stop()
			for range ticker.C {
				if err := cr.rotate(); err != nil {
					log.Printf("⚠️ cert rotation failed: %v", err)
				} else {
					log.Printf("🔄 TLS certificate rotated")
				}
			}
		}()
	}
	return cr, nil
}

func (cr *certRotator) rotate() error {
	cert, err := generateSelfSignedCert()
	if err != nil {
		return err
	}
	// Lock to prevent mid update readings
	cr.mu.Lock()
	cr.cert = cert
	cr.mu.Unlock()
	return nil
}

// TLS handshake, so the active cert is always served without a restart.
func (cr *certRotator) getCertificate(_ *tls.ClientHelloInfo) (*tls.Certificate, error) {
	cr.mu.RLock()
	defer cr.mu.RUnlock()
	return cr.cert, nil
}

// generateSelfSignedCert creates an RSA-2048 self-signed certificate with a
// random serial, random validity window, and a randomly chosen common name.
func generateSelfSignedCert() (*tls.Certificate, error) {
	key, err := rsa.GenerateKey(cryptorand.Reader, 2048)
	if err != nil {
		return nil, fmt.Errorf("generate key: %w", err)
	}

	serial, err := cryptorand.Int(cryptorand.Reader, new(big.Int).Lsh(big.NewInt(1), 128))
	if err != nil {
		return nil, fmt.Errorf("generate serial: %w", err)
	}

	// Pretend the cert was issued 1–7 days ago and expires 14–45 days from
	// issuance so every rotation produces a distinct fingerprint.
	notBefore := time.Now().Add(-time.Duration(randN(7)+1) * 24 * time.Hour)
	notAfter := notBefore.Add(time.Duration(randN(32)+14) * 24 * time.Hour)

	tmpl := &x509.Certificate{
		SerialNumber:          serial,
		Subject:               pkix.Name{CommonName: randomCN()},
		NotBefore:             notBefore,
		NotAfter:              notAfter,
		KeyUsage:              x509.KeyUsageKeyEncipherment | x509.KeyUsageDigitalSignature,
		ExtKeyUsage:           []x509.ExtKeyUsage{x509.ExtKeyUsageServerAuth},
		BasicConstraintsValid: true,
	}

	der, err := x509.CreateCertificate(cryptorand.Reader, tmpl, tmpl, &key.PublicKey, key)
	if err != nil {
		return nil, fmt.Errorf("create certificate: %w", err)
	}

	return &tls.Certificate{
		Certificate: [][]byte{der},
		PrivateKey:  key,
	}, nil
}

// randN returns a cryptographically random integer in [0, n).
func randN(n int) int {
	b, _ := cryptorand.Int(cryptorand.Reader, big.NewInt(int64(n)))
	return int(b.Int64())
}

// randomCN picks a plausible-looking common name so the certificate subject does not look like a honeypot.
// name pattern taken from real certs through shodan.io and modified.
var commonNames = []string{
	"psgfmap01.internal.bones.net",
	"svc-portal.internal",
	"sys-admin.internal",
	"rapid.management.internal",
	"portin-production-c.internal.mathspeech.com",
	"fge-integration-test.internal.coralset.com",
}

func randomCN() string {
	return commonNames[randN(len(commonNames))]
}

func main() {
	// Command line flags
	listenAddr := flag.String("listen", ":8443", "Address to listen on (use :443 in production, :8443 for unprivileged dev)")
	targetAddr := flag.String("target", "localhost:8080", "Target honeypot address (the proxy forwards plaintext to this backend)")
	certFile := flag.String("cert", "testdata/cert.pem", "TLS certificate file (ignored when --rotate-cert-interval > 0)")
	keyFile := flag.String("key", "testdata/key.pem", "TLS private key file (ignored when --rotate-cert-interval > 0)")
	logDir := flag.String("log-dir", "./logs", "Directory to store logs")
	forwardHTTPS := flag.Bool("forward-https", false, "Forward to honeypot using HTTPS (default HTTP)")
	verbose := flag.Bool("verbose", false, "Log every request/response to console")
	rotateCertInterval := flag.Duration("rotate-cert-interval", 0, "How often to rotate the TLS certificate (e.g. 24h). 0 disables rotation and uses --cert/--key files instead.")
	flag.Parse()

	// Create log directory
	if err := os.MkdirAll(*logDir, 0755); err != nil {
		log.Fatalf("Failed to create log directory: %v", err)
	}

	// Configure target
	targetScheme := "http"
	if *forwardHTTPS {
		targetScheme = "https"
	}
	targetURL := fmt.Sprintf("%s://%s", targetScheme, *targetAddr)

	// Create reverse proxy
	proxy := &HoneypotProxy{
		targetURL: targetURL,
		logDir:    *logDir,
		verbose:   *verbose,
		transport: createTransport(*forwardHTTPS),
	}

	// Build TLS config — either rotating certs or static files.
	tlsCfg := createTLSConfig()
	if *rotateCertInterval > 0 {
		cr, err := newCertRotator(*rotateCertInterval)
		if err != nil {
			log.Fatalf("cert rotator: %v", err)
		}
		tlsCfg.GetCertificate = cr.getCertificate
		log.Printf("🔄 Certificate rotation enabled (interval: %s)", *rotateCertInterval)
	}

	// Setup HTTP server
	server := &http.Server{
		Addr:         *listenAddr,
		Handler:      proxy,
		TLSConfig:    tlsCfg,
		ReadTimeout:  30 * time.Second,
		WriteTimeout: 30 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	log.Printf("🚀 Starting honeypot proxy on %s", *listenAddr)
	log.Printf("🎯 Forwarding to %s", targetURL)
	log.Printf("📝 Logging to %s", *logDir)

	// Start server — use a manual TLS listener when rotating (no cert files
	// needed), or the standard ListenAndServeTLS with static files otherwise.
	if *rotateCertInterval > 0 {
		ln, err := net.Listen("tcp", *listenAddr)
		if err != nil {
			log.Fatalf("listen: %v", err)
		}
		if err := server.Serve(tls.NewListener(ln, tlsCfg)); err != nil {
			log.Fatalf("Failed to start server: %v", err)
		}
	} else {
		if err := server.ListenAndServeTLS(*certFile, *keyFile); err != nil {
			log.Fatalf("Failed to start server: %v", err)
		}
	}
}

type HoneypotProxy struct {
	targetURL string
	logDir    string
	verbose   bool
	transport http.RoundTripper
}

func createTransport(forwardHTTPS bool) http.RoundTripper {
	transport := &http.Transport{
		MaxIdleConns:        100,
		MaxIdleConnsPerHost: 10,
		IdleConnTimeout:     90 * time.Second,
		DisableCompression:  false,
	}

	if forwardHTTPS {
		// For HTTPS forwarding, skip cert verification (it's a honeypot)
		transport.TLSClientConfig = &tls.Config{
			InsecureSkipVerify: true,
		}
	}

	return transport
}

func createTLSConfig() *tls.Config {
	return &tls.Config{
		MinVersion:   tls.VersionTLS12,
		MaxVersion:   tls.VersionTLS13,
		Certificates: nil, // Will be loaded from files
		CurvePreferences: []tls.CurveID{
			tls.CurveP256,
			tls.X25519,
		},
		PreferServerCipherSuites: true,
		CipherSuites: []uint16{
			tls.TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256,
			tls.TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384,
			tls.TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305,
		},
	}
}

func (p *HoneypotProxy) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	startTime := time.Now()

	// Get client IP (host only, no port)
	clientIP := remoteHost(r.RemoteAddr)
	if forwarded := r.Header.Get("X-Forwarded-For"); forwarded != "" {
		clientIP = forwarded + "," + clientIP
	}

	// Log request
	reqLog, bodyBytes := p.logRequest(r, clientIP)

	if p.verbose {
		log.Printf("📥 %s %s from %s", r.Method, r.URL.Path, clientIP)
	}

	// Prepare request for forwarding
	proxyReq, err := p.prepareForwardRequest(r, bodyBytes)
	if err != nil {
		log.Printf("❌ Failed to prepare forward request: %v", err)
		p.logErrorResponse(reqLog, http.StatusBadGateway, err, time.Since(startTime))
		http.Error(w, "Proxy Error", http.StatusBadGateway)
		return
	}

	// Forward request to honeypot
	resp, err := p.transport.RoundTrip(proxyReq)
	if err != nil {
		log.Printf("❌ Failed to forward request to honeypot: %v", err)
		p.logErrorResponse(reqLog, http.StatusBadGateway, err, time.Since(startTime))
		http.Error(w, "Bad Gateway", http.StatusBadGateway)
		return
	}
	defer resp.Body.Close()

	// Read response body
	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		log.Printf("❌ Failed to read response body: %v", err)
		p.logErrorResponse(reqLog, http.StatusInternalServerError, err, time.Since(startTime))
		http.Error(w, "Proxy Error", http.StatusInternalServerError)
		return
	}

	// Log response
	duration := time.Since(startTime)
	p.logResponse(resp, respBody, reqLog, duration)

	if p.verbose {
		log.Printf("📤 %d %s (%dms)", resp.StatusCode, http.StatusText(resp.StatusCode), duration.Milliseconds())
	}

	// Copy response headers
	for key, values := range resp.Header {
		for _, value := range values {
			w.Header().Add(key, value)
		}
	}

	// Add proxy header
	w.Header().Set("X-Proxy", "Honeypot-MitM")

	// Send response
	w.WriteHeader(resp.StatusCode)
	if _, err := w.Write(respBody); err != nil {
		log.Printf("⚠️ Failed to write response body: %v", err)
	}
}

func (p *HoneypotProxy) logRequest(r *http.Request, clientIP string) (*RequestLog, []byte) {
	// Read body
	bodyBytes, err := io.ReadAll(r.Body)
	if err != nil {
		log.Printf("⚠️ Failed to read request body: %v", err)
		bodyBytes = []byte{}
	}
	// Restore body for forwarding
	r.Body = io.NopCloser(bytes.NewBuffer(bodyBytes))

	// Convert headers
	headers := make(map[string]string)
	for key, values := range r.Header {
		headers[key] = strings.Join(values, ", ")
	}

	bodyStr, bodyEnc, bodyTrunc := formatBody(bodyBytes)
	dstIP, dstPort := localAddr(r)
	classification := classifyRequest(r, bodyBytes)
	group := experimentGroup(dstIP)

	reqLog := &RequestLog{
		RequestID:       newRequestID(),
		Timestamp:       time.Now().UTC(),
		Method:          r.Method,
		URL:             r.URL.String(),
		Path:            r.URL.Path,
		Query:           r.URL.RawQuery,
		Proto:           r.Proto,
		Host:            r.Host,
		Headers:         headers,
		Body:            bodyStr,
		BodyEncoding:    bodyEnc,
		BodyTruncated:   bodyTrunc,
		ClientIP:        clientIP,
		DestinationIP:   dstIP,
		DestinationPort: dstPort,
		UserAgent:       r.UserAgent(),
		ForwardedTo:     p.targetURL,
		Classification:  classification,
		ExperimentGroup: group,
		TLS:             tlsInfoFromRequest(r),
	}

	// Write to daily log file
	go p.writeRequestLog(reqLog)

	return reqLog, bodyBytes
}

func (p *HoneypotProxy) logResponse(resp *http.Response, bodyBytes []byte, reqLog *RequestLog, duration time.Duration) {
	// Convert headers
	headers := make(map[string]string)
	for key, values := range resp.Header {
		headers[key] = strings.Join(values, ", ")
	}

	bodyStr, bodyEnc, bodyTrunc := formatBody(bodyBytes)

	respLog := &ResponseLog{
		Timestamp:     time.Now(),
		StatusCode:    resp.StatusCode,
		Status:        resp.Status,
		Headers:       headers,
		Body:          bodyStr,
		BodyEncoding:  bodyEnc,
		BodyTruncated: bodyTrunc,
		DurationMs:    duration.Milliseconds(),
	}

	// Write to daily log file
	go p.writeResponseLog(reqLog, respLog)
}

func (p *HoneypotProxy) prepareForwardRequest(origReq *http.Request, bodyBytes []byte) (*http.Request, error) {
	// Build target URL
	targetURL := p.targetURL + origReq.URL.Path
	if origReq.URL.RawQuery != "" {
		targetURL += "?" + origReq.URL.RawQuery
	}

	// Create new request
	proxyReq, err := http.NewRequest(origReq.Method, targetURL, bytes.NewReader(bodyBytes))
	if err != nil {
		return nil, err
	}

	// Copy headers
	for key, values := range origReq.Header {
		for _, value := range values {
			proxyReq.Header.Add(key, value)
		}
	}

	// Add proxy headers (XFF/X-Real-IP carry the host only, no port)
	clientHost := remoteHost(origReq.RemoteAddr)
	proxyReq.Header.Set("X-Forwarded-For", clientHost)
	proxyReq.Header.Set("X-Forwarded-Proto", "https")
	proxyReq.Header.Set("X-Real-IP", clientHost)

	return proxyReq, nil
}

func (p *HoneypotProxy) writeRequestLog(reqLog *RequestLog) {
	logMutex.Lock()
	defer logMutex.Unlock()

	filename := filepath.Join(p.logDir, fmt.Sprintf("requests-%s.jsonl", time.Now().Format("2006-01-02")))
	p.writeJSONLog(filename, reqLog)
}

func (p *HoneypotProxy) writeResponseLog(reqLog *RequestLog, respLog *ResponseLog) {
	logMutex.Lock()
	defer logMutex.Unlock()

	// Combine for easier analysis
	combined := map[string]interface{}{
		"request":  reqLog,
		"response": respLog,
	}

	filename := filepath.Join(p.logDir, fmt.Sprintf("traffic-%s.jsonl", time.Now().Format("2006-01-02")))
	p.writeJSONLog(filename, combined)
}

func (p *HoneypotProxy) writeJSONLog(filename string, data interface{}) {
	file, err := os.OpenFile(filename, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		log.Printf("⚠️ Failed to open log file %s: %v", filename, err)
		return
	}
	defer file.Close()

	encoder := json.NewEncoder(file)
	if err := encoder.Encode(data); err != nil {
		log.Printf("⚠️ Failed to write JSON log: %v", err)
	}
}

func tlsInfoFromRequest(r *http.Request) *TLSInfo {
	if r.TLS == nil {
		return nil
	}
	return &TLSInfo{
		Version:            tlsVersionName(r.TLS.Version),
		CipherSuite:        tls.CipherSuiteName(r.TLS.CipherSuite),
		ServerName:         r.TLS.ServerName,
		NegotiatedProtocol: r.TLS.NegotiatedProtocol,
	}
}

func tlsVersionName(v uint16) string {
	switch v {
	case tls.VersionTLS10:
		return "TLS 1.0"
	case tls.VersionTLS11:
		return "TLS 1.1"
	case tls.VersionTLS12:
		return "TLS 1.2"
	case tls.VersionTLS13:
		return "TLS 1.3"
	default:
		return fmt.Sprintf("0x%04x", v)
	}
}

func remoteHost(addr string) string {
	host, _, err := net.SplitHostPort(addr)
	if err != nil {
		return addr
	}
	return host
}

// formatBody returns a JSON-safe representation of body bytes. When the bytes
// are valid UTF-8 the body is returned as-is with no encoding marker. When
// they are not (binary payloads, mis-encoded shell args, etc.) the body is
// base64-encoded so the raw bytes survive the round-trip into JSON.
func formatBody(b []byte) (body string, encoding string, truncated bool) {
	const maxBody = 10240
	if len(b) > maxBody {
		b = b[:maxBody]
		truncated = true
	}
	if utf8.Valid(b) {
		return string(b), "", truncated
	}
	return base64.StdEncoding.EncodeToString(b), "base64", truncated
}

// logErrorResponse records a synthetic response entry in the traffic log when
// the proxy could not reach the backend (502) or otherwise short-circuited
// the request. Keeps request/response pairing complete for analysis.
func (p *HoneypotProxy) logErrorResponse(reqLog *RequestLog, statusCode int, err error, duration time.Duration) {
	respLog := &ResponseLog{
		Timestamp:  time.Now(),
		StatusCode: statusCode,
		Status:     fmt.Sprintf("%d %s", statusCode, http.StatusText(statusCode)),
		Headers:    map[string]string{},
		Body:       fmt.Sprintf("proxy error: %v", err),
		DurationMs: duration.Milliseconds(),
	}
	go p.writeResponseLog(reqLog, respLog)
}

func newRequestID() string {
	return fmt.Sprintf("%d", time.Now().UnixNano())
}

func localAddr(r *http.Request) (string, string) {
	addr := r.Context().Value(http.LocalAddrContextKey)
	if addr == nil {
		return "", ""
	}

	tcpAddr, ok := addr.(*net.TCPAddr)
	if !ok {
		return "", ""
	}

	return tcpAddr.IP.String(), fmt.Sprintf("%d", tcpAddr.Port)
}

func experimentGroup(destinationIP string) string {
	return "default"
}

func classifyRequest(r *http.Request, body []byte) string {
	path := strings.ToLower(r.URL.Path)
	query := strings.ToLower(r.URL.RawQuery)
	bodyText := strings.ToLower(string(body))
	combined := path + "?" + query + " " + bodyText

	switch {
	case strings.Contains(path, "citrix") ||
		strings.Contains(path, "storeweb") ||
		strings.Contains(path, "/vpn/") ||
		strings.Contains(path, "logonpoint"):
		return "citrix_vpn_probe"

	case r.Method == http.MethodPost &&
		(path == "/" ||
			strings.Contains(path, "wp-login") ||
			strings.Contains(path, "login") ||
			strings.Contains(path, "logon") ||
			strings.Contains(path, "signin") ||
			strings.Contains(bodyText, "username=") ||
			strings.Contains(bodyText, "password=") ||
			strings.Contains(bodyText, "log=") ||
			strings.Contains(bodyText, "pwd=")):
		return "login_attempt"

	case strings.Contains(path, ".env") ||
		strings.Contains(path, "wp-config.php") ||
		strings.Contains(path, "config") ||
		strings.Contains(path, "backup") ||
		strings.Contains(path, ".sql") ||
		strings.Contains(path, ".bak") ||
		strings.Contains(path, ".zip"):
		return "sensitive_file_probe"

	case strings.Contains(path, "xmlrpc.php"):
		return "xmlrpc_probe"

	case strings.Contains(path, "wp-login") ||
		strings.Contains(path, "wp-admin") ||
		strings.Contains(path, "wp-json") ||
		strings.Contains(path, "wp-content") ||
		strings.Contains(path, "wp-includes"):
		return "wordpress_probe"

	case strings.Contains(combined, "../") ||
		strings.Contains(combined, "%2e%2e") ||
		strings.Contains(combined, "/etc/passwd"):
		return "path_traversal_attempt"

	case strings.Contains(combined, "cmd=") ||
		strings.Contains(combined, "powershell") ||
		strings.Contains(combined, "wget ") ||
		strings.Contains(combined, "curl "):
		return "command_injection_probe"

	case r.URL.Path == "/" ||
		r.URL.Path == "/favicon.ico" ||
		r.Method == http.MethodHead:
		return "reconnaissance"

	default:
		return "unknown"
	}
}
