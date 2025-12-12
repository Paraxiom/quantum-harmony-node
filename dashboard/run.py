#!/usr/bin/env python3
"""
QuantumHarmony Node Operator
Dashboard + Node Control + RPC Proxy
"""
import http.server
import socketserver
import urllib.request
import subprocess
import signal
import json
import os
import time
import webbrowser

PORT = 9955
RPC_URL = "http://127.0.0.1:9944"
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(DIRECTORY)

NODE_PROCESS = None
NODE_LOG = "/tmp/quantumharmony-node.log"
NODE_BINARY = os.path.join(ROOT_DIR, "quantumharmony-node")
NODE_NAME = os.environ.get("NODE_NAME", "Operator")

BOOTNODES = [
    "/ip4/51.79.26.123/tcp/30333/p2p/12D3KooWRaui4w4RJjRYmrK23gBJeM4RHE2qg84zC4w2rUcbqerX",
    "/ip4/51.79.26.168/tcp/30333/p2p/12D3KooWPkzuqKSCUxRvj8R6bw7VLPCTq27E9yGPLbTwS1sPAxKP"
]

def start_node():
    global NODE_PROCESS
    if NODE_PROCESS and NODE_PROCESS.poll() is None:
        return {"success": True, "message": "already_running", "pid": NODE_PROCESS.pid}

    if not os.path.exists(NODE_BINARY):
        return {"success": False, "message": f"Binary not found: {NODE_BINARY}"}

    cmd = [
        NODE_BINARY,
        "--name", NODE_NAME,
        "--rpc-port", "9944",
        "--port", "30333",
        "--rpc-cors", "all",
        "--rpc-methods", "Unsafe",
        "--rpc-external",
    ]
    for bn in BOOTNODES:
        cmd.extend(["--bootnodes", bn])

    try:
        log_file = open(NODE_LOG, "w")
        NODE_PROCESS = subprocess.Popen(cmd, stdout=log_file, stderr=subprocess.STDOUT, preexec_fn=os.setsid)
        time.sleep(2)
        return {"success": True, "message": "started", "pid": NODE_PROCESS.pid}
    except Exception as e:
        return {"success": False, "message": str(e)}

def stop_node():
    global NODE_PROCESS
    if NODE_PROCESS is None or NODE_PROCESS.poll() is not None:
        NODE_PROCESS = None
        return {"success": True, "message": "not_running"}
    try:
        pid = NODE_PROCESS.pid
        os.killpg(os.getpgid(pid), signal.SIGTERM)
        NODE_PROCESS.wait(timeout=10)
        NODE_PROCESS = None
        return {"success": True, "message": "stopped", "pid": pid}
    except Exception as e:
        return {"success": False, "message": str(e)}

def get_status():
    global NODE_PROCESS
    if NODE_PROCESS and NODE_PROCESS.poll() is None:
        return {"node_running": True, "node_pid": NODE_PROCESS.pid}
    return {"node_running": False}

def proxy_rpc(body):
    try:
        req = urllib.request.Request(RPC_URL, data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode())
    except Exception as e:
        return {"jsonrpc": "2.0", "id": 1, "error": {"code": -32000, "message": str(e)}}


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        if self.path == "/status":
            self.send_json(get_status())
        elif self.path == "/logs":
            try:
                with open(NODE_LOG, "r") as f:
                    self.send_json({"logs": "".join(f.readlines()[-100:])})
            except:
                self.send_json({"logs": ""})
        else:
            super().do_GET()

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length) if length > 0 else b'{}'

        if self.path in ["/node/start", "/start"]:
            self.send_json(start_node())
        elif self.path in ["/node/stop", "/stop"]:
            self.send_json(stop_node())
        elif self.path in ["/node/restart", "/restart"]:
            stop_node()
            time.sleep(1)
            self.send_json(start_node())
        elif self.path == "/rpc":
            self.send_json(proxy_rpc(body))
        else:
            self.send_json({"error": "not found"}, 404)

    def log_message(self, format, *args):
        if "/rpc" not in args[0]:
            print(f"[{time.strftime('%H:%M:%S')}] {args[0]}")


if __name__ == '__main__':
    print(f"""
╔══════════════════════════════════════════════════╗
║      QuantumHarmony Node Operator                ║
╠══════════════════════════════════════════════════╣
║  Dashboard: http://localhost:{PORT}               ║
║  Node Binary: {NODE_BINARY[:40]}...
╚══════════════════════════════════════════════════╝
""")

    # Open browser
    webbrowser.open(f"http://localhost:{PORT}")

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down...")
            stop_node()
