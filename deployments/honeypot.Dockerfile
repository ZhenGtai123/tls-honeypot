FROM golang:1.23-alpine AS build
WORKDIR /src
COPY go.mod ./
COPY src/ ./src/
RUN CGO_ENABLED=0 GOOS=linux go build \
    -trimpath -ldflags="-s -w" \
    -o /out/honeypot ./src/honeypot

FROM gcr.io/distroless/static-debian12
COPY --from=build /out/honeypot /honeypot
EXPOSE 8080
ENTRYPOINT ["/honeypot"]
