#!/usr/bin/env python3
"""Process management on remote servers."""
import sys, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from ssh_exec import load_config, get_client, exec_cmd


def list_processes(client):
    cmd = "ps aux --sort=-%mem | head -25"
    out, _, _ = exec_cmd(client, cmd)
    print(out)


def search_process(client, name):
    cmd = f"ps aux | grep -i '{name}' | grep -v grep"
    out, _, _ = exec_cmd(client, cmd)
    if out.strip():
        print(out)
    else:
        print(f"No processes found matching '{name}'")


def kill_process(client, pid):
    cmd = f"kill {pid}"
    out, err, code = exec_cmd(client, cmd)
    if code == 0:
        print(f"Process {pid} killed successfully")
    else:
        print(f"Failed to kill {pid}: {err.strip()}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python ssh_ps.py <alias> [kill <pid> | search <name>]")
        sys.exit(1)

    alias = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else "list"

    client, gateway = get_client(alias)
    try:
        if action == "kill":
            if len(sys.argv) < 4:
                print("Usage: python ssh_ps.py <alias> kill <pid>")
                sys.exit(1)
            kill_process(client, sys.argv[3])
        elif action == "search":
            if len(sys.argv) < 4:
                print("Usage: python ssh_ps.py <alias> search <name>")
                sys.exit(1)
            search_process(client, sys.argv[3])
        else:
            list_processes(client)
    finally:
        client.close()
        if gateway:
            gateway.close()


if __name__ == "__main__":
    main()
