import numpy as np
import matplotlib.pyplot as plt


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
    np.random.seed(42)
    delays = np.random.randn(100)
    building_distribution(delays)
