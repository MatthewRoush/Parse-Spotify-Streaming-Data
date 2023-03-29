import os
import io
from tools import *

def output_text(sorted_artists, top_songs_list, num_artists,
                num_songs_per_artist, num_songs):
    """Output data a plaintext file."""

    # Make the artist and song name fields about the same width.
    top_artist_max_name = 0
    for artist_stats in sorted_artists[:num_artists]:
        name_length = len(artist_stats["name"])
        if name_length > top_artist_max_name:
            top_artist_max_name = name_length

        i = 0 # Index.
        for song_stats in top_songs_list:
            # Continue if the song isn't by the current artist.
            if song_stats["artist"] != artist_stats["name"]:
                continue

            name_length = len(song_stats["name"])
            if name_length > top_artist_max_name:
                top_artist_max_name = name_length

            i += 1
            if i == num_songs_per_artist:
                break

    # Make the song name field about the same width.
    top_song_max_name = 0
    for song_stats in top_songs_list[:num_songs]:
        name_length = len(song_stats["name"])
        if name_length > top_song_max_name:
            top_song_max_name = name_length

    top_artists_output = io.StringIO()
    for i, artist_stats in enumerate(sorted_artists[:num_artists]):
        artist = artist_stats["name"]
        artist_listens = pretty(artist_stats["listens"])
        artist_time_listened = ms_to_readable(artist_stats["time_listened"])
        songs = artist_stats["song_data"]

        artist_name = artist
        empty_spaces = top_artist_max_name - len(artist)
        empty = io.StringIO()
        for _ in range(empty_spaces):
            empty.write(" ")

        artist_name += empty.getvalue()

        artist_line = (f"{i + 1}. {artist_name}: "
                       f"{{Listens = {artist_listens}}}, "
                       f"{{Time Listened = {artist_time_listened}}}\n")
        top_artists_output.write(artist_line)

        if num_songs_per_artist == -1:
            num_songs_per_artist = len(songs) - 1
        elif num_songs_per_artist > len(songs) - 1:
            num_songs_per_artist = len(songs) - 1

        k = 0 # Index.
        for song_stats in top_songs_list:
            # Continue if the song isn't by the current artist.
            if song_stats["artist"] != artist:
                continue

            song = song_stats["name"]
            song_listens = pretty(song_stats["listens"])
            song_time_listened = ms_to_readable(song_stats["time_listened"])

            song_name = song
            empty_spaces = top_artist_max_name - len(song)
            empty = io.StringIO()
            for _ in range(empty_spaces):
                empty.write(" ")

            song_name += empty.getvalue()

            song_line = (f"    {k + 1}. {song_name}: "
                         f"{{Listens = {song_listens}}}, "
                         f"{{Time Listened = {song_time_listened}}}\n")
            top_artists_output.write(song_line)

            k += 1
            if k == num_songs_per_artist:
                break

        top_artists_output.write("\n")

    top_artists_output = top_artists_output.getvalue()

    top_songs_output = io.StringIO()
    for i, song_stats in enumerate(top_songs_list[:num_songs]):
        song = song_stats["name"]
        artist = song_stats["artist"]
        listens = pretty(song_stats["listens"])
        time_listened = ms_to_readable(song_stats["time_listened"])

        song_name = song
        empty_spaces = top_song_max_name - len(song)
        empty = io.StringIO()
        for _ in range(empty_spaces):
            empty.write(" ")

        song_name += empty.getvalue()

        line = (f"{i + 1}. {song_name}: "
                f"{{Listens = {listens}}}, "
                f"{{Time Listened = {time_listened}}}, "
                f"{{By {artist}}}\n")
        top_songs_output.write(line)

    top_songs_output = top_songs_output.getvalue()

    path = os.path.join("output", "Top Artists.txt")
    with open(path, "w", encoding="UTF-8") as f:
        f.write(top_artists_output)

    path = os.path.join("output", "Top Songs.txt")
    with open(path, "w", encoding="UTF-8") as f:
        f.write(top_songs_output)
