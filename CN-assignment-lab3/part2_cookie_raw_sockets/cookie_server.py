#!/usr/bin/env python3
"""
Minimal HTTP server over raw sockets demonstrating cookie-based sessions.
- On first visit (no Cookie header): sends Set-Cookie: session_id=<value> and a welcome message.
- On subsequent visits: reads Cookie and responds with "Welcome back".
Note: For simplicity this server handles one request per connection.
"""
import socket, threading, time, secrets

HOST, PORT = "127.0.0.1", 9090

def parse_headers(request_bytes: bytes):
    try:
        text = request_bytes.decode("iso-8859-1", errors="replace")
        lines = text.split("\r\n")
        request_line = lines[0]
        headers = {}
        for line in lines[1:]:
            if not line:
                break
            if ":" in line:
                k, v = line.split(":", 1)
                headers[k.strip()] = v.strip()
        return request_line, headers
    except Exception:
        return "", {}

def build_response(body_html: str, status="200 OK", headers=None):
    if headers is None:
        headers = {}
    body_bytes = body_html.encode("utf-8")
    base_headers = {
        "Date": time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime()),
        "Server": "CN3CookieServer/1.0",
        "Content-Type": "text/html; charset=utf-8",
        "Content-Length": str(len(body_bytes)),
        "Connection": "close",
    }
    base_headers.update(headers)
    head = [f"HTTP/1.1 {status}"] + [f"{k}: {v}" for k, v in base_headers.items()]
    return ("\r\n".join(head) + "\r\n\r\n").encode("iso-8859-1") + body_bytes

def handle_client(conn, addr):
    data = conn.recv(65536)
    req_line, headers = parse_headers(data)
    cookies = headers.get("Cookie", "")
    session_id = None

    # very small cookie parser
    for part in cookies.split(";"):
        if "=" in part:
            k, v = part.strip().split("=", 1)
            if k == "session_id":
                session_id = v

    if session_id:
        body = f"""<!doctype html><html><body>
        <h1>Welcome back!</h1>
        <p>Your session_id is <code>{session_id}</code>.</p>
        </body></html>"""
        resp = build_response(body)
    else:
        session_id = secrets.token_hex(8)
        body = f"""<!doctype html><html><body>
        <h1>Hello, new visitor!</h1>
        <p>A session cookie has been set for you.</p>
        </body></html>"""
        headers_out = {
            # Set cookie for 1 day
            "Set-Cookie": f"session_id={session_id}; Max-Age=86400; Path=/; HttpOnly; SameSite=Lax"
        }
        resp = build_response(body, headers=headers_out)

    conn.sendall(resp)
    conn.close()

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"Cookie server running on http://{HOST}:{PORT}")
        try:
            while True:
                conn, addr = s.accept()
                threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()
        except KeyboardInterrupt:
            print("\nShutting down cookie server...")

if __name__ == "__main__":
    main()
