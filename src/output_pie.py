import os
import plotly.express as px

def output_pie(
        top_artists,
        top_songs,
        top_albums,
        sort_by_time,
        image_types,
        show_graphs
):
    values = "time_listened" if sort_by_time else "listens"

    # Top artists graph.
    fig1 = make_graph(top_artists, values, None)
    save_graph(fig1, "Top Artists", image_types)

    # Top songs graph.
    fig2 = make_graph(top_songs, values, "artist")
    save_graph(fig2, "Top Songs", image_types)

    # Top albums graph.
    fig3 = make_graph(top_albums, values, "artist")
    save_graph(fig3, "Top Albums", image_types)

    if show_graphs:
        fig1.show()
        fig2.show()

def make_graph(data, values, color):
    graph = px.pie(
            data,
            values     = values,
            names      = "name",
            color      = color,
            hole       = 0.2,
            template   = "plotly_dark",
            width      = 1920,
            height     = 1080,
            labels     = {"time_listened": "time listened (ms)"},
            hover_name = color
    )
    graph.update_traces(textinfo = "percent+label", textposition = "inside")
    graph.update_layout(uniformtext_minsize = 14, uniformtext_mode = "hide")
    return graph

def save_graph(graph, name, image_types):
    if "png" in image_types:
        path = os.path.join("output", name + ".png")
        graph.write_image(path)
    if "svg" in image_types:
        path = os.path.join("output", name + ".svg")
        graph.write_image(path)
