package main

import (
    "bytes"
    "crypto/tls"
    "encoding/json"
    "flag"
    "fmt"
    "io"
    "log"
    "net/http"
    "os"
    "path/filepath"
    "strings"
    "sync"
    "time"
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
    Timestamp   time.Time         `json:"timestamp"`
    Method      string            `json:"method"`
    URL         string            `json:"url"`
    Proto       string            `json:"proto"`
    Host        string            `json:"host"`
    Headers     map[string]string `json:"headers"`
    Body        string            `json:"body,omitempty"`
    ClientIP    string            `json:"client_ip"`
    ForwardedTo string            `json:"forwarded_to"`
}

type ResponseLog struct {
    Timestamp  time.Time         `json:"timestamp"`
    StatusCode int               `json:"status_code"`
    Status     string            `json:"status"`
    Headers    map[string]string `json:"headers"`
    Body       string            `json:"body,omitempty"`
    DurationMs int64             `json:"duration_ms"`
}

var (
    logMutex sync.Mutex
)

func main() {
    // Command line flags
    listenAddr := flag.String("listen", ":8443", "Address to listen on (use :443 in production, :8443 for unprivileged dev)")
    targetAddr := flag.String("target", "localhost:8080", "Target honeypot address (the proxy forwards plaintext to this backend)")
    certFile := flag.String("cert", "testdata/cert.pem", "TLS certificate file")
    keyFile := flag.String("key", "testdata/key.pem", "TLS private key file")
    logDir := flag.String("log-dir", "./logs", "Directory to store logs")
    forwardHTTPS := flag.Bool("forward-https", false, "Forward to honeypot using HTTPS (default HTTP)")
    verbose := flag.Bool("verbose", false, "Log every request/response to console")
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

    // Setup HTTP server
    server := &http.Server{
        Addr:         *listenAddr,
        Handler:      proxy,
        TLSConfig:    createTLSConfig(),
        ReadTimeout:  30 * time.Second,
        WriteTimeout: 30 * time.Second,
        IdleTimeout:  60 * time.Second,
    }

    log.Printf("🚀 Starting honeypot proxy on %s", *listenAddr)
    log.Printf("🎯 Forwarding to %s", targetURL)
    log.Printf("📝 Logging to %s", *logDir)

    // Start server with TLS
    if err := server.ListenAndServeTLS(*certFile, *keyFile); err != nil {
        log.Fatalf("Failed to start server: %v", err)
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
        MinVersion: tls.VersionTLS12,
        MaxVersion: tls.VersionTLS13,
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

    // Get client IP
    clientIP := r.RemoteAddr
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
        http.Error(w, "Proxy Error", http.StatusBadGateway)
        return
    }

    // Forward request to honeypot
    resp, err := p.transport.RoundTrip(proxyReq)
    if err != nil {
        log.Printf("❌ Failed to forward request to honeypot: %v", err)
        http.Error(w, "Bad Gateway", http.StatusBadGateway)
        return
    }
    defer resp.Body.Close()

    // Read response body
    respBody, err := io.ReadAll(resp.Body)
    if err != nil {
        log.Printf("❌ Failed to read response body: %v", err)
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

    // Truncate body if too large (e.g., 10KB limit for logging)
    bodyStr := string(bodyBytes)
    if len(bodyStr) > 10240 {
        bodyStr = bodyStr[:10240] + "... (truncated)"
    }

    reqLog := &RequestLog{
        Timestamp:   time.Now(),
        Method:      r.Method,
        URL:         r.URL.String(),
        Proto:       r.Proto,
        Host:        r.Host,
        Headers:     headers,
        Body:        bodyStr,
        ClientIP:    clientIP,
        ForwardedTo: p.targetURL,
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

    // Truncate body if too large
    bodyStr := string(bodyBytes)
    if len(bodyStr) > 10240 {
        bodyStr = bodyStr[:10240] + "... (truncated)"
    }

    respLog := &ResponseLog{
        Timestamp:  time.Now(),
        StatusCode: resp.StatusCode,
        Status:     resp.Status,
        Headers:    headers,
        Body:       bodyStr,
        DurationMs: duration.Milliseconds(),
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

    // Add proxy headers
    proxyReq.Header.Set("X-Forwarded-For", origReq.RemoteAddr)
    proxyReq.Header.Set("X-Forwarded-Proto", "https")
    proxyReq.Header.Set("X-Real-IP", origReq.RemoteAddr)

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
