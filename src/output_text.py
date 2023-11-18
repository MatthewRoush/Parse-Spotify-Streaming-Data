import os
import io
from tools import *

def output_text(top_artists, top_songs, top_albums, date_range):
    """Output data a plaintext file."""

    max_artist_index = len(str(len(top_artists)))

    first_date, last_date = date_range
    header = f"Data from {format_date(first_date)} to {format_date(last_date)}\n\n"

    padding = get_padding(top_artists)

    top_artists_output = io.StringIO()
    top_artists_output.write(header)

    indent = " " * (padding["max_index"] + 2) + "  "
    for i, artist_stats in enumerate(top_artists):
        top_artists_output.write(
            get_line(
                index             = str(i + 1),
                name              = pad_name(artist_stats["name"], padding["max_name"], i),
                listens           = pretty(artist_stats["listens"]),
                time_listened     = ms_to_readable(artist_stats["time_listened"]),
                days_listened     = str(artist_stats["days_listened"]),
                max_index_len     = padding["max_index"],
                max_listens       = padding["max_listens_len"],
                max_time_listened = padding["max_time_listened_len"],
                max_days_listened = padding["max_days_len"],
                pad_r             = indent
            ).rstrip()
        )

        # Albums
        albums = artist_stats["album_data"]
        if len(albums) > 0:
            top_artists_output.write(f"\n{indent}--- Albums ---\n")

        max_artist_album_index = len(str(len(albums)))
        for k, album_stats in enumerate(albums):
            top_artists_output.write(
                get_line(
                    index             = str(k + 1),
                    name              = pad_name(album_stats["name"], padding["max_name"], k),
                    listens           = pretty(album_stats["listens"]),
                    time_listened     = ms_to_readable(album_stats["time_listened"]),
                    days_listened     = str(album_stats["days_listened"]),
                    max_index_len     = max_artist_album_index,
                    max_listens       = padding["max_listens_len"],
                    max_time_listened = padding["max_time_listened_len"],
                    max_days_listened = padding["max_days_len"],
                    pad_l             = indent
                )
            )

        # Songs
        songs = artist_stats["song_data"]
        if len(songs) > 0:
            top_artists_output.write(f"\n{indent}--- Songs ---\n")

        max_artist_song_index = len(str(len(songs)))
        for k, song_stats in enumerate(songs):
            top_artists_output.write(
                get_line(
                    index             = str(k + 1),
                    name              = pad_name(song_stats["name"], padding["max_name"], k),
                    listens           = pretty(song_stats["listens"]),
                    time_listened     = ms_to_readable(song_stats["time_listened"]),
                    days_listened     = str(song_stats["days_listened"]),
                    max_index_len     = max_artist_song_index,
                    max_listens       = padding["max_listens_len"],
                    max_time_listened = padding["max_time_listened_len"],
                    max_days_listened = padding["max_days_len"],
                    pad_l             = indent
                )
            )

        top_artists_output.write("\n")

    top_artists_output = top_artists_output.getvalue()

    path = os.path.join("output", "Top Artists.txt")
    with open(path, "w", encoding="UTF-8") as f:
        f.write(top_artists_output)

    top_songs_output = generate_output(top_songs, header)
    path = os.path.join("output", "Top Songs.txt")
    with open(path, "w", encoding="UTF-8") as f:
        f.write(top_songs_output)

    if top_albums:
        top_albums_output = generate_output(top_albums, header)
        path = os.path.join("output", "Top Albums.txt")
        with open(path, "w", encoding="UTF-8") as f:
            f.write(top_albums_output)

def generate_output(data, header):
    padding = get_padding(data)

    output = io.StringIO()
    output.write(header)

    for i, stats in enumerate(data):
        output.write(
            get_line(
                index             = str(i + 1),
                name              = pad_name(stats["name"], padding["max_name"], i),
                listens           = pretty(stats["listens"]),
                time_listened     = ms_to_readable(stats["time_listened"]),
                days_listened     = str(stats["days_listened"]),
                max_index_len     = padding["max_index"],
                max_listens       = padding["max_listens_len"],
                max_time_listened = padding["max_time_listened_len"],
                max_days_listened = padding["max_days_len"],
                artist            = stats["artist"]
            )
        )

    return output.getvalue()

def get_padding(data):
    max_index             = len(str(len(data)))
    max_name              = 0
    max_listens_len       = 0
    max_time_listened_len = 0
    max_days_len          = 0
    for i, stats in enumerate(data):
        if "song_data" in stats:
            song_padding = get_padding(stats["song_data"])
            album_padding = get_padding(stats["album_data"])
        else:
            song_padding = False
            album_padding = False

        max_name = max(
                max_name,
                max_index + len(stats["name"]),
                song_padding["max_name"] if song_padding else 0,
                album_padding["max_name"] if album_padding else 0
        )
        max_listens_len = max(
                max_listens_len,
                len(pretty(stats["listens"])),
                song_padding["max_listens_len"] if song_padding else 0,
                album_padding["max_listens_len"] if album_padding else 0
        )
        max_time_listened_len = max(
                max_time_listened_len,
                len(ms_to_readable(stats["time_listened"])),
                song_padding["max_time_listened_len"] if song_padding else 0,
                album_padding["max_time_listened_len"] if album_padding else 0
        )
        max_days_len = max(
                max_days_len,
                len(str(stats["days_listened"])),
                song_padding["max_days_len"] if song_padding else 0,
                album_padding["max_days_len"] if album_padding else 0
        )

    return {
            "max_index": max_index,
            "max_name": max_name,
            "max_listens_len": max_listens_len,
            "max_time_listened_len": max_time_listened_len,
            "max_days_len": max_days_len
    }

def pad_name(name, max_name_length, index):
    padding = max_name_length - len(str(index + 1) + name)
    return name + " " * padding

def get_line(
        index,
        name,
        listens,
        time_listened,
        days_listened,
        max_index_len,
        max_listens,
        max_time_listened,
        max_days_listened,
        pad_l  = "",
        pad_r  = "",
        artist = None
):
    list_pad = " " * (max_listens - len(listens))
    time_pad = " " * (max_time_listened - len(time_listened))
    day_pad  = " " * (max_days_listened - len(days_listened))

    index_pad_len = max_index_len - len(index)
    index_pad = " " * index_pad_len
    if index_pad_len > 0:
        name = name[:index_pad_len * -1]

    sep = "  |  "
    line = (
        f"{pad_l}{index_pad}{index}. {name}{pad_r} : "
        f"Listens = {list_pad}{listens}{sep}"
        f"Time = {time_pad}{time_listened}{sep}"
        f"Days Listened = {day_pad}{days_listened}"
    )

    if artist is not None:
        line += f"{sep}By {artist}"
    return line + "\n"
