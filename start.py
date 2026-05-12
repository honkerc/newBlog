"""
============================================
一键启动脚本 - 魂牵梦绕博客
============================================
同时启动三个服务：
  - 后端 API  (FastAPI)  → http://localhost:8000
  - 前端博客  (Vue CLI)  → http://localhost:8080
  - Mini 端   (Vue CLI)  → http://localhost:3001

使用方式：
  python start.py

按 Ctrl+C 停止所有服务。
============================================
"""

import subprocess
import sys
import time
from pathlib import Path

BASE_DIR = Path(__file__).parent

SERVICES = [
    {
        "name": "后端 API",
        "cwd": BASE_DIR / "back",
        "cmd": [sys.executable, "run.py"],
        "port": 8000,
    },
    {
        "name": "前端博客",
        "cwd": BASE_DIR / "front",
        "cmd": ["npm", "run", "serve"],
        "port": 8080,
    },
    {
        "name": "Mini 端",
        "cwd": BASE_DIR / "mini",
        "cmd": ["npm", "run", "serve"],
        "port": 3001,
    },
]

BOLD = "\033[1m"
RESET = "\033[0m"


def main():
    banner = f"""
{BOLD}{'=' * 54}{RESET}
{BOLD}  魂牵梦绕 - 博客一键启动{RESET}
{BOLD}{'=' * 54}{RESET}

  后端 API   → {BOLD}http://localhost:8000{RESET}
  前端博客   → {BOLD}http://localhost:8080{RESET}
  Mini 端    → {BOLD}http://localhost:3001{RESET}

  管理员账号: admin / admin123

{BOLD}{'=' * 54}{RESET}
"""
    print(banner)

    processes = []

    try:
        for svc in SERVICES:
            print(f"  [{svc['name']}] 正在启动...")
            proc = subprocess.Popen(
                svc["cmd"],
                cwd=svc["cwd"],
                shell=True,
            )
            processes.append(proc)
            time.sleep(1.5)

        print(f"\n{BOLD}所有服务已启动！按 Ctrl+C 停止。{RESET}\n")

        for proc in processes:
            proc.wait()

    except KeyboardInterrupt:
        print(f"\n{BOLD}正在停止所有服务...{RESET}")
        for proc in processes:
            proc.terminate()
        print(f"{BOLD}所有服务已停止。{RESET}")


if __name__ == "__main__":
    main()
