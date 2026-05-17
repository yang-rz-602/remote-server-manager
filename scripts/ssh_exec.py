#!/usr/bin/env python3
"""Execute remote commands via SSH with optional conda env activation. No args = health check."""
import json, os, sys, argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(SCRIPT_DIR, "servers.json")


def load_config():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["servers"]


def get_client(alias):
    import paramiko
    servers = load_config()
    if alias not in servers:
        print(f"Error: server '{alias}' not found. Available: {', '.join(servers.keys())}")
        sys.exit(1)
    srv = servers[alias]
    jump = srv.get("jump_host")
    if jump:
        jump_srv = servers[jump]
        gateway = paramiko.SSHClient()
        gateway.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        gateway.connect(jump_srv["host"], port=jump_srv["port"], username=jump_srv["username"],
                        password=jump_srv.get("password", ""), timeout=15)
        jump_transport = gateway.get_transport()
        channel = jump_transport.open_channel("direct-tcpip", (srv["host"], srv["port"]),
                                              (jump_srv["host"], jump_srv["port"]))
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(srv["host"], port=srv["port"], username=srv["username"],
                       password=srv.get("password", ""), sock=channel, timeout=15)
        return client, gateway
    else:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        kwargs = {"hostname": srv["host"], "port": srv["port"], "username": srv["username"], "timeout": 15}
        if srv["auth"] == "key":
            kwargs["key_filename"] = srv["key_path"]
        else:
            kwargs["password"] = srv.get("password", "")
        client.connect(**kwargs)
        return client, None


def exec_cmd(client, command, conda_env=None, conda_path=""):
    if conda_env and conda_path:
        activate = f"source {conda_path}/etc/profile.d/conda.sh && conda activate {conda_env} && "
        command = activate + command
    elif conda_env:
        activate = f"conda activate {conda_env} 2>/dev/null; "
        command = activate + command
    stdin, stdout, stderr = client.exec_command(command, timeout=60)
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    return out, err, stdout.channel.recv_exit_status()


def health_check(client, conda_path=""):
    cmds = {
        "hostname": "hostname",
        "os": "cat /etc/os-release 2>/dev/null | head -2",
        "kernel": "uname -r",
        "uptime": "uptime",
        "cpu": "lscpu | grep -E '^(Architecture|CPU\\(s\\)|Model name)' 2>/dev/null || nproc",
        "memory": "free -h | head -2",
        "disk": "df -h | grep -E '^/dev/'",
        "load": "cat /proc/loadavg 2>/dev/null || uptime",
    }
    if conda_path:
        cmds["conda"] = f"ls {conda_path}/envs/ 2>/dev/null || echo 'conda not found at {conda_path}'"

    print("=" * 50)
    print("  SERVER HEALTH CHECK")
    print("=" * 50)
    for label, cmd in cmds.items():
        out, err, code = exec_cmd(client, cmd)
        val = out.strip() if out.strip() else err.strip()
        if label == "memory":
            lines = val.split("\n")
            print(f"  Memory:  {lines[0] if lines else val}")
            if len(lines) > 1:
                print(f"           {lines[1]}")
        elif label == "disk":
            for line in val.split("\n"):
                print(f"  Disk:    {line}")
        else:
            print(f"  {label.capitalize():10s} {val}")
    print("=" * 50)


def main():
    parser = argparse.ArgumentParser(description="SSH remote command executor")
    parser.add_argument("alias", help="Server alias from servers.json")
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to execute (omit for health check)")
    parser.add_argument("--conda", dest="conda_env", help="Conda environment to activate")
    args = parser.parse_args()

    srv = load_config().get(args.alias, {})
    conda_path = srv.get("conda_path", "")

    client, gateway = get_client(args.alias)
    try:
        if args.command:
            cmd = " ".join(args.command)
            out, err, code = exec_cmd(client, cmd, conda_env=args.conda_env, conda_path=conda_path)
            if out:
                print(out, end="")
            if err:
                print(err, end="", file=sys.stderr)
            sys.exit(code)
        else:
            health_check(client, conda_path=conda_path)
    finally:
        client.close()
        if gateway:
            gateway.close()


if __name__ == "__main__":
    main()
