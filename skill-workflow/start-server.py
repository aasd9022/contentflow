#!/usr/bin/env python3
"""
start-server.py - 启动本地静态HTTP服务器用于预览幻灯片

使用方法：
    python start-server.py
    然后在浏览器访问 http://localhost:8000
"""

import http.server
import socketserver
import os
import sys
from pathlib import Path


def start_server(port=8000, directory=None):
    if directory is None:
        directory = Path(__file__).parent / "data"

    os.chdir(directory)

    handler = http.server.SimpleHTTPRequestHandler

    try:
        with socketserver.TCPServer(("", port), handler) as httpd:
            print("=" * 60)
            print(f"🌐 本地预览服务器已启动")
            print(f"=" * 60)
            print(f"📁 服务目录: {directory}")
            print(f"🔗 访问地址: http://localhost:{port}")
            print(f"=" * 60)
            print(f"\n💡 在浏览器中打开以下链接查看幻灯片：")
            print(f"   http://localhost:{port}/")
            print(f"\n⚠️  按 Ctrl+C 停止服务器")
            print(f"=" * 60)

            # 自动打开浏览器
            import webbrowser
            import threading

            def open_browser():
                import time
                time.sleep(1)
                webbrowser.open(f"http://localhost:{port}/")

            threading.Thread(target=open_browser, daemon=True).start()

            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")
        sys.exit(0)
    except OSError as e:
        if e.errno == 10048:  # Windows: port already in use
            print(f"\n❌ 端口 {port} 已被占用，尝试使用 {port + 1}...")
            start_server(port + 1, directory)
        else:
            raise


if __name__ == "__main__":
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("⚠️  端口参数无效，使用默认 8000")

    start_server(port)
