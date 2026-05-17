package main

import (
	"encoding/json"
	"flag"
	"io"
	"log"
	"net"
	"net/http"
	"os"
	"strings"
	"time"
)

const maxBodyLog = 64 * 1024

type RequestLog struct {
	Timestamp time.Time         `json:"timestamp"`
	Method    string            `json:"method"`
	Path      string            `json:"path"`
	Query     string            `json:"query,omitempty"`
	Proto     string            `json:"proto"`
	Host      string            `json:"host"`
	Headers   map[string]string `json:"headers"`
	Body      string            `json:"body,omitempty"`
	Truncated bool              `json:"body_truncated,omitempty"`
	ClientIP  string            `json:"client_ip"`
	UserAgent string            `json:"user_agent,omitempty"`
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

func main() {
	listen := flag.String("listen", ":8080", "Address to listen on (HTTP only; the proxy handles TLS)")
	logFile := flag.String("log-file", "", "File to append JSON-lines logs to; empty means stdout")
	flag.Parse()

	var logOut io.Writer = os.Stdout
	if *logFile != "" {
		f, err := os.OpenFile(*logFile, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0644)
		if err != nil {
			log.Fatalf("open log file: %v", err)
		}
		defer f.Close()
		logOut = f
	}
	enc := json.NewEncoder(logOut)

	srv := &http.Server{
		Addr:         *listen,
		Handler:      handler(enc),
		ReadTimeout:  20 * time.Second,
		WriteTimeout: 20 * time.Second,
		IdleTimeout:  60 * time.Second,
	}

	log.Printf("honeypot listening on %s", *listen)
	if err := srv.ListenAndServe(); err != nil {
		log.Fatal(err)
	}
}

func handler(enc *json.Encoder) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		logRequest(enc, r)

		w.Header().Set("Server", "Apache/2.4.41 (Ubuntu)")
		w.Header().Set("Content-Type", "text/html; charset=utf-8")

		switch r.Method {
		case http.MethodGet, http.MethodHead:
			w.WriteHeader(http.StatusOK)
			if r.Method == http.MethodGet {
				_, _ = io.WriteString(w, fakeLoginHTML)
			}
		case http.MethodPost:
			w.WriteHeader(http.StatusUnauthorized)
			_, _ = io.WriteString(w, "<h1>Invalid credentials</h1>")
		default:
			w.Header().Set("Allow", "GET, HEAD, POST")
			w.WriteHeader(http.StatusMethodNotAllowed)
		}
	})
}

func logRequest(enc *json.Encoder, r *http.Request) {
	body, truncated := readBody(r)
	entry := RequestLog{
		Timestamp: time.Now().UTC(),
		Method:    r.Method,
		Path:      r.URL.Path,
		Query:     r.URL.RawQuery,
		Proto:     r.Proto,
		Host:      r.Host,
		Headers:   flattenHeaders(r.Header),
		Body:      body,
		Truncated: truncated,
		ClientIP:  clientIP(r),
		UserAgent: r.UserAgent(),
	}
	if err := enc.Encode(&entry); err != nil {
		log.Printf("log encode error: %v", err)
	}
}

func readBody(r *http.Request) (string, bool) {
	if r.Body == nil {
		return "", false
	}
	defer r.Body.Close()
	limited := io.LimitReader(r.Body, maxBodyLog+1)
	b, err := io.ReadAll(limited)
	if err != nil {
		return "", false
	}
	if len(b) > maxBodyLog {
		return string(b[:maxBodyLog]), true
	}
	return string(b), false
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
