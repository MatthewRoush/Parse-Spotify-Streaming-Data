# Parse-Spotify-Streaming-Data
Parse Spotify streaming data files and export data in various formats.

## Dependencies
[plotly](https://pypi.org/project/plotly/) for exporting data as a bar or pie graph.

## Usage
This is a command-line script that parses your .json streaming history files, which you can [download from Spotify](https://www.spotify.com/account/privacy/)

It exports top artists data, which are the most listened to artists in your streaming history files, with the option to show a number of their top songs. It also exports top songs data, which are the most listened to songs in your streaming history files.

All artists and songs are sorted by most to least listens.

A threshold can be set that will combine artists and songs with fewer listens than it into an "Other" category within the artist and song data sets.

It can export data as a .txt, .csv, .png bar graph, or .png pie graph.

The number of artists, songs per artist, number of songs (in top songs data), and the threshold for minimum listens can all be manually set.

Use `main.py -h` for more detailed information on arguments.
