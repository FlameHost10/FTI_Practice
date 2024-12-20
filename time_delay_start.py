from support.functions import *


def read_satellites_from_file(filename):
    satellites = []
    with open(filename, 'r') as file:
        for line in file:
            satellite = Satellite.from_string(line.strip())
            satellites.append(satellite)
    return satellites


if __name__ == '__main__':
    satellites = read_satellites_from_file('resources/satellites.txt')
    ra_d = 288.2643
    dec_d = 19.7712

    ra = radians(ra_d)
    dec = radians(dec_d)
    results = calculate_delays_between_satellites(satellites, ra, dec)
    for elem in results:
        print(elem[3])
