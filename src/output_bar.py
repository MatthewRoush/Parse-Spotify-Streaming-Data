import os
import plotly.express as px
from tools import *

def output_bar(sorted_artists, top_songs_list, num_artists, num_songs):
    """Output data as a bar graph."""
    # Top artists graph.
    artist_data = sorted_artists[:num_artists]

    # Scale width to the number of artists.
    x1 = len(artist_data)
    width1 = translate_width(x1)
    # Scale height to the number of listens.
    x2 = sorted_artists[0]["listens"]
    height1 = translate_height(x2)

    fig1 = px.bar(artist_data, x="name", y="listens", template="plotly_dark",
                  title="Artists by most to least listens.",
                  width=width1, height=height1)

    tickangle = 50
    fig1.update_xaxes(tickangle=tickangle)
    vals, text = get_y_tick_vals_text(height1, x2)
    fig1.update_yaxes(tickvals=vals, ticktext=text)

    path = os.path.join("output", "Top Artists Bar Graph.png")
    fig1.write_image(path)

    # Top songs graph.
    song_data = top_songs_list[:num_songs]

    # Scale width to the number of songs.
    x3 = len(song_data)
    width2 = translate_width(x3)
    # Scale height to the number of listens.
    x4 = top_songs_list[0]["listens"]
    height2 = translate_height(x4)

    fig2 = px.bar(song_data, x="name", y="listens", template="plotly_dark",
                  title="Songs by most to least listens.",
                  width=width2, height=height2)

    fig2.update_xaxes(tickangle=tickangle)
    vals, text = get_y_tick_vals_text(height2, x4)
    fig2.update_yaxes(tickvals=vals, ticktext=text)

    path = os.path.join("output", "Top Songs Bar Graph.png")
    fig2.write_image(path)

def translate_width(val):
    """Scale the graph width to fit the data."""
    return int(400 + val * 20)

def translate_height(val):
    """Scale the graph height to fit the data."""
    return int(400 + val / 10)

def get_y_tick_vals_text(img_h, max_y):
    """Get values and text for the y ticks."""
    num_ticks = int(img_h / 100)
    vals = [int((max_y / num_ticks) * x) for x in range(num_ticks + 1)]
    text = [pretty(val) for val in vals]
    return vals, text
