from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import json
from scraper import scrape_with_browser
from chunker import split_to_chunks
from json_writer import save_knowledge_base

found_links = []
depth = 1

class ScraperHandler(BaseHTTPRequestHandler):

    # 🔁 Ответ на предварительные OPTIONS-запросы
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        global found_links, depth

        if self.path.startswith('/start'):
            params = urlparse.parse_qs(urlparse.urlparse(self.path).query)
            url = params.get("url", [""])[0]
            depth = int(params.get("depth", ["1"])[0])

            text, links = scrape_with_browser(url)

            found_links.clear()
            found_links.extend(links)

            print(f"Найдено ссылок: {len(found_links)}")
            for link in found_links:
                print(link)

            with open("links_buffer.json", "w") as f:
                json.dump(found_links, f)

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"Started")

        elif self.path.startswith("/links"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps(found_links).encode())

    def do_POST(self):
        if self.path == "/continue":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            selected_links = json.loads(post_data).get("links", [])

            knowledge = []
            for url in selected_links:
                text, _ = scrape_with_browser(url)
                chunks = split_to_chunks(text)
                knowledge.append({"url": url, "chunks": chunks})
                print(f"[✔] Обработано: {url} — {len(chunks)} блоков")

            save_knowledge_base(knowledge)

            self.send_response(200)
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(b"OK")

def run_server():
    server = HTTPServer(('0.0.0.0', 8000), ScraperHandler)
    print("Server started at http://localhost:8000")
    server.serve_forever()

if __name__ == "__main__":
    run_server()
