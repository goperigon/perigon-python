#!/usr/bin/env python3
"""
Perigon SDK webhook signature example.

Verifies the raw request body against the perigon-signature header.

Before running: set PERIGON_WEBHOOK_SECRET
Run: python examples/webhooks.py
"""

import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from perigon import WEBHOOK_HEADER, SignatureVerificationError, Webhooks

secret = os.environ.get("PERIGON_WEBHOOK_SECRET", "")
webhooks = Webhooks()


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        if self.path != "/webhook":
            self.send_error(404)
            return

        length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(length)
        signature = self.headers.get(WEBHOOK_HEADER)
        try:
            webhooks.construct_event(body, signature, secret)
        except SignatureVerificationError as error:
            print(error)
            self.send_response(400)
            self.end_headers()
            return

        self.send_response(200)
        self.end_headers()


def main() -> None:
    port = 3000
    server = ThreadingHTTPServer(("127.0.0.1", port), WebhookHandler)
    print(f"Example app listening on port {port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
