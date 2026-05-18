FROM golang:1.23-alpine AS build
WORKDIR /src
COPY go.mod ./
COPY src/ ./src/
RUN CGO_ENABLED=0 GOOS=linux go build \
    -trimpath -ldflags="-s -w" \
    -o /out/proxy ./src/proxy

FROM gcr.io/distroless/static-debian12
COPY --from=build /out/proxy /proxy
EXPOSE 8443
ENTRYPOINT ["/proxy"]
