import os
import json
from operator import itemgetter

def get_artist_data(folder, filenames, extended_history):
    """Return a dict containing artist stats and song data."""
    artist_data = {}
    for file in filenames:
        path = os.path.join(folder, file)
        with open(path, "r", encoding="UTF-8") as f:
            data = json.load(f)

        for listen in data:
            if extended_history:
                artist_name = listen["master_metadata_album_artist_name"]
                track_name = listen["master_metadata_track_name"]
            else:
                artist_name = listen["artistName"]
                track_name = listen["trackName"]

            if artist_name is None:
                artist_name = "- Unknown Artist -"

            if track_name is None:
                track_name = "- Unknown Song -"

            # Check if the artist is already in the dictionary.
            try:
                artist_data[artist_name]
            except KeyError:
                artist_data[artist_name] = {
                    "name": artist_name,
                    "listens": 0,
                    "time_listened": 0,
                    "song_data": {}
                }

            # Add a listen to the artist that made the song.
            artist_data[artist_name]["listens"] += 1

            # Get the milliseconds that the song was played for.
            if extended_history:
                listen_time = listen["ms_played"]
            else:
                listen_time = listen["msPlayed"]

            # Add that time to the artist's listen time.
            artist_data[artist_name]["time_listened"] += listen_time

            song_data = artist_data[artist_name]["song_data"]
            # Try to add a listen and the listen time to the song's data.
            try:
                song_data[track_name]["listens"] += 1
                song_data[track_name]["time_listened"] += listen_time
            except KeyError:
                song_data[track_name] = {
                    "artist": artist_name,
                    "name": track_name,
                    "listens": 1,
                    "time_listened": listen_time
                }

    return artist_data

def get_top_artists(artist_data, threshold, hide_other):
    """Return a list of artists sorted by most listens."""
    filtered = []
    other = {
        "name": "- Other -",
        "listens": 0,
        "time_listened": 0,
        "song_data": {}
    }

    for artist_stats in artist_data.values():
        if artist_stats["listens"] >= threshold:
            filtered.append(artist_stats)
        else:
            other["listens"] += artist_stats["listens"]
            other["time_listened"] += artist_stats["time_listened"]
            other["song_data"] |= artist_stats["song_data"]

    # Put other in even if it's below the threshold.
    if other["listens"] > 0 and not hide_other:
        filtered.append(other)

    filtered.sort(key=itemgetter("time_listened"), reverse=True)
    return sorted(filtered, key=itemgetter("listens"), reverse=True)

def get_top_songs(artist_data, threshold, hide_other):
    """Return a list of songs sorted by most to least listens."""
    filtered = []
    other = {
        "artist": "- Various Artists -",
        "name": "- Other -",
        "listens": 0,
        "time_listened": 0
    }

    for artist_stats in artist_data.values():
        for song_stats in artist_stats["song_data"].values():
            if song_stats["listens"] >= threshold:
                filtered.append(song_stats)
            else:
                other["listens"] += song_stats["listens"]
                other["time_listened"] += song_stats["time_listened"]

    # Put other in even if it's below the threshold.
    if other["listens"] > 0 and not hide_other:
        filtered.append(other)

    filtered.sort(key=itemgetter("time_listened"), reverse=True)
    return sorted(filtered, key=itemgetter("listens"), reverse=True)
