import networkx as nx
from networkx_viewer import Viewer

u = nx.readwrite.read_gpickle('multiverse/universe.uni')

app = Viewer(u)
app.mainloop()
