This is Personal Project. Using Python 3.11

Requirement Module:
numpy `pip install numpy`

pandas `pip install pandas`

geopy `pip install geopy`


### Code fragment the could be alternative of current visualizer
```python
import networkx as nx

G = nx.DiGraph()
for index, row in df.iterrows():
  stop_id = row['stop_id']
  lat = row['stop_lat']
  lon = row['stop_lon']
  G.add_node(stop_id, pos=(lat, lon))

for index, row in df.iterrows():
  stop_id = row['stop_id']
  next_id = row['next_id']
  route_id = row['route_id']
  G.add_edge(stop_id, next_id, color=route_id)

colors = nx.get_edge_attributes(G,'color').values()
p = nx.get_node_attributes(G, 'pos')
nx.draw(G, p, with_labels=False, node_size=50,
        edge_color=colors)
plt.show()
```