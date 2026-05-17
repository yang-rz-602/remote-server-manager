#!/usr/bin/env python3
"""SSH port forwarding / tunnel."""
import sys, time, signal, os, socket, threading, select

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SCRIPT_DIR)
from ssh_exec import load_config, get_client


def main():
    if len(sys.argv) < 4:
        print("Usage: python ssh_tunnel.py <alias> <remote_host:remote_port> <local_port>")
        print("Example: python ssh_tunnel.py storage 127.0.0.1:3306 3306")
        sys.exit(1)

    alias = sys.argv[1]
    remote = sys.argv[2]
    local_port = int(sys.argv[3])

    if ":" in remote:
        remote_host, remote_port = remote.rsplit(":", 1)
        remote_port = int(remote_port)
    else:
        print("Error: remote must be host:port format")
        sys.exit(1)

    client, gateway = get_client(alias)

    class TunnelServer:
        def __init__(self):
            self.running = True

        def handle(self, client_socket):
            try:
                channel = client.get_transport().open_channel(
                    "direct-tcpip", (remote_host, remote_port), client_socket.getpeername()
                )
                while self.running:
                    r, _, _ = select.select([client_socket, channel], [], [], 1)
                    if client_socket in r:
                        data = client_socket.recv(4096)
                        if not data:
                            break
                        channel.send(data)
                    if channel in r:
                        data = channel.recv(4096)
                        if not data:
                            break
                        client_socket.send(data)
            except Exception:
                pass
            finally:
                try:
                    client_socket.close()
                except Exception:
                    pass

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("127.0.0.1", local_port))
    server_socket.listen(5)
    server_socket.settimeout(1)

    tunnel = TunnelServer()
    print(f"Tunnel active: localhost:{local_port} -> {remote_host}:{remote_port} (via {alias})")
    print(f"Press Ctrl+C to stop")

    def shutdown(sig, frame):
        tunnel.running = False
        server_socket.close()
        client.close()
        if gateway:
            gateway.close()
        print("\nTunnel closed.")
        sys.exit(0)

    signal.signal(signal.SIGINT, shutdown)

    while tunnel.running:
        try:
            sock, _ = server_socket.accept()
            t = threading.Thread(target=tunnel.handle, args=(sock,), daemon=True)
            t.start()
        except socket.timeout:
            continue
        except OSError:
            break


if __name__ == "__main__":
    main()
