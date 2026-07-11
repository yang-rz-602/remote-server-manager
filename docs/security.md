# Security Guide

Remote Server Manager is intentionally small, but it has high-impact capabilities. Use it as an operator tool, not as an unattended privileged daemon.

## Recommended practices

- Use SSH keys for production systems.
- Store credentials only in `scripts/servers.json`.
- Keep `scripts/servers.json` out of Git.
- Use non-root server accounts where possible.
- Start with read-only checks before making changes.
- Confirm package installs, file uploads, process kills, and tunnels before running them.
- Avoid writing to system paths from automation.

## Safer server accounts

Create accounts with only the access needed for the intended workflows. For example, a data processing account may need access to `/data/project` and a conda installation, but not passwordless sudo.

## Rotating credentials

Rotate credentials if:

- A config file was committed by mistake.
- A terminal recording or screenshot exposed a password.
- A server alias was shared publicly with real host details.
- A private key path or key file was copied into a public location.

## Public examples

Examples should use placeholder hosts such as:

- `example.com`
- `192.168.1.100`
- `10.0.0.5`

Do not use private production hostnames in docs or issues.
