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
