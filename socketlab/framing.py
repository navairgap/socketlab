"""Incremental length-prefixed TCP frame decoder.

Frames use a four-byte unsigned big-endian payload length. The decoder stores
only the unfinished header or current payload, never an entire input chunk.
"""
from __future__ import annotations


HEADER_SIZE = 4
DEFAULT_MAX_FRAME_SIZE = 64 * 1024


class FrameProtocolError(ValueError):
    """Base class for invalid or incomplete frames."""


class FrameTooLarge(FrameProtocolError):
    pass


class TruncatedFrame(FrameProtocolError):
    def __init__(self, phase: str, received: int, expected: int) -> None:
        self.phase = phase
        self.received = received
        self.expected = expected
        super().__init__(
            f"EOF during {phase}: received {received} of {expected} bytes"
        )


def encode_frame(payload: bytes, max_frame_size: int = DEFAULT_MAX_FRAME_SIZE) -> bytes:
    if isinstance(max_frame_size, bool) or not isinstance(max_frame_size, int) or max_frame_size < 0:
        raise ValueError("max_frame_size must be a non-negative integer")
    if not isinstance(payload, (bytes, bytearray, memoryview)):
        raise TypeError("payload must be bytes-like")
    data = bytes(payload)
    if len(data) > max_frame_size:
        raise FrameTooLarge(f"frame length {len(data)} exceeds limit {max_frame_size}")
    return len(data).to_bytes(HEADER_SIZE, "big") + data


class FrameDecoder:
    """Decode arbitrary TCP chunks into complete payloads."""

    def __init__(self, max_frame_size: int = DEFAULT_MAX_FRAME_SIZE) -> None:
        if isinstance(max_frame_size, bool) or not isinstance(max_frame_size, int) or max_frame_size < 0:
            raise ValueError("max_frame_size must be a non-negative integer")
        self.max_frame_size = max_frame_size
        self._buffer = bytearray()
        self._expected_payload: int | None = None
        self._failed = False
        self._finished = False

    @property
    def buffered_bytes(self) -> int:
        return len(self._buffer)

    def feed(self, data: bytes | bytearray | memoryview) -> list[bytes]:
        if self._failed:
            raise FrameProtocolError("decoder is unusable after a framing error")
        if self._finished:
            raise FrameProtocolError("decoder has already been finished")
        if not isinstance(data, (bytes, bytearray, memoryview)):
            raise TypeError("data must be bytes-like")

        view = memoryview(data).cast("B")
        position = 0
        frames: list[bytes] = []

        while position < len(view):
            if self._expected_payload is None:
                needed = HEADER_SIZE - len(self._buffer)
                take = min(needed, len(view) - position)
                self._buffer.extend(view[position : position + take])
                position += take
                if len(self._buffer) < HEADER_SIZE:
                    break

                declared = int.from_bytes(self._buffer, "big")
                self._buffer.clear()
                if declared > self.max_frame_size:
                    self._failed = True
                    raise FrameTooLarge(
                        f"declared frame length {declared} exceeds limit {self.max_frame_size}"
                    )
                self._expected_payload = declared
                if declared == 0:
                    frames.append(b"")
                    self._expected_payload = None
                    continue

            needed = self._expected_payload - len(self._buffer)
            take = min(needed, len(view) - position)
            self._buffer.extend(view[position : position + take])
            position += take
            if len(self._buffer) == self._expected_payload:
                frames.append(bytes(self._buffer))
                self._buffer.clear()
                self._expected_payload = None

        return frames

    def finish(self) -> None:
        """Mark EOF; raise when a header or payload is incomplete."""
        if self._failed:
            raise FrameProtocolError("decoder is unusable after a framing error")
        if self._finished:
            return
        if self._expected_payload is None and not self._buffer:
            self._finished = True
            return
        self._failed = True
        if self._expected_payload is None:
            raise TruncatedFrame("header", len(self._buffer), HEADER_SIZE)
        raise TruncatedFrame("payload", len(self._buffer), self._expected_payload)
