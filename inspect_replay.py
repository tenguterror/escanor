import sys
from pathlib import Path

if len(sys.argv) != 2:
    print("Usage: python3 inspect_replay.py <replay_file>")
    sys.exit(1)

replay_path = Path(sys.argv[1])

if not replay_path.is_file():
    print(f"Error: Replay file not found: {replay_path}")
    sys.exit(1)

with replay_path.open("rb") as replay_file:
    header = replay_file.read(32)

if len(header) < 32:
    print(f"Error: Incomplete replay header. Expected 32 bytes, got {len(header)}.")
    sys.exit(1)

print(f"Bytes read: {len(header)}")
print(f"Header: {header.hex(' ')}")

version = int.from_bytes(header[:4], byteorder="little")
print(f"Replay version: {version}")
