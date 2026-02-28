"""
OAAI Model-Radar — Backend Server
========================================
A zero-dependency HTTP server for managing LLM API configurations.

Features:
  - Multi-profile config management (create / read / update / delete)
  - Concurrent API connectivity testing
  - Static file serving for the React frontend (index.html)

Usage:
  python server.py [PORT]       # default port: 5000
  python server.py 8080

Requirements:
  Python 3.6+ (standard library only — no pip install needed)
"""

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, unquote
import json
import os
import ssl
import urllib.request
import urllib.error
import threading
import sys
import webbrowser

# ─── 路径配置 ────────────────────────────────────────────────────────────────
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CONFIG_DIR = os.path.join(BASE_DIR, "configs")
INDEX_FILE = os.path.join(BASE_DIR, "index.html")
DEFAULT_CONFIG = "默认配置"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5000

# ─── 初始化 configs 目录 ──────────────────────────────────────────────────────
os.makedirs(CONFIG_DIR, exist_ok=True)
default_path = os.path.join(CONFIG_DIR, DEFAULT_CONFIG + ".json")
if not os.path.exists(default_path):
    old_source = os.path.join(BASE_DIR, "openclaw_remote.json")
    template = {"models": {"providers": {}}, "agents": {"defaults": {"model": {"primary": ""}}}}
    if os.path.exists(old_source):
        try:
            with open(old_source, 'r', encoding='utf-8') as f:
                template = json.load(f)
        except Exception:
            pass
    with open(default_path, 'w', encoding='utf-8') as f:
        json.dump(template, f, indent=2, ensure_ascii=False)

# ─── 静态文件 MIME 类型 ────────────────────────────────────────────────────────
MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.js':   'application/javascript',
    '.css':  'text/css',
    '.svg':  'image/svg+xml',
    '.ico':  'image/x-icon',
    '.json': 'application/json',
    '.png':  'image/png',
    '.woff': 'font/woff',
    '.woff2':'font/woff2',
    '.map':  'application/json',
}

# ─── 工具函数 ──────────────────────────────────────────────────────────────────
def get_config_path(name):
    if not name:
        name = DEFAULT_CONFIG
    name = os.path.basename(name)
    if not name.endswith('.json'):
        name += '.json'
    return os.path.join(CONFIG_DIR, name)


def test_single_api(provider_cfg):
    """Test connectivity for a single provider API.

    Args:
        provider_cfg (dict): Must contain 'baseUrl', 'apiKey', and 'model' keys.

    Returns:
        dict: {"status": "success"|"error", "message": str}
    """
    url = f"{provider_cfg['baseUrl']}/chat/completions"
    api_key = provider_cfg['apiKey']
    # Mask API key in any error logs for security
    masked_key = api_key[:8] + '...' + api_key[-4:] if len(api_key) > 12 else '***'
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    body = {
        "model": provider_cfg["model"],
        "messages": [{"role": "user", "content": "Hi"}],
        "max_tokens": 10
    }
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=15, context=ctx):
            return {"status": "success", "message": "连接成功"}
    except urllib.error.HTTPError as e:
        msg = e.read().decode('utf-8', errors='ignore')
        return {"status": "error", "message": f"HTTP {e.code}: {msg}"}
    except Exception as e:
        err = str(e)
        if "timed out" in err:
            err = "连接超时（15s）"
        return {"status": "error", "message": err}


