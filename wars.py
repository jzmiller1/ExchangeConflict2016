from collections import Counter
from datetime import datetime

import networkx as nx


def get_messages(current_node, neighbors, U):
    """Gets messages for a given node"""
    node_data = U.node[current_node]
    messages = ['\nSector  : {}\n'.format(current_node), ]

    if node_data.get('system') is not None:
        star = 'Star    : {} - {} Solar masses\n'.format(
            node_data['system']['star']['name'],
            node_data['system']['star']['mass']
        )
        messages.append(star)
        if node_data['system'].get('bodies') is not None:
            bodies = [body['planet_no'] + ' - ' + body['type']
                      for body
                      in node_data['system']['bodies']]
            messages.append('Bodies  : {}\n'.format(bodies))

    stations = node_data.get('station', None)
    if stations is not None:
        messages.append('Ports   : {}\n'.format(stations))

    jumps = " - ".join([str(x) for x in neighbors])
    messages.append('Warps to Sector(s) : {}\n'.format(jumps))
    return messages


# MAIN
U = nx.readwrite.read_gpickle('multiverse/universe.uni')

# add status to graph if it doesn't exist (new game case)
U.graph.setdefault('state', {'players': {}})

PLAYER = 'Crash'
CENTRALITY_NODE = {v: k
                   for k, v
                   in nx.get_node_attributes(U, 'name').items()}['Centrality']

if U.graph['state']['players'] == {}:
    U.graph['state']['players']['Crash'] = {'name': 'Crash',
                                            'wallet': 10000,
                                            'location': CENTRALITY_NODE,
                                            'visited': Counter()}
    U.graph['state']['players']['Crash']['visited'][CENTRALITY_NODE] = 1

current_node = U.graph['state']['players']['Crash']['location']
current_player = U.graph['state']['players'][PLAYER]

command = None

while command != 'Q':
    neighbors = U.neighbors(current_node)
    print("".join(get_messages(current_node, neighbors, U)))

    clock = datetime.now().strftime('%H:%M:%S')
    command = input("Command [TL={}]:[{}] (?=Help) : ".format(clock,
                                                              current_node)
                    )

    if command not in ['Q', 'V']:
        target_node = int(command)
        if target_node in neighbors:
            current_node = target_node
            current_player['location'] = current_node
            current_player['visited'].update({current_node: 1})

    if command == 'V':
        print("Jump history: {}".format(current_player['visited']))

nx.readwrite.write_gpickle(U, 'multiverse/universe.uni')
