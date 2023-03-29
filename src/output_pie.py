import os
import plotly.express as px

def output_pie(sorted_artists, top_songs_list, num_artists, num_songs):
    # Top artists graph.
    artist_data = sorted_artists[:num_artists]

    hole = 0.2
    width = 2000
    height = 1000
    template = "plotly_dark"
    textinfo = "percent+label"

    fig1 = px.pie(artist_data, values="listens", names="name", hole=hole,
                  template=template, width=width, height=height)
    fig1.update_traces(textinfo=textinfo)
    
    path = os.path.join("output", "Top Artists Pie Graph.png")
    fig1.write_image(path)

    # Top songs graph.
    song_data = top_songs_list[:num_songs]

    fig2 = px.pie(song_data, values="listens", names="name", hole=hole,
                  template=template, width=width, height=height)
    fig2.update_traces(textinfo=textinfo)
    
    path = os.path.join("output", "Top Songs Pie Graph.png")
    fig2.write_image(path)
