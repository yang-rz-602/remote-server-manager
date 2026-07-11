# Command Reference

All commands assume you are in the repository root.

## Health check

```bash
python scripts/ssh_exec.py <alias>
```

## Execute command

```bash
python scripts/ssh_exec.py <alias> "hostname && uptime"
python scripts/ssh_exec.py <alias> "python train.py" --conda myenv
```

## Conda

```bash
python scripts/ssh_conda.py <alias> list
python scripts/ssh_conda.py <alias> packages <env>
python scripts/ssh_conda.py <alias> create <env> 3.10
python scripts/ssh_conda.py <alias> install <env> numpy pandas
python scripts/ssh_conda.py <alias> info
```

## File transfer

```bash
python scripts/ssh_upload.py <alias> ./local.txt /remote/path/local.txt
python scripts/ssh_download.py <alias> /remote/path/result.txt ./result.txt
```

## Run a local script remotely

```bash
python scripts/ssh_script.py <alias> ./script.py --conda myenv arg1 arg2
python scripts/ssh_script.py <alias> ./script.sh arg1 arg2
```

## Logs

```bash
python scripts/ssh_tail.py <alias> /var/log/app.log
python scripts/ssh_tail.py <alias> /var/log/app.log 100
```

## Port forwarding

```bash
python scripts/ssh_tunnel.py <alias> 127.0.0.1:8888 8888
```

## Processes

```bash
python scripts/ssh_ps.py <alias>
python scripts/ssh_ps.py <alias> search python
python scripts/ssh_ps.py <alias> kill 12345
```

## Server metadata

```bash
python scripts/ssh_memory.py <alias>
python scripts/ssh_memory.py <alias> --deep
python scripts/ssh_memory.py --refresh-all
```
