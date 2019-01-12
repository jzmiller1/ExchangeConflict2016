import os
import random
import time

import networkx as nx

from stargen import get_system_data, parse_system
from components import Commodity


def gen(total_systems=20, deadends=0, rings=0, connectivity=1):
    G = nx.Graph()
    print("...with {} systems, {} deadends, {} rings and {} connectivity.".format(total_systems, deadends, rings, connectivity))
    starchart = {}
    system_id = 1
    systems = 0
    potentials = [x for x in range(1, total_systems + 1)]
    connected = []
    dead = []

    f = open('data/star_names.txt', 'r')
    names = f.readlines()
    names = [line.strip() for line in names]
    f.close()

    if total_systems < 20:
        raise TooFewStarsError
    if 2 * deadends > total_systems / 2.0:
        raise ExcessiveDeadendsError

    while systems <= total_systems:
        if deadends > 0:
            print("Creating deadend.")
            G.add_node(system_id)
            G.add_node(system_id + 1)
            G.add_edge(system_id, system_id + 1)
            potentials.remove(system_id)
            connected.append(system_id)
            deadends -= 1
            system_id += 2
            dead.append(system_id)
            continue
        if rings != 0:
            ring_size = random.choice([3, 3, 5, 5, 5, 5, 5, 7, 7, 9])
            ring_status = 'incomplete'
            ring = []
            while ring_status != 'complete':
                if len(potentials) > ring_size and len(ring) < ring_size:
                    system = random.choice(potentials)
                    potentials.remove(system)
                    connected.append(system)
                    ring.append(system)
                if len(ring) == ring_size:
                    ring_status = 'complete'
            print("Forming ring... {}".format(ring))
            for x in range(0, len(ring)):
                if x == 0:
                    G.add_node(ring[-1])
                    G.add_node(ring[x+1])
                    G.add_edge(ring[-1], ring[x+1])
                elif x == len(ring)-1:
                    G.add_node(ring[x-1])
                    G.add_node(ring[0])
                    G.add_edge(ring[x-1], ring[0])
                else:
                    G.add_node(ring[x-1])
                    G.add_node(ring[x+1])
                    G.add_edge(ring[x-1], ring[x+1])
            rings -= 1
            continue

        if connectivity > 0:
            while potentials:
                system = random.choice(potentials)
                target = random.choice(connected)
                G.add_edge(target, system)
                potentials.remove(system)
                connected.append(system)
                continue

        systems += 1

    while not nx.is_connected(G):
        elements = nx.connected_component_subgraphs(G)
        choices = []
        for element in elements:
            choices.append(random.choice(element.nodes()))
        G.add_edge(choices[0], choices[1])

    central = 1
    for node in G.nodes():
        if len(G.neighbors(node)) > central:
            central = node
    centrality_jumps = len(G.neighbors(central))
    print("Centrality is node {} with {} jumps...".format(central,
                                                          centrality_jumps))

    star_names = {}
    for x in range(0, total_systems):
        star_names[x+1] = names.pop(random.randint(0, len(names)-1))

    star_names[central] = 'Centrality'
    nx.set_node_attributes(G, 'name', star_names)
    G.node[central]['label_fill'] = 'red'
    return G


def stationgen(items):
    """Generates station."""
    commodities = [Commodity(*item) for item in items]
    station = {'items': {commodity.name: commodity
                         for commodity in commodities}}

    items = station['items']
    for item in items:
        items[item].generate()

    station['tags'] = []

    for item in items:
        item = items[item]
        if item.price_buy > item.price_sell:
            station['tags'].append("INVALID")

    if station['items']['equipment'].price_buy < 400 and station['items']['equipment'].price_sell < 250:
        station['tags'].append("PRODUCTION")

    if station['items']['organics'].price_sell < 80:
        station['tags'].append("ORBITAL HYDROPONICS")

    if station['items']['ice'].price_sell < 115:
        station['tags'].append("ICE MINING")

    if station['items']['organics'].price_buy > 30 and station['items']['ice'].price_buy > 70 and station['items']['fuel ore'].price_buy >= 4 and station['items']['equipment'].price_buy > 500:
        station['tags'].append("SUPER BUY")

    return station


def getstations(target=30, total_systems=100, stock_volumes=.1, items=None):
    start = time.time()
    stations = []

    superbuys = 0
    superbuys_target = 3 + total_systems / 100

    productions = 0
    productions_target = 3 + total_systems / 100

    mines = 0
    mines_target = 5 + total_systems / 100
    while len(stations) < target:
        station = stationgen(items)
        if superbuys < superbuys_target:
            if 'SUPER BUY' in station['tags']:
                stations.append(station)
                superbuys += 1
        elif superbuys >= superbuys_target and productions < productions_target:
            if 'PRODUCTION' in station['tags']:
                stations.append(station)
                productions += 1
        elif superbuys >= superbuys_target and productions >= productions_target and mines < mines_target:
            if 'ORBITAL HYDROPONICS' in station['tags'] or 'ICE MINING' in station['tags']:
                stations.append(station)
        elif superbuys >= superbuys_target and productions >= productions_target and mines >= mines_target and "INVALID" not in station['tags']:
            stations.append(station)
    stop = time.time()
    print("Stations took {} seconds to generate...".format(stop - start))
    return stations


def universe(total_systems=20, deadends=0, rings=0, connectivity=1, stations='common', stock_volumes='normal', items=None):
    station_density = {'sparse': .1,
                       'uncommmon': .15,
                       'common': .3,
                       'frequent': .45,
                       'dense': .6,
                       }

    stock = {'low': .1,
             'normal': .2,
             'high': .3,
             'epic': .4}

    u = gen(total_systems, deadends, rings, connectivity)
    print("Universe built.")
    print("Creating stations...")
    stations = getstations(target=station_density[stations] * total_systems,
                           total_systems=total_systems,
                           stock_volumes=stock[stock_volumes],
                           items=items)
    return u, stations



# MAIN

print("Running program.")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STARGEN_EXE_PATH = 'WinStarGen/StarGen.exe'
STARGEN_DATA_PATH = 'WinStarGen/html/StarGen.csv'

items = [('fuel ore', (1, 7, 2), (1, 10, 1), 5000, 30000),
         ('organics', (20, 90, 2), (20, 150, 1), 500, 20000),
         ('equipment', (220, 625, 2), (220, 1200, 1), 500, 20000),
         ('ice', (50, 150, 2), (50, 120, 1), 500, 20000)
         ]

print("Generating Universe...")
u, s = universe(25, 5, 1, 1, 'common', 'normal', items)

print("Placing stations...")
nodes = u.nodes()
random.shuffle(nodes)
for node in nodes:
    if s != []:
        new_station = s.pop()
        u.node[node]['station'] = new_station
        u.node[node]['fill'] = 'green'
    u.node[node]['system'] = parse_system(get_system_data(BASE_DIR,
                                                          STARGEN_EXE_PATH,
                                                          STARGEN_DATA_PATH)
                                          )

print("Universe created!")
print("Writing Universe to file...")
nx.readwrite.write_gpickle(u, 'multiverse/universe_stationfix.uni')
print("Complete!")


