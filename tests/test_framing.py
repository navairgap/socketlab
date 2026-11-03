import unittest

from socketlab.framing import (
    FrameDecoder, FrameTooLarge, TruncatedFrame, encode_frame,
)


class FrameDecoderTests(unittest.TestCase):
    def test_header_split_across_four_reads(self):
        decoder = FrameDecoder()
        frame = encode_frame(b"hello")
        self.assertEqual(decoder.feed(frame[:1]), [])
        self.assertEqual(decoder.feed(frame[1:2]), [])
        self.assertEqual(decoder.feed(frame[2:3]), [])
        self.assertEqual(decoder.feed(frame[3:4]), [])
        self.assertEqual(decoder.feed(frame[4:]), [b"hello"])
        decoder.finish()

    def test_payload_fragmentation(self):
        decoder = FrameDecoder()
        self.assertEqual(decoder.feed(b"\x00\x00\x00\x05he"), [])
        self.assertEqual(decoder.feed(b"l"), [])
        self.assertEqual(decoder.feed(b"lo"), [b"hello"])

    def test_multiple_frames_in_one_chunk_and_zero_length_frame(self):
        decoder = FrameDecoder()
        data = encode_frame(b"one") + encode_frame(b"") + encode_frame(b"two")
        self.assertEqual(decoder.feed(data), [b"one", b"", b"two"])
        decoder.finish()

    def test_eof_distinguishes_partial_header_and_payload(self):
        header = FrameDecoder()
        header.feed(b"\x00\x00")
        with self.assertRaises(TruncatedFrame) as caught:
            header.finish()
        self.assertEqual(caught.exception.phase, "header")

        payload = FrameDecoder()
        payload.feed(b"\x00\x00\x00\x04ab")
        with self.assertRaises(TruncatedFrame) as caught:
            payload.finish()
        self.assertEqual(caught.exception.phase, "payload")
        self.assertEqual((caught.exception.received, caught.exception.expected), (2, 4))

    def test_oversized_length_is_rejected_before_payload(self):
        decoder = FrameDecoder(max_frame_size=8)
        with self.assertRaises(FrameTooLarge):
            decoder.feed((9).to_bytes(4, "big"))
        self.assertEqual(decoder.buffered_bytes, 0)
        with self.assertRaises(ValueError):
            decoder.feed(b"")

    def test_encoder_enforces_limit(self):
        with self.assertRaises(FrameTooLarge):
            encode_frame(b"123", max_frame_size=2)


if __name__ == "__main__":
    unittest.main()
