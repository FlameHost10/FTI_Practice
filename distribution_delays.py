from math import sin, cos, asin, acos, radians, pi, sqrt
from numpy import arctan2, arcsin

import numpy as np
import matplotlib.pyplot as plt
from numpy import array

from TLE_time_delays_start import get_satellites_positions
from support.functions import calculate_delays_between_satellites
from support.point_on_sphere import point_on_sphere_distribution
from skyfield.api import load
import datetime


def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        datetime_str = lines[0].strip()

    dt = datetime.datetime.fromisoformat(datetime_str)
    ts = load.timescale()
    return ts.utc(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)


def cartesian(x, y, z):
    r = sqrt(x ** 2 + y ** 2 + z ** 2)

    ra = arctan2(y, x)
    dec = arcsin(z / r)
    return ra, dec


def building_distribution(delays_with_none):
    valid_delays = [delay for delay in delays_with_none if delay is not None]

    mean_delay = np.mean(valid_delays)
    std_delay = np.std(valid_delays)

    plt.figure(figsize=(10, 6))
    plt.hist(valid_delays, bins=30, alpha=0.7, color='blue', edgecolor='black')
    plt.axvline(mean_delay, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean_delay:.2f}s')
    plt.axvline(mean_delay + std_delay, color='green', linestyle='dashed', linewidth=1,
                label=f'Std Dev: {std_delay:.2f}s')
    plt.axvline(mean_delay - std_delay, color='green', linestyle='dashed', linewidth=1)
    plt.title('Распределение времён задержек между космическими аппаратами')
    plt.xlabel('Время задержки (с)')
    plt.ylabel('Частота')
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == '__main__':
    n_points = 200
    points = array(point_on_sphere_distribution(n_points))
    tle_folder_path = "resources/tle"
    input_file_path = "input.txt"
    utc_time = read_input_file(input_file_path)
    satellites = get_satellites_positions(utc_time, tle_folder_path)

    delays = np.array([])
    for point in points:
        ra_r, dec_r = cartesian(point[0], point[1], point[2])
        results = calculate_delays_between_satellites(satellites, ra_r, dec_r)
        np_results = np.array(results)
        new_delays = np_results[:, 2]
        delays = np.append(delays, new_delays)

    print(delays[0])

    building_distribution(delays)

