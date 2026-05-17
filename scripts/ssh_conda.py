#!/usr/bin/env python3
"""Conda environment management on remote servers."""
import json, os, sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from ssh_exec import load_config, get_client, exec_cmd


def find_conda_path(client):
    for path in ["~/miniconda3", "~/anaconda3", "/opt/conda", "/opt/miniconda3"]:
        out, _, code = exec_cmd(client, f"test -d {path} && echo {path}")
        if code == 0 and out.strip():
            return out.strip()
    out, _, _ = exec_cmd(client, "which conda 2>/dev/null")
    if out.strip():
        return os.path.dirname(os.path.dirname(out.strip()))
    return ""


def list_envs(client, conda_path):
    out, err, _ = exec_cmd(client, f"{conda_path}/bin/conda env list 2>/dev/null || conda env list 2>/dev/null")
    print(out if out.strip() else err)


def list_packages(client, conda_path, env_name):
    out, err, _ = exec_cmd(client, f"{conda_path}/bin/conda list -n {env_name} 2>/dev/null || conda list -n {env_name} 2>/dev/null")
    print(out if out.strip() else err)


def create_env(client, conda_path, env_name, python_ver="3.10"):
    cmd = f"{conda_path}/bin/conda create -n {env_name} python={python_ver} -y 2>/dev/null || conda create -n {env_name} python={python_ver} -y"
    out, err, code = exec_cmd(client, cmd)
    print(out if out.strip() else err)
    return code


def install_packages(client, conda_path, env_name, packages):
    pkgs = " ".join(packages)
    cmd = f"{conda_path}/bin/conda install -n {env_name} {pkgs} -y 2>/dev/null || conda install -n {env_name} {pkgs} -y"
    out, err, code = exec_cmd(client, cmd)
    print(out if out.strip() else err)
    return code


def conda_info(client, conda_path):
    out, err, _ = exec_cmd(client, f"{conda_path}/bin/conda info 2>/dev/null || conda info 2>/dev/null")
    print(out if out.strip() else err)


def main():
    if len(sys.argv) < 3:
        print("Usage: python ssh_conda.py <alias> <action> [args...]")
        print("Actions: list, packages <env>, create <env> [python_ver], install <env> <pkgs...>, info")
        sys.exit(1)

    alias = sys.argv[1]
    action = sys.argv[2]

    srv = load_config().get(alias, {})
    conda_path = srv.get("conda_path", "")

    client, gateway = get_client(alias)
    try:
        if not conda_path:
            conda_path = find_conda_path(client)
            if not conda_path:
                print("Error: conda not found on remote server")
                sys.exit(1)
            print(f"[auto-detected conda at {conda_path}]")

        if action == "list":
            list_envs(client, conda_path)
        elif action == "packages":
            if len(sys.argv) < 4:
                print("Usage: python ssh_conda.py <alias> packages <env_name>")
                sys.exit(1)
            list_packages(client, conda_path, sys.argv[3])
        elif action == "create":
            env_name = sys.argv[3] if len(sys.argv) > 3 else None
            if not env_name:
                print("Usage: python ssh_conda.py <alias> create <env_name> [python_ver]")
                sys.exit(1)
            python_ver = sys.argv[4] if len(sys.argv) > 4 else "3.10"
            create_env(client, conda_path, env_name, python_ver)
        elif action == "install":
            if len(sys.argv) < 5:
                print("Usage: python ssh_conda.py <alias> install <env_name> <package1> [package2...]")
                sys.exit(1)
            install_packages(client, conda_path, sys.argv[3], sys.argv[4:])
        elif action == "info":
            conda_info(client, conda_path)
        else:
            print(f"Unknown action: {action}")
            sys.exit(1)
    finally:
        client.close()
        if gateway:
            gateway.close()


if __name__ == "__main__":
    main()
