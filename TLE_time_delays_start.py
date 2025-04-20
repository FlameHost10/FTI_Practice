import random
from skyfield.api import load
from pathlib import Path

from support.functions import *
from math import radians
from support.validators import *


def get_satellites_positions(utc_time, tle_folder_path):
    satellites = []
    tle_folder = Path(tle_folder_path)

    for tle_file in tle_folder.glob("*.txt"):
        name = tle_file.stem
        ra, dec, r = time_coordinates_cubesat(utc_time, tle_file)
        satellite = Satellite(name=name, ra=ra, dec=dec, r=r)
        satellites.append(satellite)

    return satellites


def generate_random_time_in_month(year, month):
    day = random.randint(1, 28)
    hour = random.randint(0, 23)
    minute = random.randint(0, 59)
    ts = load.timescale()
    return ts.utc(year, month, day, hour, minute)


def main():
    year = int(input("Enter year (e.g., 2024): "))
    month = get_month_input()

    user_choice = get_user_choice()

    if user_choice == 'Y':
        day = get_day_input(year, month)
        hour = get_hour_input()
        minute = get_minute_input()
        ts = load.timescale()
        utc_time = ts.utc(year, month, day, hour, minute)
    elif user_choice == 'N':
        utc_time = generate_random_time_in_month(year, month)
        print(f"\033[94mSelected random time: {utc_time.utc_jpl()}\033[0m")

    tle_folder_path = "resources/tle"

    satellites = get_satellites_positions(utc_time, tle_folder_path)
    print("Satellite coordinates at selected time:")
    for sat in satellites:
        print(f"{sat.name}: RA={sat.ra}, Dec={sat.dec}, Distance={sat.r} km")

    print("=" * 88)
    light_ra_r = radians(float(input("\033[94mEnter source coordinates (RA) in degrees: \033[0m")))
    light_dec_r = radians(float(input("\033[94mEnter source coordinates (Dec) in degrees: \033[0m")))

    results = calculate_delays_between_satellites(satellites, light_ra_r, light_dec_r)


    print("Satellite delay results:")
    for result in results:
        print(result[-1])


if __name__ == '__main__':
    main()
