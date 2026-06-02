package main

import (
	"encoding/base64"
	"encoding/json"
	"flag"
	"fmt"
	"io"
	"log"
	"net"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"sync"
	"time"
	"unicode/utf8"
)

const maxBodyLog = 64 * 1024

type RequestLog struct {
	Timestamp    time.Time         `json:"timestamp"`
	Method       string            `json:"method"`
	Path         string            `json:"path"`
	Query        string            `json:"query,omitempty"`
	Proto        string            `json:"proto"`
	Host         string            `json:"host"`
	Headers      map[string]string `json:"headers"`
	Body         string            `json:"body,omitempty"`
	BodyEncoding string            `json:"body_encoding,omitempty"` // "" = utf8, "base64" for non-UTF8 bytes
	Truncated    bool              `json:"body_truncated,omitempty"`
	ClientIP     string            `json:"client_ip"`
	UserAgent    string            `json:"user_agent,omitempty"`
}

const fakeLoginHTML = `<!doctype html>
<html lang="en">
<head><meta charset="utf-8"><title>Admin Sign in</title>
<style>body{font-family:system-ui,sans-serif;background:#f5f6fa;display:flex;align-items:center;justify-content:center;height:100vh;margin:0}form{background:#fff;padding:2rem;border-radius:6px;box-shadow:0 2px 8px rgba(0,0,0,.08);min-width:280px}h1{margin:0 0 1rem;font-size:1.1rem}label{display:block;font-size:.85rem;margin-top:.6rem;color:#444}input{width:100%;padding:.5rem;margin-top:.2rem;box-sizing:border-box;border:1px solid #ccc;border-radius:3px}button{margin-top:1rem;width:100%;padding:.55rem;background:#2d6cdf;color:#fff;border:0;border-radius:3px;cursor:pointer}.note{font-size:.75rem;color:#888;margin-top:.8rem;text-align:center}</style>
</head>
<body>
<form method="POST" action="">
<h1>Administrator sign in</h1>
<label>Username<input type="text" name="username" autocomplete="username" required></label>
<label>Password<input type="password" name="password" autocomplete="current-password" required></label>
<button type="submit">Sign in</button>
<div class="note">Authorized personnel only.</div>
</form>
</body></html>`

const wordpressHomeHTML = `<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Demo Blog - Just another WordPress site</title>
	<meta name="generator" content="WordPress 6.4.3">
	<style>
		body{font-family:Georgia,serif;max-width:900px;margin:40px auto;color:#222;line-height:1.6}
		header{border-bottom:1px solid #ddd;margin-bottom:24px}
		h1{font-size:36px;margin-bottom:4px}
		.tagline{color:#666}
		.post{margin-bottom:28px}
		a{color:#2271b1;text-decoration:none}
		footer{border-top:1px solid #ddd;margin-top:40px;padding-top:16px;color:#777;font-size:14px}
	</style>
</head>
<body>
	<header>
		<h1><a href="/">Demo Blog</a></h1>
		<div class="tagline">Just another WordPress site</div>
	</header>

	<main>
		<article class="post">
			<h2>Hello world!</h2>
			<p>Welcome to WordPress. This is your first post. Edit or delete it, then start writing!</p>
		</article>

		<article class="post">
			<h2>Sample Page</h2>
			<p>This is an example page. It is different from a blog post because it will stay in one place.</p>
		</article>
	</main>

	<footer>
		Powered by WordPress
	</footer>
</body>
</html>`

