## Requirements

- Go installed
- Git installed
- Windows PowerShell

## 1. Generate local certificates

Each group member should generate their own local certificates.

We use two certificate/key pairs:

```text
testdata/cert.pem              proxy certificate
testdata/key.pem               proxy private key

testdata/backend-cert.pem      honeypot certificate
testdata/backend-key.pem       honeypot private key
```

Generate the proxy certificate:

```powershell
go run "C:\Program Files\Go\src\crypto\tls\generate_cert.go" -host localhost
move cert.pem testdata\cert.pem
move key.pem testdata\key.pem
```

Generate the honeypot/backend certificate:

```powershell
go run "C:\Program Files\Go\src\crypto\tls\generate_cert.go" -host localhost
move cert.pem testdata\backend-cert.pem
move key.pem testdata\backend-key.pem
```

Do **not** commit your private keys:

```text
testdata/key.pem
testdata/backend-key.pem
```

## 2. Run the project

Open **three different terminals** in the project root.

In each terminal, first run:

```powershell
cd C:\Users\user\Documents\tls-honeypot
```
(basically go to directory you have the code at.)

Then run the following commands in order.

## Terminal 1 - Honeypot

```powershell
go run ./src/honeypot -listen :8444 -tls -cert testdata/backend-cert.pem -key testdata/backend-key.pem
```

## Terminal 2 - Proxy

```powershell
go run ./src/proxy -listen :8443 -target localhost:8444 -forward-https -cert testdata/cert.pem -key testdata/key.pem -log-dir ./logs -verbose
```

## Terminal 3 - Dashboard

```powershell
go run ./src/dashboard -listen 127.0.0.1:9090 -log-dir ./logs
```

## 3. Open the dashboard

Open this in your browser:

```text
http://127.0.0.1:9090
```

The dashboard shows logged requests, classifications, TLS version, backend protocol, request body, and response status.

## 4. Test URLs

Open these through the proxy:

```text
https://localhost:8443/
https://localhost:8443/wp-login.php
https://localhost:8443/wp-admin/
https://localhost:8443/wp-json/
https://localhost:8443/xmlrpc.php
https://localhost:8443/.env
https://localhost:8443/wp-config.php
https://localhost:8443/wp-content/themes/twentytwenty/style.css
https://localhost:8443/backup.zip
```

You can also submit a fake username and password at:

```text
https://localhost:8443/wp-login.php
```

Then check the dashboard to see the captured login attempt.

## Notes

- The browser certificate warning is expected during local testing.
- Each group member should generate their own local certificates.
- Do not commit private keys:
  - `testdata/key.pem`
  - `testdata/backend-key.pem`
- Do not expose the dashboard publicly.
