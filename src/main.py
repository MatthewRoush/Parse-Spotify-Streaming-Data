import os
import sys
import argparse
from get_data import (get_artist_data, get_top_artists, get_top_songs)
from tools import *
from output_text import output_text
from output_bar import output_bar
from output_csv import output_csv
from output_pie import output_pie

def main():
    parser = argparse.ArgumentParser(
        prog = "main.py",
        description = "Parse Spotify data files.")

    parser.add_argument("-p", "--path",
                        help=("Path to folder or file. "
                              "Put in single or double quotes if the "
                              "path contains spaces. "
                              "If left empty then try to use the last path "
                              "that was used."))

    parser.add_argument("-e", "--extended",
                        action="store_true",
                        help=("Flag for parsing extended streaming history "
                              "files. Defaults to false."))

    parser.add_argument("-a", "--artists",
                        type=int,
                        default=10,
                        help=("Number of artists to use for the top artists "
                              "output. Defaults to 10. Set to -1 for max."))

    parser.add_argument("-i", "--songs-per",
                        type=int,
                        default=3,
                        help=("Number of songs to list under each artist. "
                              "Defaults to 3. Set to -1 for max. "
                              "Not used for graphs."))

    parser.add_argument("-s", "--songs",
                        type=int,
                        default=50,
                        help=("Number of songs to list in the top songs "
                              "output. Defaults to 50. Set to -1 for max."))

    parser.add_argument("-t", "--threshold",
                        type=int,
                        default=10,
                        help=("Only artists and songs with at least this "
                              "number of listens will be shown. "
                              "Defaults to 10."))

    parser.add_argument("-o", "--output",
                        default="text",
                        choices=["text", "csv", "bar", "pie", "all"],
                        help=("The output type for the data. Options are "
                              "'text', 'csv', 'bar', 'pie', and 'all'. "
                              "Defaults to text."))

    parser.add_argument("-x", "--hide_other",
                        action="store_true",
                        help=("Flag to hide the 'other' category "
                              "when it's present in the data."))

    args = parser.parse_args()

    saved_path_file_name = "last_used_path.txt"
    last_used_path = get_last_used_path(saved_path_file_name)

    # Verify path.
    if args.path is None:
        if last_used_path is not None:
            folder_path = last_used_path
        else:
            print("There is no saved path, so --path can't be left empty.")
            return
    else:
        folder_path = args.path

    if not os.path.exists(folder_path):
        print("Path does not exist.")
        return

    extended_history = args.extended
    num_artists = args.artists
    num_songs_per_artist = args.songs_per
    num_songs = args.songs
    threshold = args.threshold
    output_type = args.output.lower()
    hide_other = args.hide_other

    data_files = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if extended_history:
                # Extended streaming history files start with "endsong".
                if filename.startswith("endsong"):
                    data_files.append(filename)
            else:
                # User account data files containing listening history start
                # with "StreamingHistory".
                if filename.startswith("StreamingHistory"):
                    data_files.append(filename)

    save_path(saved_path_file_name, folder_path)

    print("\nCollecting Data...")

    # Get artist data.
    artist_data = get_artist_data(folder_path, data_files, extended_history)

    # Get a list of artist names sorted by most listens.
    sorted_artists = get_top_artists(artist_data, threshold, hide_other)

    # Get a list of all the songs by most listens.
    top_songs_list = get_top_songs(artist_data, threshold, hide_other)

    # Make sure the requested number of artists and songs are not greater than
    # the available number of artists and songs.
    if num_artists == -1:
        num_artists = len(sorted_artists) - 1
    elif num_artists > len(sorted_artists) - 1:
        num_artists = len(sorted_artists) - 1

    if num_songs == -1:
        num_songs = len(top_songs_list) - 1
    elif num_songs > len(top_songs_list) - 1:
        num_songs = len(top_songs_list) - 1

    # Make sure there's an output folder.
    if not os.path.exists("output"):
        os.mkdir("output")

    if output_type == "text":
        output_text(sorted_artists, top_songs_list, num_artists,
                    num_songs_per_artist, num_songs)
    elif output_type == "csv":
        output_csv(sorted_artists, top_songs_list, num_artists,
                   num_songs_per_artist, num_songs)
    elif output_type == "bar":
        output_bar(sorted_artists, top_songs_list, num_artists, num_songs)
    elif output_type == "pie":
        output_pie(sorted_artists, top_songs_list, num_artists, num_songs)
    elif output_type == "all":
        output_text(sorted_artists, top_songs_list, num_artists,
                    num_songs_per_artist, num_songs)

        output_csv(sorted_artists, top_songs_list, num_artists,
                   num_songs_per_artist, num_songs)

        output_bar(sorted_artists, top_songs_list, num_artists, num_songs)

        output_pie(sorted_artists, top_songs_list, num_artists, num_songs)
    else:
        print(f"Output type '{output_type}' is invalid.")
        return

    print("\nData Exported.")

if __name__ == "__main__":
    main()
