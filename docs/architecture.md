# Architecture

Remote Server Manager keeps the implementation intentionally small. Each operation is a standalone script so an agent can call the narrowest tool for the job.

## Components

```text
agent request
  -> SKILL.md routing
  -> script selection
  -> scripts/servers.json alias lookup
  -> Paramiko SSH/SFTP client
  -> remote Linux server
```

## Shared flow

Most scripts follow the same pattern:

1. Parse command-line arguments.
2. Resolve the server alias from `scripts/servers.json`.
3. Create a Paramiko SSH client, optionally through a jump host.
4. Run the narrow operation.
5. Close the SSH client and gateway connection.

## Script boundaries

| Script | Boundary |
| --- | --- |
| `ssh_exec.py` | Shared SSH client creation and command execution |
| `ssh_conda.py` | Conda-specific remote commands |
| `ssh_script.py` | Upload a local script to `/tmp` and execute it |
| `ssh_upload.py` | SFTP upload only |
| `ssh_download.py` | SFTP download only |
| `ssh_tail.py` | Long-running remote `tail -f` session |
| `ssh_tunnel.py` | Local socket server and Paramiko direct TCP channel |
| `ssh_ps.py` | Process listing, search, and kill helpers |
| `ssh_memory.py` | Server metadata scan and config update |

## Design principles

- Keep commands explicit and auditable.
- Prefer small scripts over a large CLI framework.
- Keep secrets out of the repository.
- Make read-only checks easy.
- Keep write, kill, install, upload, and tunnel operations visible in command names.
