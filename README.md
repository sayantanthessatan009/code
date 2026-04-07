# base64_uv

Minimal Base64 encoder/decoder providing:
- `b64` CLI: `encode` / `decode`
- `b64-server` HTTP server with `/encode` and `/decode` endpoints

This project has no external dependencies and works with the Python standard library.

Using `uv` locally
- Use your usual `uv` workflow to create/activate a local environment.
- Inside that environment, install the package locally:

```bash
python -m pip install -e .
```

Then run the CLI:

```bash
b64 encode "hello"
b64 decode aGVsbG8=
```

Run the HTTP server (default port 8000):

```bash
b64-server --host 127.0.0.1 --port 8000
```

HTTP usage examples
- GET encode: `http://127.0.0.1:8000/encode?data=hello`
- POST decode: `POST /decode` with JSON body `{ "data": "aGVsbG8=" }`

Long description
----------------
This project implements simple Base64 encoding and decoding using only the Python standard library.
It provides a small CLI for quick tasks and a minimal HTTP server suitable for local use or lightweight automation.

Changelog
---------
- 0.1.1: Packaging metadata and extra tests; linting + CI steps added.
- 0.1.0: Initial implementation with CLI and server.

