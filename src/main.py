import os
import sys
import argparse
from get_data import get_artist_data, get_top_artists, get_top_songs
from tools import *
from output_text import output_text
from output_csv import output_csv
from output_pie import output_pie

def main():
    parser = argparse.ArgumentParser(description = "Parse Spotify data files. Album data is only available in extended streaming history data.")

    parser.add_argument(
        "-p", "--path",
        help  = "Path to folder or file. If left empty then try to use the last path that was used."
    )

    parser.add_argument(
        "-e", "--extended",
        action = "store_true",
        help   = "Parse extended streaming history."
    )

    parser.add_argument(
        "-x", "--hide_other",
        action = "store_true",
        help   = "Hide the 'other' category when it's present in the data."
    )

    parser.add_argument(
        "-b", "--sort-by-time",
        action = "store_true",
        help   = "Sort by time listened instead of number of listens."
    )

    parser.add_argument(
        "-a", "--artists",
        type    = int,
        default = 10,
        help    = "Number of artists to use for the top artists output. Defaults to %(default)s. Set to -1 for max."
    )

    parser.add_argument(
        "-n", "--songs-per",
        type    = int,
        default = 3,
        help    = "Number of songs to list under each artist. Defaults to %(default)s. Set to -1 for max. Not used for graphs."
    )

    parser.add_argument(
        "-m", "--albums-per",
        type    = int,
        default = 1,
        help    = "Number of albums to list under each artist. Defaults to %(default)s. Set to -1 for max. Not used for graphs."
    )

    parser.add_argument(
        "-s", "--songs",
        type    = int,
        default = 50,
        help    = "Number of songs to list in the top songs output. Defaults to %(default)s. Set to -1 for max."
    )

    parser.add_argument(
        "-u", "--albums",
        type    = int,
        default = 15,
        help    = "Number of albums to list in the top albums output. Defaults to %(default)s. Set to -1 for max."
    )

    parser.add_argument(
        "-t", "--threshold",
        type    = int,
        default = 10,
        help    = "Only artists, songs, and albums with at least this many listens will be included in the data. Defaults to %(default)s."
    )

    parser.add_argument(
        "-o", "--output",
        default = ["text"],
        nargs   = "*",
        choices = ["text", "csv", "pie", "all"],
        help    = "The output type for the data. Defaults to %(default)s."
    )

    parser.add_argument(
        "-i", "--image-type",
        default = ["png"],
        nargs   = "*",
        choices = ["png", "svg", "all"],
        help    = "The image type to save the pie graphs as. Defaults to %(default)s."
    )

    parser.add_argument(
        "-g", "--interactive-graphs",
        action = "store_true",
        help   = "Open interactive graphs in the default web browser."
    )

    args = parser.parse_args()

    saved_path_file_name = "last_used_path.txt"
    last_used_path = get_last_used_path(saved_path_file_name)

    # Verify path.
    if args.path is None:
        if last_used_path is not None:
            folder_path = last_used_path
        else:
            print("There is no saved path, so --path can't be left empty.")
            sys.exit(1)
    else:
        folder_path = args.path

    if not os.path.exists(folder_path):
        print(f"Path does not exist, '{folder_path}'")
        sys.exit(1)

    extended_history      = args.extended
    num_artists           = args.artists
    num_songs_per_artist  = args.songs_per
    num_albums_per_artist = args.albums_per
    num_songs             = args.songs
    num_albums            = args.albums
    threshold             = args.threshold
    output_types          = args.output
    hide_other            = args.hide_other
    sort_by_time          = args.sort_by_time
    image_types           = args.image_type
    show_graphs           = args.interactive_graphs

    if "all" in output_types:
        output_types = ["text", "csv", "pie"]

    if "all" in image_types:
        image_types = ["png", "svg"]

    data_files = []
    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            if extended_history:
                # Extended streaming history files start with "endsong".
                if filename.startswith("endsong"):
                    data_files.append(filename)
            else:
                # User account data files containing listening history start with "StreamingHistory".
                if filename.startswith("StreamingHistory"):
                    data_files.append(filename)

    save_path(saved_path_file_name, folder_path)

    print("\nCollecting Data...")

    # Get artist data.
    top_artists, top_songs, top_albums, date_range = get_artist_data(
            folder       = folder_path,
            filenames    = data_files,
            ext_hist     = extended_history,
            threshold    = threshold,
            num_artists  = num_artists,
            songs_per    = num_songs_per_artist,
            albums_per   = num_albums_per_artist,
            num_songs    = num_songs,
            num_albums   = num_albums,
            hide_other   = hide_other,
            sort_by_time = sort_by_time
    )

    # Make sure there's an output folder.
    if not os.path.exists("output"):
        os.mkdir("output")

    print("\nCreating Output Files...")

    if "text" in output_types:
        output_text(
            top_artists,
            top_songs,
            top_albums,
            date_range
        )
    if "csv" in output_types:
        output_csv(
            top_artists,
            top_songs,
            top_albums
        )
    if "pie" in output_types:
        output_pie(
            top_artists,
            top_songs,
            top_albums,
            sort_by_time,
            image_types,
            show_graphs
        )

    print("\nData Exported.")

if __name__ == "__main__":
    main()
