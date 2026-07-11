# Troubleshooting

## `ModuleNotFoundError: No module named 'paramiko'`

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## `server '<alias>' not found`

Check that:

- `scripts/servers.json` exists.
- The JSON has a top-level `servers` object.
- The alias matches exactly.

## Authentication fails

Check:

- Host, port, username, and auth mode
- Password or private key path
- Server firewall and SSH service status
- Whether the server requires a jump host

## Conda command fails

Set `conda_path` in `servers.json`, or verify that `conda` is available on the remote shell path.

## Tunnel starts but the browser cannot connect

Check:

- The remote service is listening on the specified host and port.
- The local port is not already in use.
- Firewalls or service binding rules are not blocking access.

## Path looks wrong on Windows Git Bash

Some scripts normalize Git Bash paths such as `/home` being rewritten under `C:/Program Files/Git`. Use quoted paths and absolute remote paths where possible.
