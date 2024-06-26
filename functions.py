from math import sin, cos, asin, acos, radians, pi, sqrt
from skyfield.sgp4lib import EarthSatellite


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
    print(ra, dec, r)

    print('Time of interest: ', utc_time.utc_jpl())
    print('Satellite position: ', ra._degrees, dec._degrees, r.km)
    print('Satellite epoch: ', satellite.epoch.utc_jpl())

    return ra._degrees, dec._degrees, r.km


def earth_block_degrees(sc_ra, sc_dec, sc_r, light_source_ra, light_source_dec, light_source_r):
    sc_ra = radians(sc_ra)
    sc_dec = radians(sc_dec)

    light_source_ra = radians(light_source_ra)
    light_source_dec = radians(light_source_dec)

    r_Earth = 6371  # km

    sc_z = sc_r * sin(sc_dec)
    sc_y = sc_r * cos(sc_dec) * sin(sc_ra)
    sc_x = sc_r * cos(sc_dec) * cos(sc_ra)

    light_source_z = light_source_r * sin(light_source_dec)
    light_source_y = light_source_r * cos(light_source_dec) * sin(light_source_ra)
    light_source_x = light_source_r * cos(light_source_dec) * cos(light_source_ra)

    Theta_Earth = asin(r_Earth / sc_r)

    dot_sc_light_source = sc_x * light_source_x + sc_y * light_source_y + sc_z * light_source_z
    Theta_src = acos(-dot_sc_light_source / (sc_r * light_source_r))

    return Theta_Earth > Theta_src


def point_on_sphere_distribution(n):
    return [
        (
            (
            acos(1 – 2 * (i + 0.5) / n),  # phi
            pi * (1 + sqrt(5)) * i  # theta
            ),
            (
                cos(pi * (1 + sqrt(5)) * i) * sin(acos(1 - 2 * (i + 0.5) / n)),  # x
                sin(pi * (1 + sqrt(5)) * i) * sin(acos(1 - 2 * (i + 0.5) / n)),  # y
                cos(acos(1 - 2 * (i + 0.5) / n))  # z
            )
        )
        for i in range(n)
    ]


def signal_delay(sc_ra, sc_dec, sc_r, light_source_ra, light_source_dec, light_source_r):
    if earth_block_degrees(sc_ra, sc_dec, sc_r, light_source_ra, light_source_dec, light_source_r):
        raise ValueError('Earth blocks the SC')
    else:
        C = 299_792.458

        sc_z = sc_r * sin(sc_dec)
        sc_y = sc_r * cos(sc_dec) * sin(sc_ra)
        sc_x = sc_r * cos(sc_dec) * cos(sc_ra)

        light_source_z = light_source_r * sin(light_source_dec)
        light_source_y = light_source_r * cos(light_source_dec) * sin(light_source_ra)
        light_source_x = light_source_r * cos(light_source_dec) * cos(light_source_ra)

        distance = ((sc_x - light_source_x) ** 2 + (sc_y - light_source_y) ** 2 + (sc_z - light_source_z) ** 2) ** .5

        return distance / C
