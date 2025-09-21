#!/usr/bin/env python3
"""
Simple HTTP Server for Cloudflare Tunnel
Serves content on port 80 for web.190801.xyz
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path

# Create a simple HTML page
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Welcome to web.190801.xyz</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
        }
        .container {
            background: rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 10px;
            backdrop-filter: blur(10px);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
        }
        .status {
            background: rgba(0, 255, 0, 0.2);
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
            border-left: 4px solid #00ff00;
        }
        .info {
            background: rgba(255, 255, 255, 0.1);
            padding: 15px;
            border-radius: 5px;
            margin: 20px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Welcome to web.190801.xyz</h1>
        
        <div class="status">
            <h3>✅ Service Status: ONLINE</h3>
            <p>Your Cloudflare tunnel is working perfectly!</p>
        </div>
        
        <div class="info">
            <h3>📊 Server Information</h3>
            <ul>
                <li><strong>Domain:</strong> web.190801.xyz</li>
                <li><strong>Server:</strong> Python HTTP Server</li>
                <li><strong>Port:</strong> 80</li>
                <li><strong>Tunnel:</strong> Cloudflare Tunnel Active</li>
                <li><strong>Status:</strong> Connected and Running</li>
            </ul>
        </div>
        
        <div class="info">
            <h3>🔧 Configuration Details</h3>
            <p>This page is being served through your Cloudflare tunnel, which means:</p>
            <ul>
                <li>Your local server is accessible from anywhere on the internet</li>
                <li>Traffic is routed through Cloudflare's global network</li>
                <li>You get the benefits of Cloudflare's CDN and security features</li>
            </ul>
        </div>
        
        <div class="info">
            <h3>🎉 Success!</h3>
            <p>If you can see this page, your tunnel setup is working correctly!</p>
        </div>
    </div>
</body>
</html>"""

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode())
        else:
            super().do_GET()

def start_server(port=8080):
    """Start the HTTP server on the specified port"""
    try:
        # Check if port 80 is available
        with socketserver.TCPServer(("", port), CustomHTTPRequestHandler) as httpd:
            print(f"🚀 Starting HTTP server on port {port}")
            print(f"🌐 Server accessible at: http://localhost:{port}")
            print(f"🌍 Tunnel URL: https://web.190801.xyz")
            print("Press Ctrl+C to stop the server")
            httpd.serve_forever()
    except PermissionError:
        print(f"❌ Error: Permission denied to bind to port {port}")
        print("💡 Try running as Administrator or use a different port")
        sys.exit(1)
    except OSError as e:
        if e.errno == 10048:  # Port already in use
            print(f"❌ Error: Port {port} is already in use")
            print("💡 Try stopping other services using port 80")
        else:
            print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_server(8080)
