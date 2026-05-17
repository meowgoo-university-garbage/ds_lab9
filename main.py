import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np

from shapely.geometry import LineString



PATH = "./Fire_Stations/Fire_Stations.shp"



fire_stations = gpd.read_file(PATH)
TOTAL = len(fire_stations)
TOTAL = 50

fire_stations.plot()
plt.show()



# fire_stations = fire_stations.to_crs('EPSG:4326')
fire_stations = fire_stations.to_crs("EPSG:3857")


selection = fire_stations[0:TOTAL]



dist_closest_avg_sum = 0
dist_closest_avg_num = 0
dist_closest_min = None
dist_closest_max = None

lines = []
distances = np.zeros(len(selection))
for i in range(len(selection)):
    src = selection.iloc[i].geometry
    for j in range(len(selection)):
        dst = selection.iloc[j].geometry
        distances[j] = src.distance(dst)

    indexes = np.argsort(distances)
    for j in range(1, 4):
        dst = selection.iloc[indexes[j]].geometry
        line = LineString([src, dst])
        lines.append(line)

        d = src.distance(dst)
        dist_closest_avg_sum += d
        dist_closest_avg_num += 1

        if dist_closest_min == None or d < dist_closest_min:
            dist_closest_min = d

        if dist_closest_max == None or d > dist_closest_max:
            dist_closest_max = d

dist_avg_sum = 0
dist_avg_num = 0
dist_min = None
dist_max = None

dist_matrix = np.zeros((len(selection), len(selection)))
for i in range(len(selection)):
    for j in range(len(selection)):
        src = selection.iloc[i].geometry
        dst = selection.iloc[j].geometry
        d = src.distance(dst)
        dist_matrix[i, j] = d

        if i != j:
            dist_avg_sum += d
            dist_avg_num += 1

            if dist_min == None or d < dist_min:
                dist_min = d

            if dist_max == None or d > dist_max:
                dist_max = d

print(dist_matrix)
print("Average distance:", dist_avg_sum / dist_avg_num)
print("Min distance:", dist_min, "Max distance:", dist_max)
print("Closest average distance:", dist_closest_avg_sum / dist_closest_avg_num)
print("Closest min distance:", dist_closest_min, "Closest max distance:", dist_closest_max)




lines_gdf = gpd.GeoDataFrame(geometry=lines, crs=fire_stations.crs)

fig, ax = plt.subplots(figsize=(8, 4))
fire_stations.plot(ax=ax, markersize=20, color="blue", marker="o", zorder=1)
selection.plot(ax=ax, markersize=20, color="red", marker="o", zorder=3)


lines_gdf.plot(ax=ax, color="lime", linewidth=2, zorder=2)

plt.show()
