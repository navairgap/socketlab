# TCP framing lab exercises

TCP provides an ordered byte stream, not application message boundaries. These exercises define reproducible tests for a future loopback-only SocketLab harness.

## Length-prefixed frame proposal

A frame consists of a 4-byte unsigned big-endian payload length followed by exactly that many payload bytes. The maximum payload is configured by the server and defaults to a conservative limit such as 64 KiB.

## Required behaviors

- A read may return part of the header, part of the payload, or bytes spanning multiple frames.
- The parser must accumulate bytes until a complete frame is available.
- Reject a declared length above the configured maximum before allocating the payload buffer.
- Treat EOF during a header or payload as an incomplete frame and report it distinctly from a clean close.
- Bound per-connection buffering and idle time so slow clients cannot grow memory without limit.
- Do not assume a single write is delivered as a single read by the peer.

## Exercises

1. Split the four-byte header across four writes.
2. Split a payload across multiple writes.
3. Send two frames in one write and verify both are decoded.
4. Disconnect halfway through a frame.
5. Declare a payload above the maximum.
6. Send a complete frame followed by a partial next frame.

## Safety

Bind to loopback by default. Any non-loopback listener should require an explicit option and clear warning. Tests must use local sockets and close all resources deterministically.

## Error reporting contract

Frame errors should identify the connection, parser phase, and byte offset without echoing attacker-controlled payload bytes. Distinguish a clean close between frames from EOF during a header or payload. Once a framing violation occurs, close that connection and release its buffered data; do not attempt to resynchronize by scanning arbitrary payload bytes for a plausible length prefix. Keep diagnostics bounded and deterministic for tests.

## Deadline ownership

Use separate, documented deadlines for completing a frame header, completing its payload, and remaining idle between frames. Reset the appropriate deadline only when bytes relevant to that phase arrive; unrelated activity on another connection must not extend it. A timeout should release that connection's buffered bytes and leave the listener available to other clients. Tests should use an injected clock or short deterministic deadlines, not long sleeps.
