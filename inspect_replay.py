from pathlib import Path

replay_path = Path('/mnt/c/Users/vegas/OneDrive/Documents/Assetto Corsa/replay/temp/AC_171126-193711_O_ogp_superdoof_bmw_e46_pt_bihoku_highland_pt_bihoku_highland.acreplay')

with replay_path.open("rb") as replay_file:
    header = replay_file.read(4)
    weather = replay_file.read(12)
    weather_length = int.from_bytes(weather[8:12], byteorder="little")
    weather_name_bytes = replay_file.read(weather_length)
    weather_name = weather_name_bytes.decode("utf-8")

print(f"Weather bytes: {weather} length: {len(weather)}")

print(f"Bytes read: {len(header)}")

version = int.from_bytes(header, byteorder="little")
print(f"Version: {version}")


print(f"Weather length: {weather_length}")
print(f"Weather name: {weather_name}")