import networkx as nx

U = nx.readwrite.read_gpickle('multiverse/universe.uni')

CENTRALITY_NODE = {v: k for k, v in nx.get_node_attributes(U, 'name').items()}['Centrality']
print(CENTRALITY_NODE)