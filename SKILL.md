---
name: remote-server-manager
description: Remote server management via SSH — connect, execute commands, manage conda environments, transfer files, monitor logs, port forwarding, process management. Trigger when user mentions: 连接服务器, SSH, 远程执行, 服务器状态, conda环境, 上传文件, 下载文件, 端口转发, 进程管理, or server aliases like storage, a100.
metadata:
  type: reference
  version: 1.0.0
---

# Remote Server Manager

SSH-based remote server management skill for Claude Code. Uses paramiko (pure Python SSH) for reliable execution in non-interactive environments.

## Server Configuration

Servers are defined in `~/.claude/skills/remote-server-manager/scripts/servers.json`.

To add a new server, edit that JSON file and add an entry:
```json
{
  "my-server": {
    "host": "1.2.3.4",
    "port": 22,
    "username": "user",
    "password": "pass",
    "auth": "password",
    "conda_path": "",
    "default_env": "",
    "description": "My server"
  }
}
```

For SSH key auth, set `"auth": "key"` and `"key_path": "/path/to/key.pem"`.
For jump host (two-hop), set `"jump_host": "alias-of-gateway-server"`.

## All Commands

All scripts are in `~/.claude/skills/remote-server-manager/scripts/`.

### Execute Command / Health Check
```bash
python ~/.claude/skills/remote-server-manager/scripts/ssh_exec.py <alias> "<command>"
python ~/.claude/skills/remote-server-manager/scripts/ssh_exec.py <alias>
python ~/.claude/skills/remote-server-manager/scripts/ssh_exec.py <alias> "<cmd>" --conda myenv
```

### Conda Environment Management
```bash
python ~/.claude/skills/remote-server-manager/scripts/ssh_conda.py <alias> list
python ~/.claude/skills/remote-server-manager/scripts/ssh_conda.py <alias> packages <env>
python ~/.claude/skills/remote-server-manager/scripts/ssh_conda.py <alias> create <env> [python_ver]
python ~/.claude/skills/remote-server-manager/scripts/ssh_conda.py <alias> install <env> <pkg1> [pkg2...]
python ~/.claude/skills/remote-server-manager/scripts/ssh_conda.py <alias> info
```

### File Transfer
```bash
python ~/.claude/skills/remote-server-manager/scripts/ssh_upload.py <alias> <local_path> <remote_path>
python ~/.claude/skills/remote-server-manager/scripts/ssh_download.py <alias> <remote_path> <local_path>
```

### Remote Script Execution
```bash
python ~/.claude/skills/remote-server-manager/scripts/ssh_script.py <alias> <local_script> [--conda env] [args...]
```

### Real-time Log Monitoring
```bash
python ~/.claude/skills/remote-server-manager/scripts/ssh_tail.py <alias> <remote_path> [lines=50]
```

### Port Forwarding / Tunnel
```bash
python ~/.claude/skills/remote-server-manager/scripts/ssh_tunnel.py <alias> <remote_host:remote_port> <local_port>
python ~/.claude/skills/remote-server-manager/scripts/ssh_tunnel.py storage 127.0.0.1:3306 3306
```

### Process Management
```bash
python ~/.claude/skills/remote-server-manager/scripts/ssh_ps.py <alias>
python ~/.claude/skills/remote-server-manager/scripts/ssh_ps.py <alias> search <name>
python ~/.claude/skills/remote-server-manager/scripts/ssh_ps.py <alias> kill <pid>
```

### Memory / Info Update
```bash
python ~/.claude/skills/remote-server-manager/scripts/ssh_memory.py <alias>
python ~/.claude/skills/remote-server-manager/scripts/ssh_memory.py <alias> --deep
python ~/.claude/skills/remote-server-manager/scripts/ssh_memory.py --refresh-all
```

## Trigger Keywords

Activate this skill when the user says:
- 连接服务器, 登录服务器, SSH到..., 远程执行, 在服务器上运行
- 服务器状态, 健康检查, 服务器信息
- conda环境, 列出环境, 激活环境, 安装包
- 上传文件, 下载文件, 传输文件
- 远程日志, tail日志, 监控日志
- 端口转发, 隧道, 映射端口
- 查看进程, 杀掉进程, 进程管理
- 远程脚本, 运行脚本
- 更新服务器信息, 刷新服务器记忆
- Server aliases: storage, a100, a100-node2, a100-node3
