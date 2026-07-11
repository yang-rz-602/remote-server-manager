# Configuration Guide

Server aliases are stored in `scripts/servers.json`.

Start from the template:

```bash
cp scripts/servers.json.example scripts/servers.json
```

## Basic password authentication

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

## SSH key authentication

```json
{
  "servers": {
    "gpu-node": {
      "host": "example.internal",
      "port": 22,
      "username": "ubuntu",
      "password": "",
      "auth": "key",
      "key_path": "~/.ssh/id_rsa",
      "jump_host": null,
      "conda_path": "",
      "default_env": "base",
      "description": "GPU node"
    }
  }
}
```

## Jump host

Use `jump_host` when a server is reachable only through a gateway alias.

```json
{
  "servers": {
    "gateway": {
      "host": "gateway.example.com",
      "port": 22,
      "username": "user",
      "password": "",
      "auth": "key",
      "key_path": "~/.ssh/id_rsa",
      "jump_host": null,
      "conda_path": "",
      "default_env": "",
      "description": "Gateway"
    },
    "internal-node": {
      "host": "10.0.0.5",
      "port": 22,
      "username": "user",
      "password": "",
      "auth": "key",
      "key_path": "~/.ssh/id_rsa",
      "jump_host": "gateway",
      "conda_path": "",
      "default_env": "base",
      "description": "Internal compute node"
    }
  }
}
```

## Fields

| Field | Description |
| --- | --- |
| `host` | Server hostname or IP address |
| `port` | SSH port, usually `22` |
| `username` | SSH username |
| `password` | Password for password auth; leave empty for key auth |
| `auth` | `password` or `key` |
| `key_path` | Private key path for key auth |
| `jump_host` | Gateway server alias, or `null` |
| `conda_path` | Conda install path; leave empty for auto-detection |
| `default_env` | Default conda environment name |
| `description` | Human-readable server description |
