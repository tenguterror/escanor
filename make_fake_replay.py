from pathlib import Path

fake_replay_path = Path('data/private/fake_replay.acreplay')

version_bytes = (16).to_bytes(4, byteorder="little")
mystery_bytes = bytes(8)
weather_name = "tengu_lionheart_extra_long_weather_name!"
weather_name_bytes = weather_name.encode("utf-8")
weather_length_bytes = len(weather_name_bytes).to_bytes(4, byteorder="little")


with fake_replay_path.open("wb") as fake_replay_file:
    bytes_written = fake_replay_file.write(version_bytes)
    mystery_bytes_written = fake_replay_file.write(mystery_bytes)
    weather_length_written = fake_replay_file.write(weather_length_bytes)
    weather_name_written = fake_replay_file.write(weather_name_bytes)
