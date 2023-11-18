import os
import json
from datetime import date
from unicodedata import normalize
from operator import itemgetter
from tools import get_amount

def get_artist_data(
        folder,
        filenames,
        ext_hist,
        threshold,
        num_artists,
        songs_per,
        albums_per,
        num_songs,
        num_albums,
        hide_other,
        sort_by_time
):
    """Return a dict containing artist stats and song data."""
    date_range_start = None
    date_range_end = None
    artist_data = {}
    for file in filenames:
        path = os.path.join(folder, file)
        with open(path, "r", encoding="UTF-8") as f:
            data = json.load(f)

        for listen in data:
            if ext_hist:
                artist_name = listen["master_metadata_album_artist_name"]
                track_name = listen["master_metadata_track_name"]
                listen_time = listen["ms_played"]
                listen_date = to_date(listen["ts"], True)
                album_name = listen["master_metadata_album_album_name"]
            else:
                artist_name = listen["artistName"]
                track_name = listen["trackName"]
                listen_time = listen["msPlayed"]
                listen_date = to_date(listen["endTime"], False)
                album_name = None # Very sad

            if date_range_start is None:
                date_range_start = listen_date
            else:
                date_range_start = min(date_range_start, listen_date)

            if date_range_end is None:
                date_range_end = listen_date
            else:
                date_range_end = max(date_range_end, listen_date)

            # Extended history, not a song, probably podcast.
            if artist_name is None:
                continue

            # If you don't normalize then len(name) can be different than the actual number of characters.
            artist_name = normalize("NFC", artist_name)
            track_name = normalize("NFC", track_name)

            # Artist data
            if artist_name in artist_data:
                data = artist_data[artist_name]
                data["listens"] += 1
                data["time_listened"] += listen_time
                data["first_listen"] = min(data["first_listen"], listen_date)
                data["last_listen"] = max(data["last_listen"], listen_date)
                data["days_listened"][listen_date] = None
            else:
                artist_data[artist_name] = {
                    "name": artist_name,
                    "listens": 1,
                    "time_listened": listen_time,
                    "first_listen": listen_date,
                    "last_listen": listen_date,
                    "song_data": [],
                    "album_data": [],
                    "song_data_index_table": {},
                    "album_data_index_table": {},
                    "days_listened": {listen_date: None}
                }

            # Song data
            song_data = artist_data[artist_name]["song_data"]
            song_data_index_table = artist_data[artist_name]["song_data_index_table"]
            manage_sub_data(
                    artist_name,
                    track_name,
                    listen_time,
                    listen_date,
                    song_data,
                    song_data_index_table
            )

            # Album data
            if album_name is not None:
                album_name = normalize("NFC", album_name)

                album_data = artist_data[artist_name]["album_data"]
                album_data_index_table = artist_data[artist_name]["album_data_index_table"]
                manage_sub_data(
                        artist_name,
                        album_name,
                        listen_time,
                        listen_date,
                        album_data,
                        album_data_index_table
                )

    for data in artist_data.values():
        sort_list(data["song_data"], sort_by_time)
        del data["song_data_index_table"]

        sort_list(data["album_data"], sort_by_time)
        del data["album_data_index_table"]

    top_songs = get_sub_data(
            artist_data,
            "song_data",
            threshold,
            hide_other,
            sort_by_time
    )
    top_songs = top_songs[:get_amount(len(top_songs), num_songs)]

    top_albums = get_sub_data(
            artist_data,
            "album_data",
            threshold,
            hide_other,
            sort_by_time
    )
    top_albums = top_albums[:get_amount(len(top_albums), num_albums)]

    top_artists = get_top_artists(
            artist_data,
            threshold,
            hide_other,
            sort_by_time
    )
    top_artists = top_artists[:get_amount(len(top_artists), num_artists)]
    for artist in top_artists:
        songs = artist["song_data"]
        artist["song_data"] = songs[:get_amount(len(songs), songs_per)]
        albums = artist["album_data"]
        artist["album_data"] = albums[:get_amount(len(albums), albums_per)]

    return (
            top_artists,
            top_songs,
            top_albums,
            (date_range_start, date_range_end)
    )

