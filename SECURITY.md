# Security Policy

Remote Server Manager can access real servers. Treat configuration and command execution carefully.

## Secrets

Never commit:

- `scripts/servers.json`
- Passwords
- Private key paths
- Hostnames or IP addresses that should remain private
- Tokens or cloud credentials

Use `scripts/servers.json.example` as the public template.

## Reporting issues

If you find a security issue, open a private report if available on GitHub, or contact the repository owner directly. Avoid posting working credentials, hostnames, or exploit details in public issues.

## Operational guidance

- Prefer SSH keys over passwords.
- Use least-privilege server accounts.
- Confirm destructive actions manually.
- Avoid automated writes to system paths.
- Rotate any credential that may have been exposed.
