import matplotlib.pyplot as plt
from math import acos, sqrt, pi, cos, sin
from itertools import combinations


def point_on_sphere_distribution(n):
    return [
        (
            cos(pi * (1 + sqrt(5)) * i) * sin(acos(1 - 2 * (i + 0.5) / n)),  # x
            sin(pi * (1 + sqrt(5)) * i) * sin(acos(1 - 2 * (i + 0.5) / n)),  # y
            cos(acos(1 - 2 * (i + 0.5) / n))  # z
        )
        for i in range(n)
    ]


def calculate_distances(points):
    distances = []
    for p1, p2 in combinations(points, 2):
        distance = sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 + (p2[2] - p1[2]) ** 2)
        distances.append(distance)
    return distances


def spherical_distance(p1, p2):
    dot_product = sum(p1[i] * p2[i] for i in range(3))
    return acos(dot_product)


def calculate_spherical_distances(points):
    distances = []
    for p1, p2 in combinations(points, 2):
        distance = spherical_distance(p1, p2)
        distances.append(distance)
    return distances


# Функция для построения распределения сферических расстояний
def plot_spherical_distance_distribution(min_points=4, max_points=20):
    plt.figure(figsize=(10, 6))

    for n in range(min_points, max_points + 1):
        points = point_on_sphere_distribution(n)
        distances = calculate_spherical_distances(points)

        # Строим гистограмму для текущего количества точек
        plt.hist(distances, bins=20, alpha=0.6, label=f'{n} points', density=False)

    plt.title('Distribution of Spherical Distances Between Points on a Sphere')
    plt.xlabel('Spherical Distance (radians)')
    plt.ylabel('Density')
    plt.legend()
    plt.show()


plot_spherical_distance_distribution(200, 200)