import unittest
import threading
import json
import time
import http.client

from http.server import HTTPServer

from base64_uv import server


class TestServerEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = HTTPServer(("127.0.0.1", 0), server.Handler)
        cls.host, cls.port = cls.httpd.server_address
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        # give server a moment to start
        time.sleep(0.05)

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.thread.join(timeout=1)

    def _get(self, path):
        conn = http.client.HTTPConnection(self.host, self.port, timeout=2)
        conn.request("GET", path)
        resp = conn.getresponse()
        body = resp.read()
        conn.close()
        return resp.status, body

    def _post_json(self, path, obj):
        conn = http.client.HTTPConnection(self.host, self.port, timeout=2)
        b = json.dumps(obj).encode("utf-8")
        headers = {"Content-Type": "application/json", "Content-Length": str(len(b))}
        conn.request("POST", path, body=b, headers=headers)
        resp = conn.getresponse()
        body = resp.read()
        conn.close()
        return resp.status, body

    def test_get_encode_decode(self):
        status, body = self._get('/encode?data=hello')
        self.assertEqual(status, 200)
        obj = json.loads(body)
        self.assertEqual(obj.get('b64'), 'aGVsbG8=')

        status, body = self._get('/decode?data=aGVsbG8=')
        self.assertEqual(status, 200)
        obj = json.loads(body)
        self.assertEqual(obj.get('text'), 'hello')

    def test_post_encode_decode(self):
        status, body = self._post_json('/encode', {'data': 'hi'})
        self.assertEqual(status, 200)
        obj = json.loads(body)
        self.assertEqual(obj.get('b64'), 'aGk=')

        status, body = self._post_json('/decode', {'data': 'aGk='})
        self.assertEqual(status, 200)
        obj = json.loads(body)
        self.assertEqual(obj.get('text'), 'hi')

    def test_root(self):
        status, body = self._get('/')
        self.assertEqual(status, 200)
        obj = json.loads(body)
        self.assertIn('/encode', obj.get('endpoints', []))


if __name__ == '__main__':
    unittest.main()
