#!/usr/bin/env python3
"""Capture a genuine interactive cli.py session through a pseudo-terminal.

Runs src/cli.py under a pty so the typed input is echoed exactly as it would be
in a real terminal, and writes the combined transcript to stdout. Not a project
artifact -- a helper used to produce the docs/screenshots transcripts.

Usage:  python3 _capture.py "line1" "line2" ...   (each arg = one typed line)
"""
import os, pty, sys, time

lines = sys.argv[1:]
repo = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
argv = [sys.executable, os.path.join(repo, "src", "cli.py")]

captured = bytearray()
fed = {"i": 0}


def read(fd):
    data = os.read(fd, 1024)
    captured.extend(data)
    return data


pid, master = pty.fork()
if pid == 0:  # child: exec the CLI
    os.chdir(repo)
    os.execv(argv[0], argv)
else:  # parent: drip-feed input, drain output
    time.sleep(0.15)
    for ln in lines:
        try:
            read(master)
        except OSError:
            break
        os.write(master, (ln + "\n").encode())
        time.sleep(0.12)
    while True:
        try:
            if not read(master):
                break
        except OSError:
            break
    os.waitpid(pid, 0)

sys.stdout.write("$ python3 src/cli.py\n")
sys.stdout.write(captured.decode(errors="replace"))