const wordpressLoginHTML = `<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Log In ‹ Demo Blog — WordPress</title>
	<meta name="robots" content="noindex, nofollow">
	<style>
		body{background:#f0f0f1;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
		#login{width:320px;margin:80px auto}
		h1{text-align:center;color:#2271b1}
		form{background:#fff;border:1px solid #c3c4c7;padding:24px;box-shadow:0 1px 3px rgba(0,0,0,.1)}
		label{display:block;margin-bottom:6px;color:#3c434a}
		input{width:100%;padding:8px;margin-bottom:14px;border:1px solid #8c8f94;box-sizing:border-box}
		button{background:#2271b1;color:white;border:0;border-radius:3px;padding:8px 14px;cursor:pointer}
		.message{border-left:4px solid #72aee6;background:#fff;padding:12px;margin-bottom:16px}
	</style>
</head>
<body>
	<div id="login">
		<h1>WordPress</h1>
		<div class="message">You must log in to access the admin area.</div>
		<form method="POST" action="/wp-login.php">
			<label for="user_login">Username or Email Address</label>
			<input id="user_login" name="log" type="text" autocomplete="username">

			<label for="user_pass">Password</label>
			<input id="user_pass" name="pwd" type="password" autocomplete="current-password">

			<input type="hidden" name="wp-submit" value="Log In">
			<button type="submit">Log In</button>
		</form>
	</div>
</body>
</html>`

const wordpressLoginFailedHTML = `<!doctype html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Log In ‹ Demo Blog — WordPress</title>
	<style>
		body{background:#f0f0f1;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
		#login{width:320px;margin:80px auto}
		h1{text-align:center;color:#2271b1}
		form{background:#fff;border:1px solid #c3c4c7;padding:24px;box-shadow:0 1px 3px rgba(0,0,0,.1)}
		.error{border-left:4px solid #d63638;background:#fff;padding:12px;margin-bottom:16px}
		label{display:block;margin-bottom:6px;color:#3c434a}
		input{width:100%;padding:8px;margin-bottom:14px;border:1px solid #8c8f94;box-sizing:border-box}
		button{background:#2271b1;color:white;border:0;border-radius:3px;padding:8px 14px;cursor:pointer}
	</style>
</head>
<body>
	<div id="login">
		<h1>WordPress</h1>
		<div class="error"><strong>Error:</strong> The username or password you entered is incorrect.</div>
		<form method="POST" action="/wp-login.php">
			<label for="user_login">Username or Email Address</label>
			<input id="user_login" name="log" type="text" autocomplete="username">

			<label for="user_pass">Password</label>
			<input id="user_pass" name="pwd" type="password" autocomplete="current-password">

			<button type="submit">Log In</button>
		</form>
	</div>
</body>
</html>`

// sink fans each log entry out to stdout + (optionally) a file or
// daily-rotated directory. The mutex serialises marshal + write so
// concurrent handlers can't interleave bytes inside a JSON line.
type sink struct {
	mu      sync.Mutex
	writers []io.Writer
}

func (s *sink) Log(v any) {
	payload, err := json.Marshal(v)
	if err != nil {
		log.Printf("log marshal: %v", err)
		return
	}
	payload = append(payload, '\n')
	s.mu.Lock()
	defer s.mu.Unlock()
	for _, w := range s.writers {
		_, _ = w.Write(payload)
	}
}

// dailyFileWriter appends to <dir>/<prefix>-YYYY-MM-DD.jsonl, reopening
// the file each Write so date rollover is automatic. UTC dates to keep
// filenames stable regardless of container/host timezone.
type dailyFileWriter struct{ dir, prefix string }

func (w *dailyFileWriter) Write(p []byte) (int, error) {
	path := filepath.Join(w.dir, fmt.Sprintf("%s-%s.jsonl", w.prefix, time.Now().UTC().Format("2006-01-02")))
	f, err := os.OpenFile(path, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		return 0, err
	}
	defer f.Close()
	return f.Write(p)
}

