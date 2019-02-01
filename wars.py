from datetime import datetime
import os
import pickle
import uuid

import networkx as nx
import redis

from components import Universe, PlayerConfig, GameConfig
from trade import trade
import utils
import secret

# MAIN
U = nx.readwrite.read_gpickle('multiverse/universe_body_nodes_experi.uni')
r = redis.StrictRedis(host=secret.HOST,
                      port=secret.PORT,
                      password=secret.PASSWORD)
p = r.pubsub()

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
p.subscribe('GAMEWORLD')
r.publish('GAMEWORLD', '{} joins the game... {}'.format(current_player.name,
                                                     uuid.uuid4()))

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
    command = command.upper()
    if command not in ['Q', 'V', 'P', '?'] and (command.isnumeric() or utils.is_float(command)):
        try:
            target_node = int(command)
        except ValueError:
            target_node = float(command)
        if target_node in neighbors:
            current_player.current_node = target_node
            current_player.sectors_visited.update({current_player.current_node: 1})
        else:
            print("That's an invalid jump selection...try again!")

    elif command == 'V':
        print("Jump history: {}".format(current_player.sectors_visited))

    elif command == 'C':
        ship = UNI.ships[current_player.ship_current]
        print(f"Cargo: {ship['cargo']}\n Wallet: {current_player.wallet}")

    elif command == 'S':
        utils.scanner(current_player.current_node, UNI)

    elif command == 'P':
        node_data = UNI.graph.node[current_player.current_node]
        station = node_data.get('station', None)
        if station is not None:
            selection = ''
            print("\n<T> Trade at this Port\n<Q> Quit, nevermind")
            while selection.upper() not in ['T', 'Q']:
                selection = input('Enter your choice? ')
            if selection.upper() == 'T':
                trade(UNI, current_player, station)



    elif command == '?':
        print("\n  This is the help menu.  P to trade at a Port, Q to quit, V to view jump history. C to show your wallet and cargo. S to use the scanner on planets and stars.")

    else:
        print("Invalid command!")



pickle.dump(UNI, open(UNI_PATH, 'wb'))
r.publish('GAMEWORLD', '{} leaves the game...'.format(current_player.name))
p.unsubscribe()
print(UNI.players)


