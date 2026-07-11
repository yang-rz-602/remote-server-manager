# Contributing

Thanks for improving Remote Server Manager.

## Good contributions

- Clearer docs and examples
- Safer command handling
- Better SSH, SFTP, conda, or tunnel behavior
- Cross-platform path fixes
- Tests or validation scripts

## Development setup

```bash
python -m pip install -r requirements.txt
python -m py_compile scripts/*.py
```

## Safety expectations

- Do not commit `scripts/servers.json`.
- Do not include real IP addresses, hostnames, passwords, tokens, or private key paths in examples.
- Prefer read-only operations in examples unless the action is clearly marked.
- Keep destructive operations explicit and narrow.

## Pull request checklist

- The change has a clear reason.
- Documentation is updated when command behavior changes.
- `python -m py_compile scripts/*.py` passes.
- No local credentials or generated caches are included.
