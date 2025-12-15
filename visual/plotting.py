import matplotlib.pyplot as plt
import os
from data.coordinates import LOCATION_NAMES

def plot_route_convergence(history, file_path="figure/convergence.png"):
    plt.figure(figsize=(10, 6))
    plt.plot(history, label='En İyi Mesafe', color='blue')
    plt.title('ACO Yakınsama Grafiği')
    plt.xlabel('İterasyon Sayısı')
    plt.ylabel('Mesafe (KM)')
    plt.grid(True)
    if not os.path.exists("figure"): os.makedirs("figure")
    plt.savefig(file_path)
    plt.close()
    return file_path

def plot_optimized_route(locations_df, best_route, file_path="figure/rota.png"):
    plt.figure(figsize=(10, 10))
    latitudes = locations_df['latitude'].values
    longitudes = locations_df['longitude'].values

    plt.scatter(longitudes, latitudes, c='red', s=100, zorder=5)

    for i in range(len(best_route)):
        start_idx = best_route[i]
        end_idx = best_route[(i + 1) % len(best_route)]

        color = 'gray' if i == len(best_route) - 1 else 'blue'
        linewidth = 1.5

        plt.plot(
            [longitudes[start_idx], longitudes[end_idx]],
            [latitudes[start_idx], latitudes[end_idx]],
            color=color, linewidth=linewidth, linestyle='-'
        )

    for i in range(len(latitudes)):
        name = LOCATION_NAMES[i]
        order = best_route.index(i)

        plt.annotate(
            f"({order}) {name}",
            (longitudes[i], latitudes[i]),
            xytext=(5, 5),
            textcoords='offset points',
            fontsize=9
        )

    plt.title(f'Optimize Edilmiş Gölet Rotası (ACO)')
    plt.xlabel('Boylam (Longitude)')
    plt.ylabel('Enlem (Latitude)')
    plt.tight_layout()

    if not os.path.exists("figure"): os.makedirs("figure")
    plt.savefig(file_path)
    plt.close()
    return file_path
