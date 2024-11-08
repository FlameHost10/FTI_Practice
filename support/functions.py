from math import sin, cos, asin, acos, radians, pi, sqrt

import numpy as np
from numpy import arctan2, arcsin
from skyfield.sgp4lib import EarthSatellite


class Satellite:
    def __init__(self, name=None, ra=None, dec=None, r=None, x=None, y=None, z=None, time_str=None, is_earth_occulted=None):
        self.name = name
        self.is_earth_occulted = is_earth_occulted

        if ra is not None and dec is not None and r is not None:
            self._set_equatorial(ra, dec, r)
        elif x is not None and y is not None and z is not None:
            self._set_cartesian(x, y, z)
        else:
            raise ValueError("Необходимо указать либо (ra, dec, r), либо (x, y, z)")

        if time_str:
            self.time = time_str
        else:
            self.time = None

    def _set_equatorial(self, ra, dec, r):
        self.ra = ra
        self.dec = dec
        self.r = r

        self.x = r * cos(dec) * cos(ra)
        self.y = r * cos(dec) * sin(ra)
        self.z = r * sin(dec)

    def _set_cartesian(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

        self.r = sqrt(x ** 2 + y ** 2 + z ** 2)

        self.ra = arctan2(y, x)
        self.dec = arcsin(z / self.r)

    @staticmethod
    def from_string(satellite_str):
        parts = satellite_str.replace("'", "").split()

        name = parts[0].strip(':')
        date_str = parts[1].strip()
        time_str = parts[2].strip()
        ra = float(parts[3].strip())
        dec = float(parts[4].strip())
        r = float(parts[5].strip())

        ra_rad = np.radians(ra)
        dec_rad = np.radians(dec)

        return Satellite(name=name, ra=ra_rad, dec=dec_rad, r=r, time_str=f'{date_str} {time_str}')


def radec_xyz(ra, dec, r):
    z = r * sin(dec)
    y = r * cos(dec) * sin(ra)
    x = r * cos(dec) * cos(ra)
    return x, y, z


def time_coordinates_cubesat(utc_time, address):
    min_time_diff = float("inf")
    tle_data = ["", ""]

    with open(address) as reader:
        tle_list = reader.readlines()

    for i in range(0, len(tle_list), 4):
        line_first = tle_list[i].rstrip()
        line_second = tle_list[i + 2].rstrip()

        satellite = EarthSatellite(line_first, line_second)

        if abs(utc_time.tt - satellite.epoch.tt) < min_time_diff:
            min_time_diff = abs(utc_time.tt - satellite.epoch.tt)
            tle_data[0] = line_first
            tle_data[1] = line_second

    satellite = EarthSatellite(tle_data[0], tle_data[1])
    geocentric = satellite.at(utc_time)
    ra, dec, r = geocentric.radec()
    # print(ra, dec, r)

    # print('Time of interest: ', utc_time.utc_jpl())
    # print('Satellite position: ', ra._degrees, dec._degrees, r.km)
    # print('Satellite epoch: ', satellite.epoch.utc_jpl())

    return radians(ra._degrees), radians(dec._degrees), r.km


def earth_block_degrees(sc_ra_r, sc_dec_r, sc_r, light_source_ra_r, light_source_dec_r):

    light_source_ra = radians(light_source_ra_r)
    light_source_dec = radians(light_source_dec_r)

    r_Earth = 6371  # km

    sc_z = sin(sc_dec_r)
    sc_y = cos(sc_dec_r) * sin(sc_ra_r)
    sc_x = cos(sc_dec_r) * cos(sc_ra_r)

    light_source_z = sin(light_source_dec)
    light_source_y = cos(light_source_dec) * sin(light_source_ra)
    light_source_x = cos(light_source_dec) * cos(light_source_ra)

    Theta_Earth = asin(r_Earth / sc_r)

    dot_sc_light_source = sc_x * light_source_x + sc_y * light_source_y + sc_z * light_source_z
    Theta_src = acos(-dot_sc_light_source)

    return Theta_Earth > Theta_src


def calculate_time_delays(sc1: Satellite, sc2: Satellite, light_ra_r, light_dec_r):
    c = 299_792.458
    r_GRB = np.array(radec_xyz(light_ra_r, light_dec_r, 1))

    if (earth_block_degrees(sc1.ra, sc1.dec, sc1.r, light_ra_r, light_dec_r)
            or earth_block_degrees(sc2.ra, sc2.dec, sc2.r, light_ra_r, light_dec_r)):
        raise ValueError('Earth blocks the SC')

    r_diff = np.array([sc1.x, sc1.y, sc1.z]) - np.array([sc2.x, sc2.y, sc2.z])

    dT = np.dot(r_diff, r_GRB) / c

    return dT


def calculate_delays_between_satellites(satellites, light_ra_r, light_dec_r):
    results = []
    n = len(satellites)
    for i in range(n):
        for j in range(i + 1, n):
            sc1 = satellites[i]
            sc2 = satellites[j]
            try:
                delay = calculate_time_delays(sc1, sc2, light_ra_r, light_dec_r)
                results.append([
                    f"The delay between satellites \033[93m{sc1.name}\033[0m and \033[93m{sc2.name}\033[0m is "
                    f"\033[91m{delay:.6f}\033[0m seconds", sc1, sc2, delay])
            except ValueError:
                results.append([
                    f"One of the satellites \033[93m{sc1.name}\033[0m or \033[93m{sc2.name}\033[0m is obscured, "
                    f"it is \033[91mimpossible to calculate the delay\033[0m", sc1, sc2, None])
    return results




