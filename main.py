from functions import *
from skyfield.api import load


def read_satellites_from_file(filename):
    satellites = []
    with open(filename, 'r') as file:
        for line in file:
            satellite = Satellite.from_string(line.strip())
            satellites.append(satellite)
    return satellites


if __name__ == '__main__':
    satellites = read_satellites_from_file('resources/satellites.txt')
    # ra = 288.2643
    # dec = 19.7712

    # ra = 180
    # dec = 0
    results = calculate_delays_between_satellites(satellites, ra, dec)
    for elem in results:
        print(elem)
