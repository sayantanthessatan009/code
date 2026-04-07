import argparse
import json
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs


class Handler(BaseHTTPRequestHandler):
    def _send(self, code, obj, content_type="application/json"):
        b = json.dumps(obj).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            self._send(200, {"endpoints": ["/encode", "/decode"], "methods": {"encode": "GET/POST", "decode": "GET/POST"}})
            return

        qs = parse_qs(parsed.query)
        data = qs.get("data", [None])[0]

        if parsed.path == "/encode":
            if data is None:
                self._send(400, {"error": "missing data parameter"})
            else:
                self._send(200, {"b64": base64.b64encode(data.encode()).decode()})
        elif parsed.path == "/decode":
            if data is None:
                self._send(400, {"error": "missing data parameter"})
            else:
                try:
                    text = base64.b64decode(data).decode(errors="replace")
                    self._send(200, {"text": text})
                except Exception as e:
                    self._send(400, {"error": str(e)})
        else:
            self._send(404, {"error": "not found"})

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b""
        try:
            payload = json.loads(raw.decode("utf-8")) if raw else {}
        except Exception:
            payload = {}
        data = payload.get("data")

        if parsed.path == "/encode":
            if data is None:
                self._send(400, {"error": "missing data in JSON body"})
            else:
                self._send(200, {"b64": base64.b64encode(data.encode()).decode()})
        elif parsed.path == "/decode":
            if data is None:
                self._send(400, {"error": "missing data in JSON body"})
            else:
                try:
                    text = base64.b64decode(data).decode(errors="replace")
                    self._send(200, {"text": text})
                except Exception as e:
                    self._send(400, {"error": str(e)})
        else:
            self._send(404, {"error": "not found"})


def main():
    parser = argparse.ArgumentParser(prog="b64-server", description="Simple Base64 HTTP server")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8000, type=int)
    args = parser.parse_args()

    addr = (args.host, args.port)
    print(f"Serving HTTP on http://{args.host}:{args.port}")
    httpd = HTTPServer(addr, Handler)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
