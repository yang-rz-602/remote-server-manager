# remote-server-manager

Claude Code Skill for remote server management via SSH. Uses [paramiko](https://www.paramiko.org/) (pure Python SSH) for reliable non-interactive execution.

## Features

| Script | Function |
|--------|----------|
| `ssh_exec.py` | Execute remote commands / health check |
| `ssh_conda.py` | Conda environment management |
| `ssh_script.py` | Upload and run local scripts on server |
| `ssh_tail.py` | Real-time log monitoring (tail -f) |
| `ssh_tunnel.py` | SSH port forwarding / tunnel |
| `ssh_ps.py` | Process management (list/search/kill) |
| `ssh_upload.py` | Upload files to server |
| `ssh_download.py` | Download files from server |
| `ssh_memory.py` | Scan server info and update config |

## Requirements

- Python 3.8+
- paramiko (`pip install paramiko`)

## Installation

1. Copy the `remote-server-manager` folder to `~/.claude/skills/`:
   ```bash
   cp -r remote-server-manager ~/.claude/skills/
   ```

2. Install paramiko:
   ```bash
   pip install paramiko
   ```

3. Create your server config from the example:
   ```bash
   cd ~/.claude/skills/remote-server-manager/scripts
   cp servers.json.example servers.json
   # Edit servers.json with your real server info
   ```

## Configuration

Edit `scripts/servers.json`:

```json
{
  "servers": {
    "my-server": {
      "host": "192.168.1.100",
      "port": 22,
      "username": "your_username",
      "password": "your_password",
      "auth": "password",
      "key_path": "",
      "jump_host": null,
      "conda_path": "",
      "default_env": "",
      "description": "My Linux server"
    }
  }
}
```

### Fields

| Field | Description |
|-------|-------------|
| `host` | Server IP or hostname |
| `port` | SSH port (default: 22) |
| `username` | SSH username |
| `password` | SSH password (when auth=password) |
| `auth` | `"password"` or `"key"` |
| `key_path` | Path to .pem/.ppk file (when auth=key) |
| `jump_host` | Alias of gateway server for two-hop, or `null` for direct |
| `conda_path` | Conda installation path (auto-detected if empty) |
| `default_env` | Default conda environment name |
| `description` | Human-readable description |

### SSH Key Authentication

```json
{
  "auth": "key",
  "key_path": "/path/to/your_key.pem"
}
```

### Jump Host (Two-Hop)

```json
{
  "gateway": {
    "host": "10.0.0.1",
    "port": 22,
    "username": "user",
    "password": "pass",
    "auth": "password",
    "jump_host": null
  },
  "internal-node": {
    "host": "10.0.0.5",
    "port": 22,
    "username": "user",
    "password": "pass",
    "auth": "password",
    "jump_host": "gateway"
  }
}
```

## Usage

All scripts are in `scripts/`. Run with `python <script>`.

### Command Execution

```bash
# Execute a command
python ssh_exec.py my-server "uname -a && uptime"

# With conda environment
python ssh_exec.py my-server "python train.py" --conda myenv

# Health check (no command = auto health check)
python ssh_exec.py my-server
```

### Conda Management

```bash
python ssh_conda.py my-server list                    # List environments
python ssh_conda.py my-server packages myenv          # List packages in env
python ssh_conda.py my-server create myenv 3.10       # Create env with Python 3.10
python ssh_conda.py my-server install myenv numpy     # Install packages
python ssh_conda.py my-server info                    # Conda info
```

### File Transfer

```bash
python ssh_upload.py my-server ./local_file.txt /remote/path/file.txt
python ssh_download.py my-server /remote/path/file.txt ./local_file.txt
```

### Remote Script Execution

```bash
python ssh_script.py my-server ./analyze.py arg1 arg2
python ssh_script.py my-server ./train.sh --conda myenv
```

### Log Monitoring

```bash
python ssh_tail.py my-server /var/log/syslog
python ssh_tail.py my-server /var/log/app.log 100     # Last 100 lines
```

### Port Forwarding

```bash
# Map remote MySQL to localhost:3306
python ssh_tunnel.py my-server 127.0.0.1:3306 3306

# Map remote Jupyter to localhost:8888
python ssh_tunnel.py my-server 127.0.0.1:8888 8888
```

### Process Management

```bash
python ssh_ps.py my-server                   # List all processes
python ssh_ps.py my-server search python     # Search by name
python ssh_ps.py my-server kill 12345        # Kill process by PID
```

### Memory Update

```bash
python ssh_memory.py my-server               # Scan and update config
python ssh_memory.py my-server --deep        # Deep scan (with conda info)
python ssh_memory.py --refresh-all           # Refresh all servers
```

## Claude Code Integration

This skill is designed for [Claude Code](https://docs.anthropic.com/en/docs/claude-code). Once installed to `~/.claude/skills/`, Claude will automatically use it when you mention:

- "连接服务器", "SSH", "远程执行"
- "服务器状态", "健康检查"
- "conda环境", "列出环境"
- "上传文件", "下载文件"
- "端口转发", "隧道"
- "查看进程", "杀掉进程"
- Server aliases like "storage", "my-server"

## Security Notes

- `servers.json` contains passwords and is excluded from git via `.gitignore`
- Never commit real credentials to version control
- Use `servers.json.example` as a template
- Consider SSH key authentication for production use

## License

MIT
