package main

import (
	"crypto/tls"
	"log"
	"net/http"
	"net/http/httputil"
	"net/url"
)

func main() {
	if err := runTLSServer(); err != nil {
		log.Fatal(err)
	}
}

func runTLSServer() error {
	cert, err := tls.LoadX509KeyPair("server.crt", "server.key")
	if err != nil {
		return err
	}
	tlsConf := &tls.Config{
		Certificates: []tls.Certificate{cert},
		MinVersion:   tls.VersionTLS12,
	}
	ln, err := tls.Listen("tcp", ":8443", tlsConf)
	if err != nil {
		return err
	}
	defer ln.Close()

	target, err := url.Parse("https://example.com")
	if err != nil {
		return err
	}
	// Use Rewrite + SetURL so the outbound Host matches the upstream (since Go 1.20,
	// NewSingleHostReverseProxy leaves Host as the client's, which Cloudflare rejects).
	proxy := &httputil.ReverseProxy{
		Rewrite: func(r *httputil.ProxyRequest) {
			r.SetURL(target)
		},
	}
	proxy.ErrorHandler = func(w http.ResponseWriter, r *http.Request, err error) {
		log.Printf("upstream error: %v (client %s)", err, r.RemoteAddr)
		http.Error(w, "bad gateway", http.StatusBadGateway)
	}

	return http.Serve(ln, logRequests(proxy))
}

func logRequests(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		log.Printf("%s %s %s Host=%q from %s", r.Method, r.RequestURI, r.Proto, r.Host, r.RemoteAddr)
		next.ServeHTTP(w, r)
	})
}
