import random
import os
import subprocess
import uuid


def get_system_data(BASE_DIR,
                    STARGEN_EXE_PATH,
                    STARGEN_DATA_PATH):
    """Generate a system and read the data from the resulting csv


    """
    seed = random.randint(0, 10000000)
    stargen_command = " ".join([os.path.join(BASE_DIR, STARGEN_EXE_PATH),
                                "-s{}".format(seed), # Looks like I need to provide a seed, if I call this too fast it gets the same seed inside stargen
                                "-n1",
                                "-e",
                                "-g",
                                # need code to handle moons in parser
                                # "-M"
                                ])

    output = subprocess.call(stargen_command, cwd='WinStarGen/')

    f = open(os.path.join(BASE_DIR, STARGEN_DATA_PATH), 'r')
    data = f.readlines()
    f.close()
    return data


def parse_system(data):
    """Parses a stargen system csv file

    returns a dict with star and bodies keys

    """
    data = [row.strip() for row in data]

    headers_star = data[0]
    headers_planet = data[2]

    system = {}
    bodies = []

    star_data = zip([col.strip().replace("'", "")
                     for col in headers_star.split(',')],
                    [col.strip().replace("'", "")
                     for col in data[1].split(',')])

    system['star'] = dict([col for col in star_data])

    # add an id
    system['star']['id'] = uuid.uuid4()

    #  Remove WinStarGen/StarGen.exe from star name
    system['star']['name'] = system['star']['name'].split(' ')[1]

    for body in data[3:]:
        body_data = zip([col.strip().replace("'", "")
                         for col in headers_planet.split(',')],
                        [col.strip().replace("'", "")
                         for col in body.split(',')])
        body = dict([col for col in body_data])

        # Remove WinStarGen/StarGen.exe and Star name from body name
        body['planet_no'] = body['planet_no'].split(' ')[2]
        # add an id
        body['id'] = uuid.uuid4()
        bodies.append(body)

    system['bodies'] = bodies

    return system




