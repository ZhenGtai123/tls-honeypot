# TLS MitM Honeypot

TU Delft Hacking Lab — Project #12.

## Goal

Set up a TLS proxy between a client and a target service. The proxy terminates TLS, decrypts the traffic, logs it, and forwards it on to the real service — so we can observe what attackers do over otherwise-encrypted channels.

## Stack

- Go (target: 1.23+)

## References

- https://github.com/Nirusu/how-to-setup-a-honeypot
- https://www.mitmproxy.org/

## Responsible Professor

Harm Griffioen

## Build

```
go run ./...
```

(Empty for now — add `cmd/proxy/main.go` when ready.)
