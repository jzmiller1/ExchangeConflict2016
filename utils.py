import random
from collections import Counter


def get_messages(current_node, current_player, neighbors, UNI):
    """Gets messages for a given node"""
    node_data = UNI.graph.node[current_node]
    messages = ['\nSector  : {}\n'.format(current_node), ]

    node_str = str(current_node)
    if '.' in node_str:
        info = str(current_node).split('.')
        parent = int(info[0])
        body = info[1]

    if node_data.get('system') is not None:
        star = 'Star    : {} - {} Solar masses\n'.format(
            node_data['system']['star']['name'],
            node_data['system']['star']['mass']
        )
        messages.append(star)
        if node_data['system'].get('bodies') is not None:

            bodies = [str(current_node) + '.' +  body['planet_no'] + '-' + body['type']
                      for body
                      in node_data['system']['bodies']]
            messages.append('Bodies  : {}\n'.format(",  ".join(bodies)))
    else:
        body = UNI.graph.node[parent]["system"]["bodies"][int(body)-1]
        messages.append(f'Body    : {body["type"]} Planet - {body["id"]}\n')

    stations = node_data.get('station', None)
    if stations is not None:
        messages.append('Ports   : {}\n'.format("-".join(stations['tags'])))

    visited_systems = current_player.sectors_visited.keys()
    jumps = " - ".join([str(x)
                        if x in visited_systems
                        else '({})'.format(str(x))
                        for x in neighbors
                        if '.' not in str(x)
                        ])
    messages.append('Warps to Sector(s) : {}\n'.format(jumps))
    return messages


def create_player(PLAYER, CENTRALITY_NODE, U):
    """Add a new player to the game state"""
    U.graph['state']['players'][PLAYER] = {'name': PLAYER,
                                           'wallet': 10000,
                                           'location': CENTRALITY_NODE,
                                           'visited': Counter(),
                                           'holds': 20,
                                           'cargo': {}}
    U.graph['state']['players'][PLAYER]['visited'][CENTRALITY_NODE] = 1


def get_player_names(U):
    return [player
            for player
            in U.graph['state']['players']]


def bimodal(low1, high1, mode1, low2, high2, mode2):
    """http://stackoverflow.com/questions/651421/bimodal-distribution-in-c-or-python"""
    toss = random.choice((1, 2))
    if toss == 1:
        return random.triangular(low1, high1, mode1)
    else:
        return random.triangular(low2, high2, mode2)


def is_float(input):
    try:
        num = float(input)
    except ValueError:
        return False
    return True


def scanner(current_node, UNI):
    """Gets data for body in current sector"""
    if isinstance(current_node, int):
        node_data = UNI.graph.node[current_node]
        print(node_data['system']['star'])
    elif isinstance(current_node, float):
        sector, body = str(current_node).split('.')
        node_data = UNI.graph.node[int(sector)]
        print(node_data['system']['bodies'][int(body)-1])
