from collections import Counter


def get_messages(current_node, current_player, neighbors, U):
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

    visited_systems = current_player['visited'].keys()
    jumps = " - ".join([str(x)
                        if x in visited_systems
                        else '({})'.format(str(x))
                        for x in neighbors
                        ])
    messages.append('Warps to Sector(s) : {}\n'.format(jumps))
    return messages


def create_player(PLAYER, CENTRALITY_NODE, U):
    """Add a new player to the game state"""
    U.graph['state']['players'][PLAYER] = {'name': PLAYER,
                                           'wallet': 10000,
                                           'location': CENTRALITY_NODE,
                                           'visited': Counter()}
    U.graph['state']['players'][PLAYER]['visited'][CENTRALITY_NODE] = 1


def get_player_names(U):
    return [player
            for player
            in U.graph['state']['players']]
