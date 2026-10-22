# socketlab

A planned test bench for experimenting with TCP framing, WebSocket behavior, and slow-client handling.

> **Status: design stage.** This repository currently contains documentation only; the server, client, and load tests are not implemented yet.

## Goal

Make protocol edge cases reproducible with small commands and fixtures rather than relying on a production service to expose them.

## Initial experiments

- TCP echo client/server with explicit framing.
- Tests that split a frame header or payload across multiple reads.
- Tests for oversized lengths, early disconnects, and partial writes.
- A slow-client mode to observe backpressure and bounded buffering.
- Optional WebSocket experiments after the TCP harness is stable.

## Safety

- Bind to loopback by default.
- Require an explicit option to listen on a non-loopback interface.
- Set maximum frame size, connection count, and idle timeout.
- Never interpret received bytes as commands or write received files to disk.
- Keep load tests opt-in and explain their resource requirements.

## Planned milestones

- [ ] Specify framing and error behavior.
- [ ] Implement an echo server and client.
- [ ] Add fragmentation and malformed-frame tests.
- [ ] Add backpressure metrics and a reproducible load-test recipe.
- [ ] Document platform support based on actual CI results.

## Measurements

No throughput figures are published yet. Any future benchmark should include hardware, compiler/runtime version, payload size, concurrency, and exact command line.

## License

MIT. See [LICENSE](LICENSE).


## Safe lab defaults

Bind test services to loopback by default, use finite timeouts and maximum frame sizes, and keep load tests bounded. Use ephemeral ports in automated tests and close sockets on success, error, and cancellation.
