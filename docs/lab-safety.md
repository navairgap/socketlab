# lab safety

Bind test servers to loopback by default and require an explicit opt-in for other interfaces. Set connection, frame-size, and idle timeouts. Keep load tests bounded and clearly separate from production targets. Ensure each test closes sockets on success, failure, and cancellation. Use ephemeral ports in automated tests to reduce conflicts and avoid requiring privileged ports.
