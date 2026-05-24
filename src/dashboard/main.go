package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"html/template"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"time"
)

type TrafficEntry struct {
	Request struct {
		RequestID       string `json:"request_id"`
		Timestamp       string `json:"timestamp"`
		Method          string `json:"method"`
		Path            string `json:"path"`
		Query           string `json:"query"`
		Host            string `json:"host"`
		ClientIP        string `json:"client_ip"`
		DestinationIP   string `json:"destination_ip"`
		DestinationPort string `json:"destination_port"`
		UserAgent       string `json:"user_agent"`
		ForwardedTo     string `json:"forwarded_to"`
		Classification  string `json:"classification"`
		ExperimentGroup string `json:"experiment_group"`
		Body            string `json:"body"`
		BodyEncoding    string `json:"body_encoding"`
		BodyTruncated   bool   `json:"body_truncated"`
		TLS             struct {
			Version            string `json:"version"`
			CipherSuite        string `json:"cipher_suite"`
			ServerName         string `json:"server_name"`
			NegotiatedProtocol string `json:"negotiated_protocol"`
		} `json:"tls"`
	} `json:"request"`

	Response struct {
		StatusCode int    `json:"status_code"`
		Status     string `json:"status"`
		DurationMs int64  `json:"duration_ms"`
	} `json:"response"`
}

type PageData struct {
	LogFile             string
	Rows                []TrafficEntry
	TotalRequests       int
	UniqueClients       int
	LoginAttempts       int
	Reconnaissance      int
	CitrixVPNProbes     int
	ExploitLikeRequests int
}

func main() {
	listen := flag.String("listen", "127.0.0.1:9090", "Dashboard listen address")
	logDir := flag.String("log-dir", "./logs", "Directory containing traffic logs")
	flag.Parse()

	http.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		rows, logFile, err := readTodayTraffic(*logDir, 200)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		data := buildPageData(rows, logFile)

		if err := pageTemplate.Execute(w, data); err != nil {
			log.Printf("template error: %v", err)
		}
	})

	log.Printf("dashboard listening on http://%s", *listen)
	log.Printf("reading logs from %s", *logDir)

	if err := http.ListenAndServe(*listen, nil); err != nil {
		log.Fatal(err)
	}
}

func readTodayTraffic(logDir string, limit int) ([]TrafficEntry, string, error) {
	filename := filepath.Join(logDir, "traffic-"+time.Now().UTC().Format("2006-01-02")+".jsonl")

	file, err := os.Open(filename)
	if err != nil {
		if os.IsNotExist(err) {
			return []TrafficEntry{}, filename, nil
		}
		return nil, filename, err
	}
	defer file.Close()

	var rows []TrafficEntry
	scanner := bufio.NewScanner(file)

	// Allow longer JSON lines than the scanner default.
	scanner.Buffer(make([]byte, 1024), 10*1024*1024)

	for scanner.Scan() {
		var entry TrafficEntry
		if err := json.Unmarshal(scanner.Bytes(), &entry); err != nil {
			log.Printf("skip bad json line: %v", err)
			continue
		}
		rows = append(rows, entry)
	}

	if err := scanner.Err(); err != nil {
		return nil, filename, err
	}

	if len(rows) > limit {
		rows = rows[len(rows)-limit:]
	}

	// Show newest first.
	for i, j := 0, len(rows)-1; i < j; i, j = i+1, j-1 {
		rows[i], rows[j] = rows[j], rows[i]
	}

	return rows, filename, nil
}