# ─── HTTP 请求处理器 ────────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass  # 静默日志，不打印每次请求

    # ── 响应工具 ───────────────────────────────────────────────────────────────
    def _cors_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(status)
        self._cors_headers()
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_file(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        mime = MIME_TYPES.get(ext, 'application/octet-stream')
        try:
            with open(file_path, 'rb') as f:
                body = f.read()
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Content-Length', str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()

    def read_body(self):
        length = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(length)) if length else {}

    def parse_path(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        return parsed.path, {k: v[0] for k, v in qs.items()}

    # ── OPTIONS（跨域预检）──────────────────────────────────────────────────────
    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.end_headers()

    # ── GET ───────────────────────────────────────────────────────────────────
    def do_GET(self):
        path, query = self.parse_path()

        # 1. 配置列表
        if path == '/api/config/list':
            files = [f[:-5] for f in os.listdir(CONFIG_DIR) if f.endswith('.json')]
            return self.send_json(files)

        # 2. 读取完整配置
        if path == '/api/config':
            cfg = get_config_path(query.get('config'))
            if os.path.exists(cfg):
                with open(cfg, 'r', encoding='utf-8') as f:
                    return self.send_json(json.load(f))
            return self.send_json({"error": "Config not found"}, 404)

        # 3. 只读 providers
        if path == '/api/providers':
            cfg = get_config_path(query.get('config'))
            if not os.path.exists(cfg):
                return self.send_json({})
            with open(cfg, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return self.send_json(data.get('models', {}).get('providers', {}))

        # 4. 静态文件服务 (提供根目录下的 index.html)
        if path == '/' or path == '/index.html':
            if os.path.exists(INDEX_FILE):
                return self.serve_file(INDEX_FILE)

        # 5. SPA fallback → index.html
        if os.path.exists(INDEX_FILE):
            return self.serve_file(INDEX_FILE)

        # 6. index.html 不存在时给出提示
        msg = (
            b"<h2>OAAI Model-Radar API is running.</h2>"
            b"<p>index.html not found in root directory!</p>"
        )
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(msg)

    # ── POST ──────────────────────────────────────────────────────────────────
    def do_POST(self):
        path, query = self.parse_path()
        data = self.read_body()

        # 保存完整配置
        if path == '/api/config':
            cfg = get_config_path(query.get('config'))
            with open(cfg, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            return self.send_json({"status": "success"})

        # 新增/更新单个 provider
        if path.startswith('/api/providers/'):
            name = unquote(path[len('/api/providers/'):])
            cfg = get_config_path(query.get('config'))
            if os.path.exists(cfg):
                with open(cfg, 'r', encoding='utf-8') as f:
                    config = json.load(f)
            else:
                config = {"models": {"providers": {}}}
            config.setdefault('models', {}).setdefault('providers', {})[name] = data
            with open(cfg, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return self.send_json({"status": "success"})

        # 批量测试所有 provider（多线程并发）
        if path == '/api/test':
            cfg = get_config_path(query.get('config'))
            if not os.path.exists(cfg):
                return self.send_json({"error": "Config not found"}, 404)
            with open(cfg, 'r', encoding='utf-8') as f:
                config = json.load(f)
            providers = config.get('models', {}).get('providers', {})
            results = {}
            lock = threading.Lock()

            def run(pname, pcfg):
                model = pcfg.get('models', [{}])[0].get('id', 'default')
                r = test_single_api({"baseUrl": pcfg['baseUrl'], "apiKey": pcfg['apiKey'], "model": model})
                with lock:
                    results[pname] = r

            threads = [threading.Thread(target=run, args=(n, c)) for n, c in providers.items()]
            for t in threads: t.start()
            for t in threads: t.join()
            return self.send_json(results)

        # 测试单个 provider
        if path.startswith('/api/test/'):
            name = unquote(path[len('/api/test/'):])
            model = data.get('models', [{}])[0].get('id', 'default')
            result = test_single_api({"baseUrl": data['baseUrl'], "apiKey": data['apiKey'], "model": model})
            return self.send_json(result)

        return self.send_json({"error": "Not found"}, 404)

    # ── DELETE ────────────────────────────────────────────────────────────────
    def do_DELETE(self):
        path, query = self.parse_path()

        # 1. 删除整个配置文件
        if path == '/api/config':
            name = query.get('config')
            if not name:
                return self.send_json({"error": "Config name required"}, 400)
            
            # 安全检查：防止删除后无配置可用
            files = [f for f in os.listdir(CONFIG_DIR) if f.endswith('.json')]
            if len(files) <= 1:
                return self.send_json({"error": "Cannot delete the last remaining config"}, 400)
            
            cfg = get_config_path(name)
            if os.path.exists(cfg):
                try:
                    os.remove(cfg)
                    print(f"[DELETE] Config file removed: {cfg}")
                    return self.send_json({"status": "success"})
                except Exception as e:
                    print(f"[ERROR] Failed to remove config: {e}")
                    return self.send_json({"error": str(e)}, 500)
            return self.send_json({"error": "Config not found"}, 404)

        # 2. 从配置中删除单个节点 (Provider)
        if path.startswith('/api/providers/'):
            name = unquote(path[len('/api/providers/'):])
            cfg = get_config_path(query.get('config'))
            if not os.path.exists(cfg):
                return self.send_json({"error": "Config not found"}, 404)
            with open(cfg, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            providers = config.get('models', {}).get('providers')
            if providers is None:
                providers = config.get('providers', {})
            
            if name in providers:
                del providers[name]
                with open(cfg, 'w', encoding='utf-8') as f:
                    json.dump(config, f, indent=2, ensure_ascii=False)
                print(f"[DELETE] Provider '{name}' removed from config: {cfg}")
                return self.send_json({"status": "success"})
            return self.send_json({"error": "Provider not found"}, 404)

        return self.send_json({"error": "Not found"}, 404)


# ─── 入口 ──────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    import socket
    import sys
    if sys.stdout.encoding.lower() != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass


    # Bind to all interfaces so LAN devices can also connect
    server = ThreadingHTTPServer(('0.0.0.0', PORT), Handler)

    # Resolve local LAN IP for display
    try:
        lan_ip = socket.gethostbyname(socket.gethostname())
    except Exception:
        lan_ip = '127.0.0.1'

    print(f"")
    print(f"  🦀  OAAI Model-Radar")
    print(f"  {'─' * 40}")
    print(f"  Local  : http://127.0.0.1:{PORT}")
    print(f"  Network: http://{lan_ip}:{PORT}")
    if os.path.isfile(INDEX_FILE):
        print(f"  UI     : ✓ index.html found")
    else:
        print(f"  UI     : ✗ index.html NOT found — open index.html directly in browser")
    print(f"  Config : {CONFIG_DIR}")
    print(f"  {'─' * 40}")
    print(f"  Press Ctrl+C to stop")
    print(f"")

    # 自动打开浏览器（延时 0.5 秒以确保服务已启动）
    if os.path.isfile(INDEX_FILE):
        threading.Timer(0.5, lambda: webbrowser.open(f'http://127.0.0.1:{PORT}')).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Stopped.")
