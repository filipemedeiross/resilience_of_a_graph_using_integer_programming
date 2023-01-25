import networkx as nx
import matplotlib.pyplot as plt
from .constants import images, pos


# Auxiliary function to plot a water distribution network
def plot_water_network(network):
    fig, ax = plt.subplots(figsize=(18, 16))

    nx.draw_networkx_edges(network, pos, width=6, edge_color=nx.get_edge_attributes(network, "color").values())
    nx.draw_networkx_edge_labels(network, pos, {edge : str(edge) for edge in network.edges})

    tr_figure = ax.transData.transform
    tr_axes = fig.transFigure.inverted().transform

    icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.005
    icon_center = icon_size / 2.0

    for n in network.nodes:
        xf, yf = tr_figure(pos[n])
        xa, ya = tr_axes((xf, yf))

        a = plt.axes([xa - icon_center, ya - icon_center, icon_size, icon_size])

        a.imshow(network.nodes[n]["image"])
        a.axis("off")

    ax.axis("off")

    return fig

# Auxiliary function to plot a military distribution network
def plot_military_network(network):
    fig, ax = plt.subplots(figsize=(18, 16))

    nx.draw_networkx_edges(network, pos, width=6, edge_color="blue")
    nx.draw_networkx_edge_labels(network, pos, {edge : str(edge) for edge in network.edges})

    tr_figure = ax.transData.transform
    tr_axes = fig.transFigure.inverted().transform

    icon_size = (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.01
    icon_center = icon_size / 2.0

    for n in network.nodes:
        xf, yf = tr_figure(pos[n])
        xa, ya = tr_axes((xf, yf))

        if network.nodes[n]["node_prop"] == "headquarters":
            a = plt.axes([xa - 2*icon_center, ya - 2*icon_center, 2*icon_size, 2*icon_size])
        else:
            a = plt.axes([xa - icon_center, ya - icon_center, icon_size, icon_size])

        a.imshow(network.nodes[n]["image"])
        a.axis("off")

    ax.axis("off")

    return fig

# Auxiliary function to update the flow at the vertices of a water distribution network
def update_flow(network, nodes):
    for node in nodes:
        network.nodes[node]["flow"] = False
        network.nodes[node]["image"] = images["node"]