func buildPageData(rows []TrafficEntry, logFile string) PageData {
	clients := map[string]bool{}

	data := PageData{
		LogFile:       logFile,
		Rows:          rows,
		TotalRequests: len(rows),
	}

	for _, row := range rows {
		if row.Request.ClientIP != "" {
			clients[row.Request.ClientIP] = true
		}

		switch row.Request.Classification {
		case "login_attempt":
			data.LoginAttempts++
		case "reconnaissance":
			data.Reconnaissance++
		case "citrix_vpn_probe":
			data.CitrixVPNProbes++
		case "path_traversal_attempt", "command_injection_probe", "sensitive_file_probe", "xmlrpc_probe":
			data.ExploitLikeRequests++
		}
	}

	data.UniqueClients = len(clients)
	return data
}

func meaning(row TrafficEntry) string {
	switch row.Request.Classification {
	case "login_attempt":
		return "Login attempt"
	case "reconnaissance":
		if row.Request.Path == "/favicon.ico" {
			return "Browser requested site icon"
		}
		return "Basic visit / scan"
	case "citrix_vpn_probe":
		return "Citrix/VPN-related probe"
	case "wordpress_probe":
		return "WordPress probe"
	case "xmlrpc_probe":
		return "WordPress XML-RPC probe"
	case "path_traversal_attempt":
		return "Path traversal attempt"
	case "command_injection_probe":
		return "Command injection probe"
	case "sensitive_file_probe":
		return "Sensitive file probe"
	case "":
		return "Unclassified"
	default:
		return row.Request.Classification
	}
}

func formatTime(ts string) string {
	t, err := time.Parse(time.RFC3339Nano, ts)
	if err != nil {
		return ts
	}

	loc, err := time.LoadLocation("Europe/Amsterdam")
	if err != nil {
		return t.UTC().Format("02 Jan 2006 15:04:05 UTC")
	}

	return t.In(loc).Format("02 Jan 2006 15:04:05 MST")
}

func backendScheme(row TrafficEntry) string {
	if strings.HasPrefix(row.Request.ForwardedTo, "https://") {
		return "HTTPS"
	}
	if strings.HasPrefix(row.Request.ForwardedTo, "http://") {
		return "HTTP"
	}
	return "-"
}