func main() {
	listen := flag.String("listen", ":8080", "Address to listen on")
	enableTLS := flag.Bool("tls", false, "Enable HTTPS/TLS for the honeypot backend")
	certFile := flag.String("cert", "testdata/backend-cert.pem", "TLS certificate file for honeypot HTTPS")
	keyFile := flag.String("key", "testdata/backend-key.pem", "TLS private key file for honeypot HTTPS")
	logDir := flag.String("log-dir", "./logs", "Directory for daily-rotated honeypot-YYYY-MM-DD.jsonl files (empty to disable)")
	logFile := flag.String("log-file", "", "Append all logs to this single file (overrides --log-dir)")
	quiet := flag.Bool("quiet", false, "Suppress stdout output of request logs")
	flag.Parse()

	var writers []io.Writer
	if !*quiet {
		writers = append(writers, os.Stdout)
	}
	if *logFile != "" {
		f, err := os.OpenFile(*logFile, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
		if err != nil {
			log.Fatalf("open log file: %v", err)
		}
		defer f.Close()
		writers = append(writers, f)
	} else if *logDir != "" {
		if err := os.MkdirAll(*logDir, 0755); err != nil {
			log.Fatalf("create log dir: %v", err)
		}
		writers = append(writers, &dailyFileWriter{dir: *logDir, prefix: "honeypot"})
	}
	snk := &sink{writers: writers}

	srv := &http.Server{
		Addr:         *listen,
		Handler:      handler(snk),
		ReadTimeout:  20 * time.Second,
		WriteTimeout: 20 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	if *enableTLS {
		log.Printf("honeypot listening with TLS on %s (log-dir=%q log-file=%q quiet=%v)", *listen, *logDir, *logFile, *quiet)
		if err := srv.ListenAndServeTLS(*certFile, *keyFile); err != nil {
			log.Fatal(err)
		}
	} else {
		log.Printf("honeypot listening on %s (log-dir=%q log-file=%q quiet=%v)", *listen, *logDir, *logFile, *quiet)
		if err := srv.ListenAndServe(); err != nil {
			log.Fatal(err)
		}
	}
}

func handler(s *sink) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		logRequest(s, r)

		w.Header().Set("Server", "Apache/2.4.41 (Ubuntu)")

		switch {
		case r.URL.Path == "/":
			handleWordPressHome(w, r)

		case r.URL.Path == "/wp-login.php":
			handleWordPressLogin(w, r)

		case r.URL.Path == "/wp-admin" || r.URL.Path == "/wp-admin/":
			http.Redirect(w, r, "/wp-login.php", http.StatusFound)

		case r.URL.Path == "/xmlrpc.php":
			handleXMLRPC(w, r)

		case r.URL.Path == "/wp-json/" || r.URL.Path == "/wp-json":
			handleWPJSON(w, r)

		case r.URL.Path == "/.env" || r.URL.Path == "/wp-config.php":
			handleForbidden(w, r)

		case strings.HasPrefix(r.URL.Path, "/wp-content/"):
			handleWPContent(w, r)

		default:
			handleNotFound(w, r)
		}
	})
}

func handleWordPressHome(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet && r.Method != http.MethodHead {
		methodNotAllowed(w, "GET, HEAD")
		return
	}

	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.WriteHeader(http.StatusOK)

	if r.Method == http.MethodGet {
		_, _ = io.WriteString(w, wordpressHomeHTML)
	}
}

func handleWordPressLogin(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")

	switch r.Method {
	case http.MethodGet, http.MethodHead:
		w.WriteHeader(http.StatusOK)
		if r.Method == http.MethodGet {
			_, _ = io.WriteString(w, wordpressLoginHTML)
		}

	case http.MethodPost:
		w.WriteHeader(http.StatusUnauthorized)
		_, _ = io.WriteString(w, wordpressLoginFailedHTML)

	default:
		methodNotAllowed(w, "GET, HEAD, POST")
	}
}

func handleXMLRPC(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/xml; charset=utf-8")

	switch r.Method {
	case http.MethodPost:
		w.WriteHeader(http.StatusOK)
		_, _ = io.WriteString(w, `<?xml version="1.0"?>
<methodResponse>
	<fault>
		<value>
			<struct>
				<member>
					<name>faultCode</name>
					<value><int>403</int></value>
				</member>
				<member>
					<name>faultString</name>
					<value><string>Incorrect username or password.</string></value>
				</member>
			</struct>
		</value>
	</fault>
</methodResponse>`)

	case http.MethodGet, http.MethodHead:
		w.WriteHeader(http.StatusOK)
		if r.Method == http.MethodGet {
			_, _ = io.WriteString(w, "XML-RPC server accepts POST requests only.")
		}

	default:
		methodNotAllowed(w, "GET, HEAD, POST")
	}
}

