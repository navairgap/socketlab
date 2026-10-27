# lab safety

Bind test servers to loopback by default and require an explicit opt-in for other interfaces. Set connection, frame-size, and idle timeouts. Keep load tests bounded and clearly separate from production targets. Ensure each test closes sockets on success, failure, and cancellation. Use ephemeral ports in automated tests to reduce conflicts and avoid requiring privileged ports.
## Listener acceptance test

For each lab server, test the default bind address before adding any exercises: it must listen only on loopback, and a separate machine must not be able to reach it. A non-loopback bind must require an explicit option and show a clear warning before start. Automated tests should bind to port 0, assert the selected socket address, and close the server in a `finally`/cleanup path even when a client assertion fails.
## Listener acceptance test

For each lab server, test the default bind address before adding any exercises: it must listen only on loopback, and a separate machine must not be able to reach it. A non-loopback bind must require an explicit option and show a clear warning before start. Automated tests should bind to port 0, assert the selected socket address, and close the server in a cleanup path even when a client assertion fails.
