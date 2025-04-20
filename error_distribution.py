import math
from math import sin, cos, asin, acos, radians, pi, sqrt
import random

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


def get_uncertainty(file_path):
    uncertainties = []

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            if parts:
                try:
                    uncertainty = float(parts[-1])
                    uncertainties.append(uncertainty)
                except ValueError:
                    print(f"Предупреждение: Не удалось преобразовать значение '{parts[-1]}' в float.")

    return uncertainties


def get_random_uncertainty(uncertainties):
    if uncertainties:
        return random.choice(uncertainties)
    else:
        return None


def get_max_error(delays_info, uncertainties):
    max_error = 0
    c = 299792458
    for delay_info in delays_info:
        d = get_distance(delay_info[0], delay_info[1])
        uncertainty = get_random_uncertainty(uncertainties)
        sign = random.choice([-1, 1])
        term1 = (c / d) * (delay_info[2] + sign * uncertainty)
        term2 = (c / d) * delay_info[2]

        if not (-1 <= term1 <= 1) or not (-1 <= term2 <= 1):
            term1 = (c / d) * (delay_info[2] - sign * uncertainty)
            term2 = (c / d) * delay_info[2]

        if not (-1 <= term1 <= 1) or not (-1 <= term2 <= 1):
            print()
            print(f"term1 {term1}, term2 {term2}")
            # print(c/d)
            # print(delay_info[2] + sign * uncertainty)
            # print(delay_info[2])
            print("=================================================ERROR=============================")
        else:
            acos_term1 = math.acos(term1)
            acos_term2 = math.acos(term2)
            error = acos_term1 - acos_term2
            max_error = max(max_error, error)

    return max_error


def get_distance(sc1, sc2):
    x = sqrt((sc1.x - sc2.x) ** 2 + (sc1.y - sc2.y) ** 2 + (sc1.z - sc2.z) ** 2) * 1000
    return x


def building_distribution(delays_with_none):
    valid_delays = [delay for delay in delays_with_none if delay is not None]

    mean_delay = np.mean(valid_delays)
    std_delay = np.std(valid_delays)

    plt.figure(figsize=(10, 6))
    plt.hist(valid_delays, bins=30, alpha=0.7, color='blue', edgecolor='black')
    plt.axvline(mean_delay, color='red', linestyle='dashed', linewidth=1, label=f'Mean: {mean_delay:.2f}')
    plt.axvline(mean_delay + std_delay, color='green', linestyle='dashed', linewidth=1,
                label=f'Std Dev: {std_delay:.2f}')
    plt.axvline(mean_delay - std_delay, color='green', linestyle='dashed', linewidth=1)
    plt.title('Распределение максимального угла ошибки между источниками ГВ')
    plt.xlabel('угол ошибки (dθ)')
    plt.ylabel('Частота')
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == '__main__':
    n_points = 200
    points = array(point_on_sphere_distribution(n_points))
    tle_folder_path = "resources/tle"
    input_file_path = "input.txt"
    uncertainties_file_path = "resources/stat_dtcc_near.txt"
    utc_time = read_input_file(input_file_path)
    satellites = get_satellites_positions(utc_time, tle_folder_path)
    uncertainties = get_uncertainty(uncertainties_file_path)

    delays = np.array([])
    for point in points:
        ra_r, dec_r = cartesian(point[0], point[1], point[2])
        results = calculate_delays_between_satellites(satellites, ra_r, dec_r)
        valid_delays = [delay for delay in results if delay[2] is not None]
        max_error = get_max_error(valid_delays, uncertainties)
        delays = np.append(delays, max_error)

    # print(delays)

    building_distribution(delays)
