# tcp framing exercises

Exercises should cover a header sent byte-by-byte, payload split across writes, multiple frames in one write, disconnect during a partial header, disconnect during a partial payload, oversized declared lengths, slow readers, and excess connections. Bind to loopback by default, set short timeouts, and cap payload sizes. Each scenario needs a deterministic assertion rather than relying on printed output.
