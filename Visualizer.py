import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def visualize(filename: str, node1:str, node2:str):
    df = pd.read_csv(filename)
    df['color'] = df['route_id'].apply(lambda x: x.lower())
    G = nx.from_pandas_edgelist(df, source=node1, target=node2, edge_attr=True)
    pos = nx.spring_layout(G, k=0.2)

    plt.figure(figsize=(10, 6))
    nx.draw(G, pos,with_labels=True,width=0.4, node_size=150, edge_color=df['color'],font_size=5)
    plt.axis('off')  # Hide axes if not needed
    plt.title("Node and Edge graph")
    plt.show()


if __name__ == '__main__':
    # visualize('route.csv', 'Origin', 'Destination')
    visualize('fairbank_stop_line.csv', 'origin_id', 'dest_id')
