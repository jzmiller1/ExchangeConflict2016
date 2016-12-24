from datetime import datetime

import networkx as nx

U = nx.readwrite.read_gpickle('multiverse/universe.uni')

CENTRALITY_NODE = {v: k
                   for k, v
                   in nx.get_node_attributes(U, 'name').items()}['Centrality']

current_node = CENTRALITY_NODE

command = None

while command != 'Q':
    neighbors = U.neighbors(current_node)
    jumps = " - ".join([str(x) for x in neighbors])
    stations = U.node[current_node].get('station', None)
    bodies = [body['planet_no'].split(' ')[2] + ' - ' + body['type']
              for body
              in U.node[current_node]['system']['bodies']]

    print("""
    Sector    : {:^5}
    Ports     : {}
    Bodies    : {}
    Warps to Sector(s) : {}
    """.format(current_node,
               stations,
               bodies,
               jumps)
          )

    clock = datetime.now().strftime('%H:%M:%S')
    command = input("Command [TL={}]:[{}] (?=Help) : ".format(clock,
                                                              current_node)
                    )

    if command != 'Q':
        target_node = int(command)
        if target_node in neighbors:
            current_node = target_node