var pageTemplate = template.Must(template.New("dashboard").Funcs(template.FuncMap{
	"meaning":       meaning,
	"formatTime":    formatTime,
	"backendScheme": backendScheme,
}).Parse(`
<!doctype html>
<html>
<head>
	<meta charset="utf-8">
	<title>TLS Honeypot Dashboard</title>
	<meta http-equiv="refresh" content="5">
	<style>
		.body {
			max-width: 420px;
			word-break: break-word;
		}
		.muted {
			color: #999;
		}
		body {
			font-family: system-ui, sans-serif;
			background: #f5f6fa;
			margin: 0;
			padding: 24px;
			color: #222;
		}
		h1 {
			margin: 0 0 8px;
			font-size: 34px;
		}
		.meta {
			color: #666;
			margin-bottom: 20px;
		}
		.cards {
			display: grid;
			grid-template-columns: repeat(6, minmax(140px, 1fr));
			gap: 14px;
			margin-bottom: 22px;
		}
		.card {
			background: white;
			border-radius: 12px;
			padding: 16px;
			box-shadow: 0 2px 8px rgba(0,0,0,.08);
		}
		.card .label {
			color: #666;
			font-size: 13px;
			margin-bottom: 8px;
		}
		.card .value {
			font-size: 28px;
			font-weight: 800;
		}
		table {
			width: 100%;
			border-collapse: collapse;
			background: white;
			box-shadow: 0 2px 8px rgba(0,0,0,.08);
			border-radius: 8px;
			overflow: hidden;
		}
		th, td {
			text-align: left;
			padding: 10px 12px;
			border-bottom: 1px solid #eee;
			font-size: 14px;
			vertical-align: top;
		}
		th {
			background: #222;
			color: white;
			position: sticky;
			top: 0;
		}
		tr:hover {
			background: #f0f4ff;
		}
		code {
			background: #eef0f4;
			padding: 2px 4px;
			border-radius: 4px;
		}
		.badge {
			display: inline-block;
			padding: 3px 8px;
			border-radius: 999px;
			background: #e8edf7;
			font-size: 12px;
			font-weight: 600;
		}
		.badge-login {
			background: #ffe8cc;
		}
		.badge-exploit {
			background: #ffd6d6;
		}
		.badge-citrix {
			background: #dceeff;
		}
		.ua {
			max-width: 320px;
			word-break: break-word;
			color: #555;
		}
		.meaning {
			font-weight: 700;
		}
	</style>
</head>
<body>
	<h1>TLS Honeypot Dashboard</h1>
	<div class="meta">
		Reading: <code>{{.LogFile}}</code> · Auto-refreshes every 5 seconds · Showing latest {{len .Rows}} entries
	</div>

	<div class="cards">
		<div class="card">
			<div class="label">Total requests</div>
			<div class="value">{{.TotalRequests}}</div>
		</div>
		<div class="card">
			<div class="label">Unique clients</div>
			<div class="value">{{.UniqueClients}}</div>
		</div>
		<div class="card">
			<div class="label">Login attempts</div>
			<div class="value">{{.LoginAttempts}}</div>
		</div>
		<div class="card">
			<div class="label">Reconnaissance</div>
			<div class="value">{{.Reconnaissance}}</div>
		</div>
		<div class="card">
			<div class="label">Citrix/VPN probes</div>
			<div class="value">{{.CitrixVPNProbes}}</div>
		</div>
		<div class="card">
			<div class="label">Exploit-like</div>
			<div class="value">{{.ExploitLikeRequests}}</div>
		</div>
	</div>

	<table>
		<thead>
			<tr>
				<th>Time</th>
				<th>Meaning</th>
				<th>Client</th>
				<th>Destination</th>
				<th>Method</th>
				<th>Path</th>
				<th>Status</th>
				<th>Class</th>
				<th>TLS</th>
				<th>Backend</th>
				<th>Duration</th>
				<th>Body</th>
				<th>User-Agent</th>
			</tr>
		</thead>
		<tbody>
			{{range .Rows}}
			<tr>
				<td><code>{{formatTime .Request.Timestamp}}</code></td>
				<td class="meaning">{{meaning .}}</td>
				<td>{{.Request.ClientIP}}</td>
				<td>{{.Request.DestinationIP}}:{{.Request.DestinationPort}}</td>
				<td><strong>{{.Request.Method}}</strong></td>
				<td><code>{{.Request.Path}}</code>{{if .Request.Query}}?{{.Request.Query}}{{end}}</td>
				<td>{{.Response.StatusCode}}</td>
				<td>
					<span class="badge {{if eq .Request.Classification "login_attempt"}}badge-login{{end}}{{if eq .Request.Classification "citrix_vpn_probe"}}badge-citrix{{end}}{{if or (eq .Request.Classification "path_traversal_attempt") (eq .Request.Classification "command_injection_probe") (eq .Request.Classification "sensitive_file_probe")}}badge-exploit{{end}}">
						{{.Request.Classification}}
					</span>
				</td>
				<td>{{.Request.TLS.Version}}</td>
				<td><span class="badge">{{backendScheme .}}</span></td>
				<td>{{.Response.DurationMs}} ms</td>
					<td class="body">
						{{if .Request.Body}}
							<code>{{.Request.Body}}</code>
							{{if .Request.BodyTruncated}}<span class="badge">truncated</span>{{end}}
							{{if .Request.BodyEncoding}}<span class="badge">{{.Request.BodyEncoding}}</span>{{end}}
						{{else}}
							<span class="muted">-</span>
						{{end}}
					</td>
					<td class="ua">{{.Request.UserAgent}}</td>
			</tr>
			{{else}}
			<tr>
				<td colspan="13">No traffic logs found yet. Visit <code>https://localhost:8443</code> first.</td>
			</tr>
			{{end}}
		</tbody>
	</table>
</body>
</html>
`))
