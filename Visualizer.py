import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def visualize(filename: str, node1:str, node2:str):
    data = pd.read_csv(filename)

    G = nx.DiGraph()

    for stop_id in data[node1].unique():
        G.add_node(stop_id)

    for index, row in data.iterrows():
        origin_id = row[node1]
        to_stop_id = row[node2]
        G.add_edge(origin_id, to_stop_id)

    pos = nx.spring_layout(G)  # Use nx.circular_layout, nx.fruchterman_reingold_layout, etc. for different layouts

    # Plot the graph
    plt.figure()

    # Plot nodes
    nx.draw_networkx_nodes(G, pos, node_size=50, node_color='lightblue', edgecolors='black')

    # Plot edges (adjust line width and style as needed)
    nx.draw_networkx_edges(G, pos, width=0.2, alpha=0.7)

    # Add node labels (optional)
    nx.draw_networkx_labels(G, pos, font_size=5, font_weight='bold')

    plt.axis('off')  # Hide axes if not needed
    plt.title("Node and Edge graph")
    plt.show()

if __name__ == '__main__':
    # visualize('route.csv', 'Origin', 'Destination')
    visualize('csv_filename.csv', 'origin_id', 'dest_id')
