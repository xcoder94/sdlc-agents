#!/usr/bin/env python3
"""
Source: anthropics/skills skills/webapp-testing/scripts/with_server.py @ dbd4588f9e1033efb41dad4bef2f7947c8993d44
(Apache-2.0, see ../LICENSE.txt). MODIFIED for the SDLC agent environment (security-vetted, fx43):
- servers start in their own session/process group (start_new_session=True) and are stopped with os.killpg,
  so `cd x && npm run dev` no longer orphans the real server;
- server stdout/stderr go to DEVNULL (or to per-server log files with --log-dir) instead of an undrained PIPE.
Prefer the project's containerized/CI runner over the host when one exists.

Start one or more servers, wait for them to be ready, run a command, then clean up.

Usage:
    # Single server
    python scripts/with_server.py --server "npm run dev" --port 5173 -- python automation.py
    python scripts/with_server.py --server "npm start" --port 3000 -- python test.py

    # Multiple servers
    python scripts/with_server.py \
      --server "cd backend && python server.py" --port 3000 \
      --server "cd frontend && npm run dev" --port 5173 \
      -- python test.py
"""

import os
import signal
import subprocess
import socket
import time
import sys
import argparse

def is_server_ready(port, timeout=30):
    """Wait for server to be ready by polling the port."""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(('localhost', port), timeout=1):
                return True
        except (socket.error, ConnectionRefusedError):
            time.sleep(0.5)
    return False


def main():
    parser = argparse.ArgumentParser(description='Run command with one or more servers')
    parser.add_argument('--server', action='append', dest='servers', required=True, help='Server command (can be repeated)')
    parser.add_argument('--port', action='append', dest='ports', type=int, required=True, help='Port for each server (must match --server count)')
    parser.add_argument('--timeout', type=int, default=30, help='Timeout in seconds per server (default: 30)')
    parser.add_argument('--log-dir', default=None, help='Write each server\'s stdout/stderr to <log-dir>/server-N.log (default: discard)')
    parser.add_argument('command', nargs=argparse.REMAINDER, help='Command to run after server(s) ready')

    args = parser.parse_args()

    # Remove the '--' separator if present
    if args.command and args.command[0] == '--':
        args.command = args.command[1:]

    if not args.command:
        print("Error: No command specified to run")
        sys.exit(1)

    # Parse server configurations
    if len(args.servers) != len(args.ports):
        print("Error: Number of --server and --port arguments must match")
        sys.exit(1)

    servers = []
    for cmd, port in zip(args.servers, args.ports):
        servers.append({'cmd': cmd, 'port': port})

    server_processes = []
    log_files = []
    if args.log_dir:
        os.makedirs(args.log_dir, exist_ok=True)

    try:
        # Start all servers
        for i, server in enumerate(servers):
            print(f"Starting server {i+1}/{len(servers)}: {server['cmd']}")

            # Use shell=True to support commands with cd and &&
            if args.log_dir:
                out = open(os.path.join(args.log_dir, f"server-{i+1}.log"), 'wb')
                log_files.append(out)
            else:
                out = subprocess.DEVNULL
            process = subprocess.Popen(
                server['cmd'],
                shell=True,
                stdout=out,
                stderr=subprocess.STDOUT if args.log_dir else subprocess.DEVNULL,
                start_new_session=True,  # own process group, killed as a group below
            )
            server_processes.append(process)

            # Wait for this server to be ready
            print(f"Waiting for server on port {server['port']}...")
            if not is_server_ready(server['port'], timeout=args.timeout):
                raise RuntimeError(f"Server failed to start on port {server['port']} within {args.timeout}s")

            print(f"Server ready on port {server['port']}")

        print(f"\nAll {len(servers)} server(s) ready")

        # Run the command
        print(f"Running: {' '.join(args.command)}\n")
        result = subprocess.run(args.command)
        sys.exit(result.returncode)

    finally:
        # Clean up all servers
        print(f"\nStopping {len(server_processes)} server(s)...")
        for i, process in enumerate(server_processes):
            try:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=5)
            except ProcessLookupError:
                pass
            except subprocess.TimeoutExpired:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait()
            print(f"Server {i+1} stopped")
        for f in log_files:
            f.close()
        print("All servers stopped")


if __name__ == '__main__':
    main()