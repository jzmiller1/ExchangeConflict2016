from datetime import datetime

import networkx as nx

import utils

# MAIN
U = nx.readwrite.read_gpickle('multiverse/universe.uni')

# add status to graph if it doesn't exist (new game case)
U.graph.setdefault('state', {'players': {}})

CENTRALITY_NODE = {v: k
                   for k, v
                   in nx.get_node_attributes(U, 'name').items()}['Centrality']

if U.graph['state']['players'] == {}:
    PLAYER = input('Enter a new player name: ')
    utils.create_player(PLAYER, CENTRALITY_NODE, U)
else:
    selection = None
    PLAYER = None
    players = utils.get_player_names(U)
    while selection not in ['N', 'E']:
        selection = input("(N)ew player or (E)xisting player? ")
    if selection == 'E':
        print("Players: {}".format(players))
        while PLAYER not in players:
            PLAYER = input('Enter valid player name: ')
    elif selection == 'N':
        while PLAYER not in players:
            players = utils.get_player_names(U)
            PLAYER = input('Enter valid player name: ')
            if PLAYER in players:
                print("You can't use that name!")
                PLAYER = None
            else:
                utils.create_player(PLAYER, CENTRALITY_NODE, U)
            players = utils.get_player_names(U)

current_node = U.graph['state']['players'][PLAYER]['location']
current_player = U.graph['state']['players'][PLAYER]

command = None

while command != 'Q':
    neighbors = U.neighbors(current_node)
    print("".join(utils.get_messages(current_node,
                                     current_player,
                                     neighbors,
                                     U)))

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
