import unittest
import threading
import time
import http.client
import json

from http.server import HTTPServer

from base64_uv import server


class TestServerErrorAndBinary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = HTTPServer(("127.0.0.1", 0), server.Handler)
        cls.host, cls.port = cls.httpd.server_address
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
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

    def _post_raw(self, path, body_bytes, content_type="application/octet-stream"):
        conn = http.client.HTTPConnection(self.host, self.port, timeout=2)
        headers = {"Content-Type": content_type, "Content-Length": str(len(body_bytes))}
        conn.request("POST", path, body=body_bytes, headers=headers)
        resp = conn.getresponse()
        body = resp.read()
        conn.close()
        return resp.status, body

    def test_missing_params(self):
        status, body = self._get('/encode')
        self.assertEqual(status, 400)
        obj = json.loads(body)
        self.assertIn('error', obj)

        status, body = self._get('/decode')
        self.assertEqual(status, 400)
        obj = json.loads(body)
        self.assertIn('error', obj)

    def test_binary_payload_post(self):
        # send JSON body with binary-like base64
        status, body = self._post_raw('/decode', json.dumps({'data': 'AAECAw=='}).encode('utf-8'), content_type='application/json')
        self.assertEqual(status, 200)
        obj = json.loads(body)
        # decoded bytes include non-text; server decodes with errors='replace'
        self.assertIn('text', obj)


if __name__ == '__main__':
    unittest.main()
