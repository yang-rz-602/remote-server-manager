#!/usr/bin/env python3
"""Real-time log monitoring (tail -f) on remote server."""
import sys, time, os, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from ssh_exec import load_config, get_client


def fix_remote_path(path):
    """Fix Git Bash path conversion (e.g. /home -> C:/Program Files/Git/home)."""
    m = re.match(r'^[A-Za-z]:/Program Files/Git(/.*)', path)
    return m.group(1) if m else path


def main():
    if len(sys.argv) < 3:
        print("Usage: python ssh_tail.py <alias> <remote_path> [lines=50]")
        sys.exit(1)

    alias = sys.argv[1]
    remote_path = fix_remote_path(sys.argv[2])
    lines = int(sys.argv[3]) if len(sys.argv) > 3 else 50

    client, gateway = get_client(alias)
    try:
        transport = client.get_transport()
        channel = transport.open_session()
        channel.exec_command(f"tail -n {lines} -f {remote_path}")

        last_data = time.time()
        try:
            while True:
                if channel.recv_ready():
                    data = channel.recv(4096).decode("utf-8", errors="replace")
                    print(data, end="", flush=True)
                    last_data = time.time()
                elif channel.exit_status_ready():
                    break
                else:
                    if time.time() - last_data > 300:
                        print("\n[timeout: no output for 300s]")
                        break
                    time.sleep(0.1)
        except KeyboardInterrupt:
            print("\n[stopped by user]")
    finally:
        client.close()
        if gateway:
            gateway.close()


if __name__ == "__main__":
    main()
