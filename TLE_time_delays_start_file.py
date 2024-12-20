from skyfield.api import load
from pathlib import Path
from support.functions import *
from math import radians, degrees
import datetime


def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        datetime_str = lines[0].strip()
        source_coordinates = lines[1].strip().split(',')
        ra_deg = float(source_coordinates[0].strip())
        dec_deg = float(source_coordinates[1].strip())

    dt = datetime.datetime.fromisoformat(datetime_str)
    ts = load.timescale()
    utc_time = ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

    return utc_time, radians(ra_deg), radians(dec_deg)


def write_output_file(output_path, utc_time, ra_deg, dec_deg, satellites, results):
    with open(output_path, 'w') as file:
        file.write(f"Time: {utc_time.utc_iso()} UTC\n")
        file.write(f"Source position: RA(deg), Dec(deg) = {ra_deg:.4f}, {dec_deg:+.4f}\n")
        file.write("\nSpacecraft information\n\n")
        file.write("ScName  RA  Dec  R  IsEarthOcculted\n")

        rad_to_degree = 180 / np.pi

        for sat in satellites:
            occulted = 'Y' if sat.is_earth_occulted else 'N'
            file.write(f"{sat.name:8}  {sat.ra * rad_to_degree:.2f}  {sat.dec * rad_to_degree:.2f}  {sat.r:.4f}  {occulted}\n")

        file.write("\nTime delays\n\n")
        file.write("ScNames   dT(s)\n")

        for result in results:
            delay = result[2]
            sc1 = result[0]
            sc2 = result[1]
            if delay is None:
                delay_str = '--'
            else:
                delay_str = f"{delay:.6f}"
            file.write(f"{sc1.name}\t-\t{sc2.name}\t{delay_str}\n")


def get_satellites_positions(utc_time, tle_folder_path, light_ra_r, light_dec_r):
    satellites = []
    tle_folder = Path(tle_folder_path)

    for tle_file in tle_folder.glob("*.txt"):
        file_name = tle_file.stem
        name = file_name.split("_")[1]
        ra, dec, r = time_coordinates_cubesat(utc_time, tle_file)
        satellite = Satellite(name=name, ra=ra, dec=dec, r=r)

        is_earth_occulted = earth_block_degrees(ra, dec, r, light_ra_r, light_dec_r)
        satellite.is_earth_occulted = is_earth_occulted
        satellites.append(satellite)

    return satellites


def main():
    input_file_path = "input.txt"
    output_file_path = "output.txt"

    utc_time, light_ra_r, light_dec_r = read_input_file(input_file_path)

    tle_folder_path = "resources/tle"

    satellites = get_satellites_positions(utc_time, tle_folder_path, light_ra_r, light_dec_r)

    results = calculate_delays_between_satellites(satellites, light_ra_r, light_dec_r)

    write_output_file(output_file_path, utc_time, degrees(light_ra_r), degrees(light_dec_r), satellites, results)


if __name__ == '__main__':
    main()