def get_top_artists(artist_data, threshold, hide_other, sort_by_time):
    """Return a list of artists sorted by most listens."""
    filtered = []
    other = {
        "name": "- Various Artists -",
        "listens": 0,
        "time_listened": 0,
        "first_listen": None,
        "last_listen": None,
        "song_data": [],
        "album_data": [],
        "days_listened": {}
    }

    for artist_stats in artist_data.values():
        if artist_stats["listens"] >= threshold:
            filtered.append(artist_stats)
        elif not hide_other:
            combine_into_other(other, artist_stats)
            other["song_data"] += artist_stats["song_data"]
            other["album_data"] += artist_stats["album_data"]

        artist_stats["days_listened"] = len(artist_stats["days_listened"])

    # Put other in even if it's below the threshold.
    if other["listens"] > 0:
        other["days_listened"] = len(other["days_listened"])
        sort_list(other["song_data"], sort_by_time)
        filtered.append(other)

    return sort_list(filtered, sort_by_time)

def get_top_songs(artist_data, threshold, hide_other, sort_by_time):
    """Return a list of songs sorted by most to least listens."""
    filtered = []
    other = {
        "artist": "- Various Artists -",
        "name": "- Other -",
        "listens": 0,
        "time_listened": 0,
        "first_listen": None,
        "last_listen": None,
        "days_listened": {}
    }

    for artist_stats in artist_data.values():
        for song_stats in artist_stats["song_data"]:
            if song_stats["listens"] >= threshold:
                filtered.append(song_stats)
            elif not hide_other:
                combine_into_other(other, song_stats)

            song_stats["days_listened"] = len(song_stats["days_listened"])

    # Put other in even if it's below the threshold.
    if other["listens"] > 0:
        other["days_listened"] = len(other["days_listened"])
        filtered.append(other)

    return sort_list(filtered, sort_by_time)

def get_sub_data(artist_data, data_key, threshold, hide_other, sort_by_time):
    filtered = []
    other = {
        "artist": "- Various Artists -",
        "name": "- Other -",
        "listens": 0,
        "time_listened": 0,
        "first_listen": None,
        "last_listen": None,
        "days_listened": {}
    }

    for artist_stats in artist_data.values():
        for data in artist_stats[data_key]:
            if data["listens"] >= threshold:
                filtered.append(data)
            elif not hide_other:
                combine_into_other(other, data)

            data["days_listened"] = len(data["days_listened"])

    # Put other in even if it's below the threshold.
    if other["listens"] > 0:
        other["days_listened"] = len(other["days_listened"])
        filtered.append(other)

    return sort_list(filtered, sort_by_time)

def combine_into_other(other, main_stats):
    other["listens"] += main_stats["listens"]
    other["time_listened"] += main_stats["time_listened"]

    if other["first_listen"] is None:
        other["first_listen"] = main_stats["first_listen"]
        other["last_listen"] = main_stats["last_listen"]
    else:
        other["first_listen"] = min(other["first_listen"], main_stats["first_listen"])
        other["last_listen"] = max(other["last_listen"], main_stats["last_listen"])

    other["days_listened"] |= main_stats["days_listened"]

def sort_list(arr, sort_by_time):
    if sort_by_time:
        arr.sort(key=itemgetter("listens"), reverse=True)
        arr.sort(key=itemgetter("time_listened"), reverse=True)
    else:
        arr.sort(key=itemgetter("time_listened"), reverse=True)
        arr.sort(key=itemgetter("listens"), reverse=True)

    return arr

def to_date(string, extended):
    if extended:
        sep = "T"
    else:
        sep = " "
    return date(*[int(x) for x in string.split(sep)[0].split("-")])

def manage_sub_data(
        artist_name,
        name,
        listen_time,
        listen_date,
        data_list,
        index_table
):
    if name in index_table:
        index = index_table[name]
        data = data_list[index]
        data["listens"] += 1
        data["time_listened"] += listen_time
        data["first_listen"] = min(data["first_listen"], listen_date)
        data["last_listen"] = max(data["last_listen"], listen_date)
        data["days_listened"][listen_date] = None
    else:
        index_table[name] = len(data_list)
        data_list.append(
            {
                "artist": artist_name,
                "name": name,
                "listens": 1,
                "time_listened": listen_time,
                "first_listen": listen_date,
                "last_listen": listen_date,
                "days_listened": {listen_date: None}
            }
        )
