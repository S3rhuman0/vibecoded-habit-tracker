"""Servidor local do Rotina. Uso: python server.py  ->  abre http://localhost:8000
Serve os arquivos da pasta, guarda tudo em data/dados.json e os PDFs em livros/."""
import http.server, json, os, re, threading, webbrowser
from urllib.parse import urlparse, parse_qs

DIR = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(DIR, "data", "dados.json")
LIV = os.path.join(DIR, "livros")
LIMITE = 500 * 1024 * 1024  # 500 MB por PDF
PORTA = 8000


class Srv(http.server.ThreadingHTTPServer):
    # No Windows, reuse_address deixa dois servidores dividirem a mesma porta
    allow_reuse_address = os.name != "nt"


class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=DIR, **k)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")  # nunca mostrar versão antiga
        super().end_headers()

    def _resp(self, code=204, corpo=None):
        self.send_response(code)
        self.send_header("Content-Length", str(len(corpo)) if corpo is not None else "0")
        if corpo is not None:
            self.send_header("Content-Type", "application/json")
        self.end_headers()
        if corpo is not None:
            self.wfile.write(corpo)

    def _pdf(self):
        """Nome de PDF vindo de ?name=, sem pastas e sem caracteres proibidos."""
        q = parse_qs(urlparse(self.path).query).get("name", [""])[0]
        n = re.sub(r'[<>:"|?*\x00-\x1f]', "_", os.path.basename(q.replace("\\", "/"))).strip()
        return n if n.lower().endswith(".pdf") and len(n) > 4 else None

    def do_GET(self):
        if urlparse(self.path).path == "/api/data":
            self._resp(200, open(ARQ, "rb").read() if os.path.exists(ARQ) else b"{}")
        else:
            super().do_GET()

    def do_POST(self):
        p = urlparse(self.path).path
        n = int(self.headers.get("Content-Length", 0))
        if p == "/api/livros":
            nome = self._pdf()
            if not nome or n > LIMITE:
                return self._resp(400)
            os.makedirs(LIV, exist_ok=True)
            base, ext = os.path.splitext(nome)
            k = 1
            while os.path.exists(os.path.join(LIV, nome)):  # nunca sobrescreve outro PDF
                k += 1
                nome = f"{base}-{k}{ext}"
            tmp = os.path.join(LIV, nome + ".tmp")
            with open(tmp, "wb") as f:
                while n > 0:
                    ch = self.rfile.read(min(n, 1 << 20))
                    if not ch:
                        break
                    f.write(ch)
                    n -= len(ch)
            os.replace(tmp, os.path.join(LIV, nome))
            return self._resp(200, json.dumps({"name": nome}, ensure_ascii=False).encode("utf-8"))
        b = self.rfile.read(n)
        try:
            dados = json.loads(b)
        except ValueError:
            return self._resp(400)
        os.makedirs(os.path.dirname(ARQ), exist_ok=True)
        tmp = ARQ + ".tmp"
        with open(tmp, "wb") as f:
            f.write(json.dumps(dados, ensure_ascii=False, indent=2).encode("utf-8"))
        os.replace(tmp, ARQ)  # gravação atômica: nunca deixa o JSON pela metade
        self._resp(204)

    def do_DELETE(self):
        nome = self._pdf() if urlparse(self.path).path == "/api/livros" else None
        f = os.path.join(LIV, nome) if nome else None
        if f and os.path.isfile(f):
            os.remove(f)
            return self._resp(204)
        self._resp(404)

    def log_message(self, *a):
        pass


if __name__ == "__main__":
    try:
        srv = Srv(("127.0.0.1", PORTA), H)
    except OSError:
        print(f"A porta {PORTA} já está em uso, provavelmente por outro server.py aberto.")
        print("Feche o outro servidor ou mude PORTA no topo deste arquivo.")
        raise SystemExit(1)
    print(f"Servindo a pasta: {DIR}")
    print(f"Rotina rodando em http://localhost:{PORTA}  (Ctrl+C para parar)")
    threading.Timer(0.8, lambda: webbrowser.open(f"http://localhost:{PORTA}")).start()
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
