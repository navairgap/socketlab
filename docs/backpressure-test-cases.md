# TCP backpressure test cases (proposed)

Backpressure tests should verify that a slow peer cannot cause unbounded memory growth or stall unrelated clients. All scenarios use loopback sockets and bounded payloads.

## Required scenarios

- A client sends frames faster than the server consumer can process them.
- A client stops reading while the server writes responses.
- Several slow clients share a listener while one fast client continues to exchange frames.
- The peer pauses during a partial frame and resumes before the deadline.
- The peer remains idle beyond the configured deadline.
- A write is only partially accepted by the local socket and the sender must continue from the remaining bytes.
- The peer disconnects while queued output remains.

## Invariants

Define a per-connection output-buffer high-water mark and a global connection/resource cap. When a limit is reached, apply a documented policy such as pausing reads, rejecting additional work, or closing the slow connection. Do not silently drop bytes from an ordered stream and continue as if delivery succeeded.

A slow connection must not extend another connection's deadline or consume its buffer allowance. On close, cancellation, or protocol failure, release queued data and unregister the connection.

## Observability

Expose bounded counters for active connections, bytes queued, backpressure events, and disconnect reasons. Do not label metrics with peer-provided arbitrary strings or full payload values.

## Test constraints

Use ephemeral ports, finite deadlines, small buffers, and explicit cleanup. Tests should avoid public destinations and high-volume load generation. Verify the listener remains responsive after a slow client is closed.