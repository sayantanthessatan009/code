import argparse
import sys
import base64


def encode(data: bytes) -> str:
    return base64.b64encode(data).decode("ascii")


def decode(data_str: str) -> bytes:
    return base64.b64decode(data_str)


def main():
    parser = argparse.ArgumentParser(prog="b64", description="Base64 encode/decode CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_enc = sub.add_parser("encode", help="Encode bytes/text to Base64")
    p_enc.add_argument("text", nargs="?", help="Text to encode; if omitted, read stdin bytes")

    p_dec = sub.add_parser("decode", help="Decode Base64 to bytes/text")
    p_dec.add_argument("text", nargs="?", help="Base64 string to decode; if omitted, read stdin")

    args = parser.parse_args()

    if args.cmd == "encode":
        if args.text is None:
            data = sys.stdin.buffer.read()
        else:
            data = args.text.encode()
        print(encode(data))

    elif args.cmd == "decode":
        if args.text is None:
            raw = sys.stdin.read().strip()
        else:
            raw = args.text
        out = decode(raw)
        try:
            # try to print as text if possible
            sys.stdout.buffer.write(out)
        except Exception:
            # fallback to printing repr
            print(out)


if __name__ == "__main__":
    main()
