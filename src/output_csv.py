import os
import io
from tools import *

def output_csv(sorted_artists, top_songs_list, num_artists,
               num_songs_per_artist, num_songs):
    """Output data as a csv file."""
    top_artists_output = io.StringIO()

    header = "Artist / Song,Listens,Time Listened\n"
    top_artists_output.write(header)

    for i, artist_stats in enumerate(sorted_artists[:num_artists]):
        top_artists_output.write(f"\"{i + 1}. {artist_stats['name']}\",")
        top_artists_output.write(f"\"{pretty(artist_stats['listens'])}\",")
        top_artists_output.write(
            ms_to_readable(artist_stats["time_listened"]) + "\n")

        k = 0
        for song_stats in top_songs_list:
            # Continue if the song isn't by the current artist.
            if song_stats["artist"] != artist_stats["name"]:
                continue

            top_artists_output.write(f"\"{k+ 1}. {song_stats['name']}\",")
            top_artists_output.write(f"\"{pretty(song_stats['listens'])}\",")
            top_artists_output.write(
                ms_to_readable(song_stats["time_listened"]) + "\n")

            k += 1
            if k == num_songs_per_artist:
                break

        top_artists_output.write("\n")

    top_artists_output = top_artists_output.getvalue()

    top_songs_output = io.StringIO()

    header = "Song,Listens,Time Listened,Artist\n"
    top_songs_output.write(header)

    for i, song_stats in enumerate(top_songs_list[:num_songs]):
        top_songs_output.write(f"\"{i + 1}. {song_stats['name']}\",")
        top_songs_output.write(f"\"{pretty(song_stats['listens'])}\",")
        top_songs_output.write(
            ms_to_readable(song_stats["time_listened"]) + ",")
        top_songs_output.write(f"\"{song_stats['artist']}\"\n")

    top_songs_output = top_songs_output.getvalue()

    path = os.path.join("output", "Top Artists.csv")
    with open(path, "w", encoding="UTF-8") as f:
        f.write(top_artists_output)

    path = os.path.join("output", "Top Songs.csv")
    with open(path, "w", encoding="UTF-8") as f:
        f.write(top_songs_output)
