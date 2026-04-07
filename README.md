# base64_uv

Minimal Base64 encoder/decoder (CLI + tiny HTTP server) using only the Python standard library.

Features
- `b64` CLI: `encode` / `decode`
- `b64-server` HTTP server with `/encode` and `/decode` endpoints

Install (editable/development)
1. Create or activate your Python environment (your `uv` workflow).
2. From the project root:

```bash
python -m pip install -e src
```

CLI usage
- Encode text to Base64:

```bash
b64 encode "hello"
```

- Decode Base64 (prints raw bytes to stdout):

```bash
b64 decode aGVsbG8=
```

Server usage

```bash
b64-server --host 127.0.0.1 --port 8000
```

HTTP examples
- GET encode: `http://127.0.0.1:8000/encode?data=hello`
- GET decode: `http://127.0.0.1:8000/decode?data=aGVsbG8=`
- POST encode: `POST /encode` with JSON body `{ "data": "hello" }`
- POST decode: `POST /decode` with JSON body `{ "data": "aGVsbG8=" }`

Testing
- Run the unit tests from the repository root:

```bash
$env:PYTHONPATH='src'; python -m unittest discover -v tests
```

Contributing
- Open an issue or pull request. CI runs tests and basic lint checks.

License
- MIT

Changelog
- 0.1.1: Packaging metadata, extra tests, and CI improvements.
- 0.1.0: Initial implementation with CLI and server.

