#!/usr/bin/env python3
from http.server import CGIHTTPRequestHandler, HTTPServer
import sys, ast

class UTF8CGIHandler(CGIHTTPRequestHandler):
    def log_message(self, format, *args):
        msg = format % args

        if msg.startswith("b'") or msg.startswith('b"'):
            try:
                raw = ast.literal_eval(msg)
                msg = raw.decode("UTF-8", "replace")
            except Exception:
                pass

        sys.stderr.write(f"{msg}\n")


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", 8000), UTF8CGIHandler).serve_forever()
