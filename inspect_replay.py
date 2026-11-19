from pathlib import Path

replay_path = Path('/mnt/c/Users/vegas/OneDrive/Documents/Assetto Corsa/replay/temp/AC_171126-193711_O_ogp_superdoof_bmw_e46_pt_bihoku_highland_pt_bihoku_highland.acreplay')

with replay_path.open("rb") as replay_file:
    header = replay_file.read(4)

print(f"Bytes read: {len(header)}")

version = int.from_bytes(header, byteorder="little")
print(f"Version: {version}")