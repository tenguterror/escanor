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
    header = replay_file.read(52)

if len(header) < 52:
    print(f"Error: Incomplete replay header. Expected 52 bytes, got {len(header)}.")
    sys.exit(1)

print(f"Bytes read: {len(header)}")
print(f"Header: {header.hex(' ')}")

version = int.from_bytes(header[:4], byteorder="little")
print(f"Replay version: {version}")

weather_length = int.from_bytes(header[12:16], byteorder="little")
print(f"Weather string length: {weather_length}")

weather_name = header[16:16 + weather_length].decode("utf-8")
print(f"Weather preset: {weather_name}")

track_offset = 16 + weather_length

track_length = int.from_bytes(
    header[track_offset:track_offset + 4],
    byteorder="little"
)

track_start = track_offset + 4
track_name = header[track_start:track_start + track_length].decode("utf-8")
print(f"Track name: {track_name}")

