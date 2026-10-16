#!/usr/bin/env python3
"""
proxy.py — Simple GraphDB CORS Proxy
Serves static files AND proxies /graphdb/* requests to GraphDB
Eliminates browser CORS issues entirely.

Usage:
    python3 proxy.py

Then open the KE Workbench: http://localhost:3000/
"""

from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
import socket
import threading
import webbrowser
import urllib.request
import urllib.error
import os

# Explicitly use 127.0.0.1 to avoid macOS IPv6 (::1) lookup mismatches
GRAPHDB_URL = os.environ.get("GRAPHDB_URL", "http://127.0.0.1:7200")
PORT = int(os.environ.get("PORT", "3000"))
# Listen on this machine only (IPv4 and IPv6 localhost); set HOST=0.0.0.0 to share
# the workbench on your network.
HOST = os.environ.get("HOST", "localhost")

class ProxyHandler(SimpleHTTPRequestHandler):

    def end_headers(self):
        # Workbench pages must never come from the browser cache, otherwise an
        # updated tool keeps showing its old version until a hard reload.
        if not self.path.startswith('/graphdb/'):
            self.send_header('Cache-Control', 'no-store, must-revalidate')
            self.send_header('Expires', '0')
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path.startswith('/graphdb/'):
            self._proxy_request('GET')
        elif self.path.startswith('/api/ingest/'):
            self._ingest('GET')
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith('/graphdb/'):
            self._proxy_request('POST')
        elif self.path.startswith('/api/ingest/'):
            self._ingest('POST')
        else:
            super().do_POST()

    def _ingest(self, method):
        # Ingestion page endpoints (ingest/ingest_api.py). Imported on first use, so a
        # problem there never stops the rest of the workbench from being served.
        try:
            import importlib, sys as _sys
            here = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ingest')
            if here not in _sys.path:
                _sys.path.insert(0, here)
            api = importlib.import_module('ingest_api')
            # Pick up updated ingestion code without restarting the server: reload when
            # ke_ingest.py or ingest_api.py changed on disk since they were imported.
            stamp = tuple(os.path.getmtime(os.path.join(here, f)) for f in ('ke_ingest.py', 'ingest_api.py'))
            if getattr(ProxyHandler, '_ingest_stamp', None) not in (None, stamp):
                importlib.reload(importlib.import_module('ke_ingest'))
                api = importlib.reload(api)
                print('  ingest: reloaded updated ingestion code')
            ProxyHandler._ingest_stamp = stamp
        except Exception as e:
            body = ('{"ok":false,"error":"Ingestion module failed to load: %s"}' % str(e).replace('"', "'")).encode()
            self.send_response(500); self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)
            return
        api.handle(self, method, GRAPHDB_URL)

    def do_PUT(self):
        if self.path.startswith('/graphdb/'):
            self._proxy_request('PUT')
        else:
            self.send_error(405)

    def do_DELETE(self):
        if self.path.startswith('/graphdb/'):
            self._proxy_request('DELETE')
        else:
            self.send_error(405)

    def do_HEAD(self):
        if self.path.startswith('/graphdb/'):
            self._proxy_request('HEAD')
        else:
            super().do_HEAD()

    def _proxy_request(self, method):
        # Strip /graphdb prefix and forward to GraphDB
        target_path = self.path[len('/graphdb'):]
        target_url = GRAPHDB_URL + target_path

        # Read request body if present
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length) if content_length > 0 else None

        req = urllib.request.Request(target_url, data=body, method=method)

        # Forward all relevant request headers (including GraphDB repository selectors)
        hop_by_hop = {'host', 'connection', 'keep-alive', 'transfer-encoding'}
        for header, val in self.headers.items():
            if header.lower() not in hop_by_hop:
                req.add_header(header, val)

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                response_body = b"" if method == 'HEAD' else resp.read()

                # Rewrite GraphDB's internal URIs so the frontend routes back through the proxy
                content_type = resp.headers.get('Content-Type', '')
                if response_body and ('json' in content_type or 'text' in content_type):
                    host_header = self.headers.get('Host', f'localhost:{PORT}')
                    proxy_base = f"http://{host_header}/graphdb".encode()
                    
                    # Replace both 127.0.0.1:7200 and localhost:7200 in the returned body
                    response_body = response_body.replace(b"http://127.0.0.1:7200", proxy_base)
                    response_body = response_body.replace(b"http://localhost:7200", proxy_base)

                self.send_response(resp.status)
                self._cors_headers()

                # Forward upstream headers
                for header, val in resp.headers.items():
                    if header.lower() not in ('transfer-encoding', 'connection', 'access-control-allow-origin', 'content-length'):
                        self.send_header(header, val)

                if method != 'HEAD':
                    self.send_header('Content-Length', str(len(response_body)))

                self.end_headers()

                if method != 'HEAD':
                    self.wfile.write(response_body)

        except urllib.error.HTTPError as e:
            err_body = b"" if method == 'HEAD' else e.read()
            self.send_response(e.code)
            self._cors_headers()
            self.send_header('Content-Type', e.headers.get('Content-Type', 'text/plain'))
            self.send_header('Content-Length', str(len(err_body)))
            self.end_headers()
            if method != 'HEAD':
                self.wfile.write(err_body)

        except Exception as e:
            msg = str(e).encode()
            self.send_response(502)
            self._cors_headers()
            self.send_header('Content-Type', 'text/plain')
            self.send_header('Content-Length', str(len(msg)))
            self.end_headers()
            if method != 'HEAD':
                self.wfile.write(msg)

    def _cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type,Accept,Authorization,X-GraphDB-Repository,X-Requested-With')

    def log_message(self, format, *args):
        first = str(args[0]) if args else ''
        if 'favicon' not in first:
            super().log_message(format, *args)


