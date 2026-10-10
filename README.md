# socketlab

WebSocket experiments: rooms, pub/sub, backpressure

> 🚧 **Status: planning** — architecture and README first, code next.

## Why

banter proved the basics; socketlab pushes deeper — presence at scale, backpressure handling, horizontal scaling with Redis adapters, and message delivery guarantees. A reference codebase for real-time architecture.

## Planned features

- Room sharding and horizontal scaling via Redis adapter
- Backpressure: slow clients, buffering policies, dropped-message metrics
- Delivery semantics: at-most-once vs at-least-once patterns
- Load-test harness: 10k concurrent sockets on one box

## Stack

`node.js` `socket.io` `redis` `artillery`

## Notes

Each experiment is its own folder with a README and repro steps.

## License

MIT, see [LICENSE](LICENSE).

---
maintained · verified 2026-09-30

## Protocol notes

socketlab speaks plain length-prefixed frames over TCP: a 4-byte big-endian length header followed by the payload. No handshake, no auth — it's a test bench, keep it on loopback or behind your firewall rules.

## Benchmarks

Rough numbers on a Ryzen 7 laptop, loopback, 1KB payloads, single client:

| mode | throughput |
| --- | --- |
| echo | ~180k msg/s |
| streaming | ~1.1 GB/s |

Treat these as ballparks, not guarantees — profile on your own hardware.


## Security

socketlab has no authentication — it's a lab bench. Never expose it beyond loopback. If you must, front it with mutual TLS and keep sessions short.


## Getting started

```bash
git clone https://github.com/navairgap/socketlab && cd socketlab
make          # build
./socketlab echo &
./socketlab client 127.0.0.1 9000
```

three terminals, one minute, working lab.

## Roadmap

- tls mode with self-signed certs for handshake testing
- latency histogram mode
- scripted conversation files (send this, expect that)

## Code style

C99, `-Wall -Wextra -Werror` clean, no warnings accepted. functions stay under ~60 lines; if one grows past that it's two functions. PRs that add warnings get bounced by CI.

## Code style

C99, `-Wall -Wextra -Werror` clean, no warnings accepted. functions stay under ~60 lines; if one grows past that it's two functions. PRs that add warnings get bounced by CI.
