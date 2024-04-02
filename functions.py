import math

from skyfield.api import load
from skyfield.sgp4lib import EarthSatellite
from skyfield.api import Angle, wgs84, Topos


def time_coordinates_cubesat(required_time, address):
    min_time_diff = float("inf")
    tle_data = ["", ""]

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

    satellite = EarthSatellite(tle_data[0], tle_data[1])

    ts = load.timescale()
    t = ts.now()

    topocentric = Topos(latitude_degrees=51.48, longitude_degrees=-0.19)

    difference = satellite - topocentric
    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()

    ra = az.radians
    dec = alt.radians

    return math.degrees(ra), math.degrees(dec)


def blackout_cubesat(satellite_ra, satellite_dec, light_source_ra, light_source_dec):
    ts = load.timescale()

    observer_location = Topos(latitude_degrees=light_source_dec, longitude_degrees=light_source_ra)

    satellite_position = Topos(latitude_degrees=satellite_dec, longitude_degrees=satellite_ra)

    t = ts.now()
    difference = satellite_position - observer_location
    topocentric = difference.at(t)
    alt, az, distance = topocentric.altaz()

    return alt.degrees > 0