class V6Server(ThreadingHTTPServer):
    address_family = socket.AF_INET6


def make_servers():
    """Bind every address HOST stands for. 'localhost' = 127.0.0.1 and ::1, so the
    browser reaches the workbench whichever one it resolves localhost to."""
    hosts = ['127.0.0.1', '::1'] if HOST == 'localhost' else [HOST]
    servers, errors = [], []
    for h in hosts:
        cls = V6Server if ':' in h else ThreadingHTTPServer
        try:
            servers.append(cls((h, PORT), ProxyHandler))
        except OSError as e:
            errors.append((h, e))
    return servers, errors


if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    servers, errors = make_servers()
    in_use = [h for h, e in errors if e.errno in (48, 98)]
    if in_use or not servers:
        for s_ in servers:
            s_.server_close()
        if in_use:
            print(f"✗ Port {PORT} is already in use — probably an older proxy.py.")
            print(f"  Stop it with:  lsof -ti tcp:{PORT} | xargs kill")
            print(f"  or run this one on another port:  PORT=3001 python3 proxy.py")
        else:
            for h, e in errors:
                print(f"✗ Could not listen on {h}:{PORT}: {e}")
        raise SystemExit(1)
    print(f"✓ Proxy server running at http://localhost:{PORT}/")
    print(f"✓ Listening on {', '.join(str(s_.server_address[0]) for s_ in servers)}")
    print(f"✓ Forwarding /graphdb/* → {GRAPHDB_URL}")
    print(f"✓ Ingestion API at /api/ingest/ (ingest/ke_ingest.py)")
    print(f"✓ Serving files from {os.getcwd()}")
    print(f"  Press Ctrl+C to stop\n")
    for s_ in servers[1:]:
        threading.Thread(target=s_.serve_forever, daemon=True).start()
    if os.environ.get("OPEN") == "1":
        threading.Timer(1.0, lambda: webbrowser.open(f"http://localhost:{PORT}/")).start()
    try:
        servers[0].serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
