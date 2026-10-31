# Socket lifecycle and cleanup contract (proposed)

A SocketLab connection should have a small, explicit lifecycle so tests can distinguish a clean close from an interrupted protocol exchange.

## Suggested states

- **Accepted:** the listener created a connection and assigned a local identifier.
- **Reading:** the parser is collecting a frame header or payload.
- **Writing:** a complete response is queued or being sent.
- **Closing:** no new application work is accepted; bounded pending output may be flushed according to policy.
- **Closed:** the socket, timers, buffers, and connection registry entry are released.

A transition to Closed should be idempotent. Repeated close notifications or cancellation signals must not double-release resources or recreate a connection entry.

## EOF and errors

EOF between complete frames is a clean peer shutdown. EOF partway through a header or payload is a truncated frame. A framing violation should close only the offending connection unless the listener itself has failed.

Distinguish timeout, reset, local cancellation, and graceful close in diagnostic categories. Avoid echoing untrusted payload bytes into logs.

## Cleanup ownership

Use one owner for each socket and its associated read/write tasks. Closing a connection should cancel outstanding operations, stop per-connection timers, release buffered data, and remove the connection from metrics/state. The listener should continue accepting unrelated clients.

## Regression matrix

Test normal request/response, peer half-close, abrupt reset, timeout during header, timeout during payload, cancellation during a write, repeated close, server shutdown with active clients, and a listener that continues serving a new client after another connection fails. Use local ephemeral ports and cleanup hooks rather than external endpoints.