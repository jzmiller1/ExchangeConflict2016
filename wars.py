from datetime import datetime
import os
import pickle

import networkx as nx

import utils
from components import Universe, PlayerConfig, GameConfig

# MAIN
U = nx.readwrite.read_gpickle('multiverse/universe.uni')

CENTRALITY_NODE = {v: k
                   for k, v
                   in nx.get_node_attributes(U, 'name').items()}['Centrality']

UNI_PATH = 'multiverse/UNISAVE.pkl'

if os.path.isfile(UNI_PATH):
    UNI = pickle.load(open(UNI_PATH, 'rb'))
else:
    UNI = Universe('New Game', U, GameConfig(PlayerConfig(CENTRALITY_NODE)))

if len(UNI.players) == 0:
    PLAYER = input('Enter a new player name: ')
    UNI.create_player(PLAYER)
else:
    selection = None
    PLAYER = None
    players = UNI.players.keys()
    while selection not in ['N', 'E']:
        selection = input("(N)ew player or (E)xisting player? ")
    if selection == 'E':
        print("Players: {}".format(UNI.players.keys()))
        while PLAYER not in players:
            PLAYER = input('Enter valid player name: ')
    elif selection == 'N':
        while PLAYER not in players:
            players = UNI.players.keys()
            PLAYER = input('Enter valid player name: ')
            if PLAYER in players:
                print("You can't use that name!")
                PLAYER = None
            else:
                UNI.create_player(PLAYER)
            players = UNI.players.keys()

current_player = UNI.players[PLAYER]

command = None

while command != 'Q':
    neighbors = UNI.graph.neighbors(current_player.current_node)
    print("".join(utils.get_messages(current_player.current_node,
                                     current_player,
                                     neighbors,
                                     UNI)))

    clock = datetime.now().strftime('%H:%M:%S')
    command = input("Command [TL={}]:[{}] (?=Help) : ".format(clock,
                                                              current_player.current_node)
                    )

    if command not in ['Q', 'V', 'P']:
        target_node = int(command)
        if target_node in neighbors:
            current_player.current_node = target_node
            current_player.sectors_visited.update({current_player.current_node: 1})

    if command == 'V':
        print("Jump history: {}".format(current_player.sectors_visited))

    if command == 'P':
        node_data = UNI.graph.node[current_player.current_node]
        stations = node_data.get('station', None)

        if stations is not None:
            selection = None
            print("\n<T> Trade at this Port\n<Q> Quit, nevermind")
            while selection not in ['T', 'Q']:
                selection = input('Enter your choice? ')
            if selection == 'T':
                print("\n{:^14} {:^16} {:^10}".format('Items', 'Prices (B/S)', 'Supply'))
                print("{:^14} {:^16} {:^10}".format('¯'*5, '¯'*13, '¯'*6))
                for item in stations['items']:
                    item = stations['items'][item]
                    prices = "{:<7}/{:>7}".format(item.price_buy, item.price_sell)
                    print("{:<14} {:^16} {:^10}".format(item.name, prices, item.units))
                print('\nYou have {} credits and Y empty cargo holds.\n'.format(current_player.wallet))
                trade = input('Enter your choice? ')

pickle.dump(UNI, open(UNI_PATH, 'wb'))
