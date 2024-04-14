from functions import *
from skyfield.api import load

if __name__ == '__main__':
    address_array = ["resources/202307_GRBAlpha_tle.txt", "resources/202307_Monitor-2_tle.txt",
                     "resources/202307_Monitor-3_tle.txt", "resources/202307_Monitor-4_tle.txt",
                     "resources/202307_VZLUSAT-2_tle.txt"]

    ts = load.timescale()
    utc_time = ts.utc(2023, 7, 1)

    print(time_coordinates_cubesat(utc_time, address_array[0]))

    print(earth_block_degrees(0, 90, 10000, 180, -90, 10000))
    print(earth_block_degrees(90, 0, 10000, 270, 0, 10000))
    print(earth_block_degrees(0, 90, 10000, 0, 90, 10001))
