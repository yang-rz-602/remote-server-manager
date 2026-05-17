#!/usr/bin/env python3
"""Scan remote server info and update servers.json with latest state."""
import json, os, sys, argparse
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "servers.json")
sys.path.insert(0, SCRIPT_DIR)
from ssh_exec import load_config, get_client, exec_cmd


def scan_server(client, conda_path=""):
    info = {}
    mappings = {
        "hostname": "hostname",
        "os": "cat /etc/os-release 2>/dev/null | grep PRETTY_NAME | cut -d'\"' -f2",
        "kernel": "uname -r",
        "arch": "uname -m",
        "cpu_cores": "nproc",
        "cpu_model": "lscpu | grep 'Model name' | sed 's/Model name:\\s*//' 2>/dev/null",
        "memory_total": "free -h | awk '/Mem:/{print $2}'",
        "memory_used": "free -h | awk '/Mem:/{print $3}'",
        "disk_root": "df -h / | tail -1 | awk '{print $2 \" used \" $3 \" (\" $5 \")\"}'",
        "uptime": "uptime -p 2>/dev/null || uptime",
        "ip_local": "hostname -I 2>/dev/null | awk '{print $1}'",
        "load_avg": "cat /proc/loadavg | awk '{print $1, $2, $3}'",
    }
    for key, cmd in mappings.items():
        out, _, _ = exec_cmd(client, cmd)
        info[key] = out.strip()

    if conda_path:
        out, _, _ = exec_cmd(client, f"ls {conda_path}/envs/ 2>/dev/null")
        info["conda_envs"] = [e.strip() for e in out.strip().split("\n") if e.strip()]
    else:
        info["conda_envs"] = []

    out, _, _ = exec_cmd(client, "systemctl list-units --type=service --state=running 2>/dev/null | grep running | wc -l")
    info["running_services"] = out.strip()
    info["last_scanned"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return info


def update_config(alias, scan_info, deep=False):
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)
    if alias not in config["servers"]:
        print(f"Error: server '{alias}' not in config")
        sys.exit(1)
    srv = config["servers"][alias]
    srv["last_scan"] = scan_info
    if deep and scan_info.get("conda_envs"):
        srv["conda_envs"] = scan_info["conda_envs"]
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

    print(f"Updated servers.json for '{alias}'")
    print(f"  Hostname:  {scan_info.get('hostname', 'N/A')}")
    print(f"  OS:        {scan_info.get('os', 'N/A')}")
    print(f"  Kernel:    {scan_info.get('kernel', 'N/A')}")
    print(f"  CPU:       {scan_info.get('cpu_cores', 'N/A')} cores ({scan_info.get('cpu_model', 'N/A')})")
    print(f"  Memory:    {scan_info.get('memory_used', 'N/A')} / {scan_info.get('memory_total', 'N/A')}")
    print(f"  Disk /:    {scan_info.get('disk_root', 'N/A')}")
    print(f"  Uptime:    {scan_info.get('uptime', 'N/A')}")
    print(f"  Load:      {scan_info.get('load_avg', 'N/A')}")
    print(f"  Services:  {scan_info.get('running_services', 'N/A')} running")
    print(f"  Conda:     {len(scan_info.get('conda_envs', []))} envs")
    print(f"  Scanned:   {scan_info.get('last_scanned', 'N/A')}")


def main():
    parser = argparse.ArgumentParser(description="Scan server and update memory")
    parser.add_argument("alias", nargs="?", help="Server alias")
    parser.add_argument("--deep", action="store_true", help="Deep scan")
    parser.add_argument("--refresh-all", action="store_true", help="Refresh all servers")
    args = parser.parse_args()

    if args.refresh_all:
        servers = load_config()
        for alias in servers:
            print(f"\n--- Scanning {alias} ---")
            srv = servers[alias]
            conda_path = srv.get("conda_path", "")
            client, gateway = get_client(alias)
            try:
                info = scan_server(client, conda_path)
                update_config(alias, info, args.deep)
            finally:
                client.close()
                if gateway:
                    gateway.close()
        return

    if not args.alias:
        print("Usage: python ssh_memory.py <alias> [--deep] | --refresh-all")
        sys.exit(1)

    srv = load_config().get(args.alias, {})
    conda_path = srv.get("conda_path", "")
    client, gateway = get_client(args.alias)
    try:
        info = scan_server(client, conda_path)
        update_config(args.alias, info, args.deep)
    finally:
        client.close()
        if gateway:
            gateway.close()


if __name__ == "__main__":
    main()
