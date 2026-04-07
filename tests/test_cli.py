import unittest

from base64_uv import cli


class TestBase64CLI(unittest.TestCase):
    def test_encode_decode_bytes(self):
        data = b"hello world"
        b64 = cli.encode(data)
        self.assertEqual(b64, "aGVsbG8gd29ybGQ=")
        out = cli.decode(b64)
        self.assertEqual(out, data)

    def test_encode_decode_text_unicode(self):
        text = "こんにちは"
        b64 = cli.encode(text.encode("utf-8"))
        self.assertEqual(cli.decode(b64), text.encode("utf-8"))

    def test_empty(self):
        self.assertEqual(cli.encode(b""), "")
        self.assertEqual(cli.decode(""), b"")


if __name__ == "__main__":
    unittest.main()
