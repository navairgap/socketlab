# socketlab

A loopback-first test bench for TCP framing and WebSocket behavior.

> **Current state: TCP frame-decoder prototype.** The first implementation is a dependency-free incremental decoder for four-byte big-endian length-prefixed frames. There is no listener, WebSocket service, or load generator yet.

## Framing prototype

The decoder accepts arbitrary TCP chunks, including split headers, split payloads, and multiple frames in one read. It rejects oversized declarations before buffering payload bytes and distinguishes clean EOF from EOF during a header or payload. A protocol error makes that decoder instance unusable; callers should close the affected connection rather than attempting to resynchronize on arbitrary payload bytes.

Run the focused tests with:

    python -m unittest discover -s tests -v

## Safety defaults

- Bind test services to loopback by default.
- Keep frame size and connection count bounded.
- Use finite deadlines for header, payload, and idle phases.
- Never interpret received bytes as commands or write received files to disk.
- Keep load tests opt-in and use ephemeral ports in automated tests.

## Remaining work

- [ ] Add a loopback echo server and client.
- [ ] Add deterministic header, payload, and idle deadlines.
- [ ] Add bounded connection management and backpressure metrics.
- [ ] Add WebSocket experiments after the TCP harness is stable.

No throughput figures are published. Any future benchmark must record hardware, runtime version, payload size, concurrency, and exact command line.

## License

MIT. See [LICENSE](LICENSE).
