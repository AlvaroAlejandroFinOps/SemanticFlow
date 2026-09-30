"""
Script to build a standalone, single-file binary for SemanticFlow using PyInstaller.
Produces an independent executable that does not require an external Python runtime.
"""
import os
import subprocess
import sys
from pathlib import Path


def build_binary():
    root = Path(__file__).resolve().parent.parent
    dist_dir = root / "dist"
    build_dir = root / "build"

    print(f"[*] Building SemanticFlow standalone executable from {root}...")

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--name=semanticflow",
        "--onefile",
        "--clean",
        "--noconfirm",
        f"--distpath={dist_dir}",
        f"--workpath={build_dir}",
        str(root / "src" / "cli.py"),
    ]

    env = os.environ.copy()
    env["PYTHONPATH"] = str(root)

    res = subprocess.run(cmd, cwd=str(root), env=env)
    if res.returncode != 0:
        print("[!] Build failed.", file=sys.stderr)
        sys.exit(res.returncode)

    ext = ".exe" if sys.platform == "win32" else ""
    target_bin = dist_dir / f"semanticflow{ext}"
    print(f"[+] Standalone binary successfully generated at: {target_bin}")


if __name__ == "__main__":
    build_binary()