func handleWPJSON(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet && r.Method != http.MethodHead {
		methodNotAllowed(w, "GET, HEAD")
		return
	}

	w.Header().Set("Content-Type", "application/json; charset=utf-8")
	w.WriteHeader(http.StatusOK)

	if r.Method == http.MethodGet {
		_, _ = io.WriteString(w, `{
  "name": "Demo Blog",
  "description": "Just another WordPress site",
  "url": "https://example.invalid",
  "home": "https://example.invalid",
  "gmt_offset": "0",
  "timezone_string": "",
  "namespaces": ["oembed/1.0", "wp/v2"]
}`)
	}
}

func handleForbidden(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.WriteHeader(http.StatusForbidden)
	_, _ = io.WriteString(w, "<h1>403 Forbidden</h1>")
}

func handleWPContent(w http.ResponseWriter, r *http.Request) {
	if strings.HasSuffix(r.URL.Path, ".css") {
		w.Header().Set("Content-Type", "text/css")
		w.WriteHeader(http.StatusOK)
		_, _ = io.WriteString(w, "body{font-family:sans-serif}")
		return
	}

	if strings.HasSuffix(r.URL.Path, ".js") {
		w.Header().Set("Content-Type", "application/javascript")
		w.WriteHeader(http.StatusOK)
		_, _ = io.WriteString(w, "console.log('wordpress');")
		return
	}

	handleNotFound(w, r)
}

func handleNotFound(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.WriteHeader(http.StatusNotFound)
	_, _ = io.WriteString(w, "<h1>404 Not Found</h1>")
}

func methodNotAllowed(w http.ResponseWriter, allowed string) {
	w.Header().Set("Allow", allowed)
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	w.WriteHeader(http.StatusMethodNotAllowed)
	_, _ = io.WriteString(w, "<h1>405 Method Not Allowed</h1>")
}

func logRequest(s *sink, r *http.Request) {
	body, encoding, truncated := readBody(r)
	entry := RequestLog{
		Timestamp:    time.Now().UTC(),
		Method:       r.Method,
		Path:         r.URL.Path,
		Query:        r.URL.RawQuery,
		Proto:        r.Proto,
		Host:         r.Host,
		Headers:      flattenHeaders(r.Header),
		Body:         body,
		BodyEncoding: encoding,
		Truncated:    truncated,
		ClientIP:     clientIP(r),
		UserAgent:    r.UserAgent(),
	}
	s.Log(&entry)
}

// readBody returns a JSON-safe representation of the request body. Non-UTF-8
// payloads are base64-encoded so the raw bytes survive into the log.
func readBody(r *http.Request) (body string, encoding string, truncated bool) {
	if r.Body == nil {
		return "", "", false
	}
	defer r.Body.Close()
	limited := io.LimitReader(r.Body, maxBodyLog+1)
	b, err := io.ReadAll(limited)
	if err != nil {
		return "", "", false
	}
	if len(b) > maxBodyLog {
		b = b[:maxBodyLog]
		truncated = true
	}
	if utf8.Valid(b) {
		return string(b), "", truncated
	}
	return base64.StdEncoding.EncodeToString(b), "base64", truncated
}

func flattenHeaders(h http.Header) map[string]string {
	out := make(map[string]string, len(h))
	for k, v := range h {
		out[k] = strings.Join(v, ", ")
	}
	return out
}

func clientIP(r *http.Request) string {
	if xff := r.Header.Get("X-Forwarded-For"); xff != "" {
		if i := strings.IndexByte(xff, ','); i > 0 {
			return strings.TrimSpace(xff[:i])
		}
		return strings.TrimSpace(xff)
	}
	if xri := r.Header.Get("X-Real-IP"); xri != "" {
		return xri
	}
	host, _, err := net.SplitHostPort(r.RemoteAddr)
	if err != nil {
		return r.RemoteAddr
	}
	return host
}
