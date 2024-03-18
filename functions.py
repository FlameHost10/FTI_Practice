from skyfield.api import load
from skyfield.sgp4lib import EarthSatellite
from skyfield.toposlib import wgs84


def time_coordinates_cubesat(required_time, address):
    min_time_diff = float("inf")
    tle_data = ["", ""]
    satellite = None

    with open(address) as reader:
        tle_list = reader.readlines()

    for i in range(0, len(tle_list), 4):
        line_first = tle_list[i].rstrip()
        line_second = tle_list[i + 2].rstrip()

        satellite = EarthSatellite(line_first, line_second)
        if abs(required_time - satellite.epoch.tt) < min_time_diff:
            min_time_diff = abs(required_time - satellite.epoch.tt)
            tle_data[0] = line_first
            tle_data[1] = line_second

    ts = load.timescale()
    bluffton = wgs84.latlon(+40.8939, -83.8917)
    tle_date = satellite.epoch.utc
    return (satellite - bluffton).at(ts.utc(tle_date[0], tle_date[1], tle_date[2], tle_date[3], tle_date[4], tle_date[5])).radec()


# def blackout_cubesat(required_time, address, coordinates_RGB):

