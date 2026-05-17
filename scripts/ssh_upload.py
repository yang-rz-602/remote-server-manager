#!/usr/bin/env python3
"""Upload a local file to a remote server via SFTP."""
import json, os, sys, re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from ssh_exec import load_config, get_client


def fix_remote_path(path):
    """Fix Git Bash path conversion (e.g. /home -> C:/Program Files/Git/home)."""
    m = re.match(r'^[A-Za-z]:/Program Files/Git(/.*)', path)
    return m.group(1) if m else path


def main():
    if len(sys.argv) < 4:
        print("Usage: python ssh_upload.py <alias> <local_path> <remote_path>")
        sys.exit(1)

    alias = sys.argv[1]
    local_path = sys.argv[2]
    remote_path = fix_remote_path(sys.argv[3])

    if not os.path.isfile(local_path):
        print(f"Error: local file not found: {local_path}")
        sys.exit(1)

    client, gateway = get_client(alias)
    try:
        sftp = client.open_sftp()
        sftp.put(local_path, remote_path)
        size = os.path.getsize(local_path)
        print(f"Uploaded: {local_path} -> {remote_path} ({size} bytes)")
        sftp.close()
    finally:
        client.close()
        if gateway:
            gateway.close()


if __name__ == "__main__":
    main()
