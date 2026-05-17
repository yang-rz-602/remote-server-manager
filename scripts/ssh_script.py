#!/usr/bin/env python3
"""Upload and execute a local script on a remote server."""
import json, os, sys, argparse

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from ssh_exec import load_config, get_client, exec_cmd


def main():
    parser = argparse.ArgumentParser(description="Upload and execute a local script on remote server")
    parser.add_argument("alias", help="Server alias")
    parser.add_argument("script", help="Local script path (.py, .sh, .bash)")
    parser.add_argument("--conda", dest="conda_env", help="Conda environment to activate")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments to pass to the script")
    args = parser.parse_args()

    if not os.path.isfile(args.script):
        print(f"Error: script not found: {args.script}")
        sys.exit(1)

    srv = load_config().get(args.alias, {})
    conda_path = srv.get("conda_path", "")
    ext = os.path.splitext(args.script)[1]
    remote_name = os.path.basename(args.script)
    remote_path = f"/tmp/{remote_name}"

    client, gateway = get_client(args.alias)
    try:
        sftp = client.open_sftp()
        sftp.put(args.script, remote_path)
        sftp.close()
        print(f"[uploaded {args.script} -> {remote_path}]")

        cmd_parts = []
        if ext in (".py",):
            cmd_parts.append(f"python3 {remote_path}")
        else:
            cmd_parts.append(f"bash {remote_path}")
        if args.args:
            cmd_parts.extend(args.args)
        cmd = " ".join(cmd_parts)

        if args.conda_env and conda_path:
            cmd = f"source {conda_path}/etc/profile.d/conda.sh && conda activate {args.conda_env} && {cmd}"
        elif args.conda_env:
            cmd = f"conda activate {args.conda_env} 2>/dev/null; {cmd}"

        cmd = f"chmod +x {remote_path} && {cmd}"

        stdin, stdout, stderr = client.exec_command(cmd, timeout=300)
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        code = stdout.channel.recv_exit_status()

        if out:
            print(out, end="")
        if err:
            print(err, end="", file=sys.stderr)

        client.exec_command(f"rm -f {remote_path}")
        sys.exit(code)
    finally:
        client.close()
        if gateway:
            gateway.close()


if __name__ == "__main__":
    main()
