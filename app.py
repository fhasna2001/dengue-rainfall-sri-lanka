"""Run the local dashboard: python app.py"""
import argparse
import csv
import io
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from src.dashboard_data import ROOT, build_data


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlsplit(self.path).path
        try:
            if path == '/api/data':
                body, kind = json.dumps(build_data(), allow_nan=False).encode(), 'application/json'
            elif path == '/download.csv':
                rows = build_data()['rows']
                output = io.StringIO(newline='')
                writer = csv.DictWriter(output, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
                body, kind = output.getvalue().encode(), 'text/csv'
            elif path in ('/', '/index.html'):
                body, kind = (ROOT / 'web/index.html').read_bytes(), 'text/html'
            else:
                self.send_error(404)
                return
            self.send_response(200)
            self.send_header('Content-Type', kind + '; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            if path == '/download.csv':
                self.send_header('Content-Disposition', 'attachment; filename="dengue_weather_weekly.csv"')
            self.end_headers()
            self.wfile.write(body)
        except (OSError, ValueError, KeyError) as error:
            self.send_error(500, 'Could not load local data: ' + str(error))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8000)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'Dashboard running at http://localhost:{args.port} (Ctrl+C to stop)', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
