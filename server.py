"""Servidor local do Rotina. Uso: python server.py  ->  abre http://localhost:8000
Serve os arquivos da pasta e guarda tudo em data/dados.json."""
import http.server, json, os, threading, webbrowser

DIR = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(DIR, "data", "dados.json")
PORTA = 8000


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=DIR, **k)

    def do_GET(self):
        if self.path.split("?")[0] == "/api/data":
            b = open(ARQ, "rb").read() if os.path.exists(ARQ) else b"{}"
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(b)))
            self.end_headers()
            self.wfile.write(b)
        else:
            super().do_GET()

    def do_POST(self):
        b = self.rfile.read(int(self.headers["Content-Length"]))
        try:
            json.loads(b)
        except ValueError:
            self.send_response(400)
            self.end_headers()
            return
        os.makedirs(os.path.dirname(ARQ), exist_ok=True)
        tmp = ARQ + ".tmp"
        with open(tmp, "wb") as f:
            f.write(json.dumps(json.loads(b), ensure_ascii=False, indent=2).encode("utf-8"))
        os.replace(tmp, ARQ)  # gravação atômica: nunca deixa o JSON pela metade
        self.send_response(204)
        self.end_headers()

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", PORTA), H)
    print(f"Rotina rodando em http://localhost:{PORTA}  (Ctrl+C para parar)")
    threading.Timer(0.8, lambda: webbrowser.open(f"http://localhost:{PORTA}")).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
