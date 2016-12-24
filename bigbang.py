import os
import random
import time

import networkx as nx

from stargen import get_system_data, parse_system


def gen(total_systems=20, deadends=0, rings=0, connectivity=1):
    G = nx.Graph()
    print(total_systems, deadends, rings, connectivity)
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
            print("Ring: {}".format(ring))
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
    print(central, G.neighbors(central))

    star_names = {}
    for x in range(0, total_systems):
        star_names[x+1] = names.pop(random.randint(0, len(names)-1))

    star_names[central] = 'Centrality'
    nx.set_node_attributes(G, 'name', star_names)
    #print nx.get_node_attributes(G, 'name')
    G.node[central]['label_fill'] = 'red'
    return G

def bimodal(low1, high1, mode1, low2, high2, mode2):
    """http://stackoverflow.com/questions/651421/bimodal-distribution-in-c-or-python"""
    toss = random.choice((1, 2))
    if toss == 1:
        return random.triangular(low1, high1, mode1)
    else:
        return random.triangular(low2, high2, mode2)


def stationgen():
    """Generates station."""
    station = {}

    x = round(bimodal(170, 500, 2, 170, 1200, 1), 0)
    y = round(bimodal(170, 500, 2, 170, 1200, 1), 0)
    station['e_buy'] = min(x, y)
    station['e_sell'] = max(x, y)

    x = round(bimodal(10, 50, 2, 10, 120, 1), 0)
    y = round(bimodal(10, 120, 1, 10, 50, 2), 0)
    station['o_buy'] = min(x, y)
    station['o_sell'] = max(x, y)

    x = round(bimodal(1, 7, 2, 1, 10, 1), 0)
    y = round(bimodal(1, 10, 1, 1, 7, 2), 0)
    station['f_buy'] = min(x, y)
    station['f_sell'] = max(x, y)

    x = round(bimodal(50, 150, 2, 50, 120, 1), 0)
    y = round(bimodal(50, 120, 1, 50, 150, 2), 0)
    station['i_buy'] = min(x, y)
    station['i_sell'] = max(x, y)

    station['tags'] = []

    if station['e_buy'] > station['e_sell'] or station['o_buy'] > station['o_sell'] or \
       station['f_buy'] > station['f_sell'] or station['i_buy'] > station['i_sell']:
        station['tags'].append("INVALID")

    if station['o_buy'] > 30 and station['e_sell'] < 400 and station['e_buy'] < 100:
        station['tags'].append("PRODUCTION")

    if station['o_buy'] > 80:
        station['tags'].append("ORE MINING")

    if station['i_buy'] > 115:
        station['tags'].append("ICE MINING")

    if station['o_buy'] > 55 and station['i_buy'] > 95:
        station['tags'].append("RESOURCE")

    if station['o_buy'] > 60 and station['i_buy'] > 100 and station['f_buy'] >= 4 and station['e_buy'] > 600:
        station['tags'].append("SUPER BUY")

    return station


def getstations(target=30, total_systems=100, stock_volumes=.1):
    start = time.time()
    stations = []

    superbuys = 0
    superbuys_target = 3 + total_systems / 100

    resources = 0
    resources_target = 3 + total_systems / 100

    productions = 0
    productions_target = 3 + total_systems / 100

    mines = 0
    mines_target = 5 + total_systems / 100
    while len(stations) < target:
        station = stationgen()
        if superbuys < superbuys_target:
            if 'SUPER BUY' in station['tags']:
                stations.append(station)
                superbuys += 1
        elif superbuys >= superbuys_target and resources < resources_target:
            if 'RESOURCE' in station['tags']:
                stations.append(station)
                resources += 1
        elif superbuys >= superbuys_target and resources >= resources_target and productions < productions_target:
            if 'PRODUCTION' in station['tags']:
                stations.append(station)
                productions += 1
        elif superbuys >= superbuys_target and resources >= resources_target and productions >= productions_target and mines < mines_target:
            if 'ORE MINING' in station['tags'] or 'ICE MINING' in station['tags']:
                stations.append(station)
        elif superbuys >= superbuys_target and resources >= resources_target and productions >= productions_target and mines >= mines_target and "INVALID" not in station['tags']:
            stations.append(station)
    stop = time.time()
    print("Total Time: {}".format(stop - start))
    return stations


def universe(total_systems=20, deadends=0, rings=0, connectivity=1, stations='common', stock_volumes='normal'):
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
    print("Going to getstations!")
    stations = getstations(target=station_density[stations] * total_systems,
                           total_systems=total_systems,
                           stock_volumes=stock[stock_volumes])
    print("Done getting stations!")
    return u, stations



# MAIN

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STARGEN_EXE_PATH = 'WinStarGen/StarGen.exe'
STARGEN_DATA_PATH = 'WinStarGen/html/StarGen.csv'

print("Running program.")
u, s = universe(25, 5, 1, 1, 'common', 'normal')
print("Printing u")
print(u)

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

nx.readwrite.write_gpickle(u, 'multiverse/universe.uni')

