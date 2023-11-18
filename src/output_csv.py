import os
import io
from tools import *

def output_csv(top_artists, top_songs, top_albums):
    """Output data as a csv file."""

    top_artists_output = generate_output(top_artists, "Artist")
    path = os.path.join("output", "Top Artists.csv")
    with open(path, "w", encoding="UTF-8") as f:
        f.write(top_artists_output)

    top_songs_output = generate_output(top_songs, "Song", True)
    path = os.path.join("output", "Top Songs.csv")
    with open(path, "w", encoding="UTF-8") as f:
        f.write(top_songs_output)

    if top_albums:
        top_albums_output = generate_output(top_albums, "Album", True)
        path = os.path.join("output", "Top Albums.csv")
        with open(path, "w", encoding="UTF-8") as f:
            f.write(top_albums_output)

def generate_output(data, name, list_artist = False):
    output = io.StringIO()
    output.write(f"{name},Listens,Time Listened,Days Listened")
    if list_artist:
        output.write(",Artist")
    output.write("\n")

    for i, stats in enumerate(data):
        output.write(get_line(i, stats, list_artist))
    return output.getvalue()

def get_line(index, data, list_artist):
    line = f"\"{index + 1}. {data['name']}\",{data['listens']},{ms_to_readable(data['time_listened'])},{data['days_listened']}"
    if list_artist:
        line += f",\"{data['artist']}\""
    return line + "\n"
