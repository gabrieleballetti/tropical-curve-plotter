import matplotlib.pyplot as plt
import numpy as np

import config
import hull, curve, subdivision

def preprocess_points(points):
    # add a dummy point to avoid "flat" configurations
    sign = 1 if config.USE_MIN_CONVENTION else -1
    new_pt = [points[0][0], points[0][1], points[0][2] + sign]
    points.append(new_pt)
    return points

def parse(filename, points):
    file = open(filename, 'r')
    for line in file:
        point = np.array([float(n) for n in line.split()])
        print(point)
        np.vstack([points, point])
    file.close()
    print(points)
    return points

points = [
    [0, 0, 2],
    [1, 0, 1],
    [2, 0, 2],
    [0, 1, 1],
    [1, 1, 1],
    [0, 2, 2],
]

#deg = 4
#for i in range(deg + 1):
#    for j in range(deg + 1):
#        if i + j > deg:
#            continue
#        k = deg - i - j
#        pts.append([i,j,np.random.randint(-20, 20)])
#        #pts.append([i, j, np.sqrt(i*j*k)])

#print(points)
#
#points = preprocess_points(points)
#subdivision_ids, flat_edges = hull.lu_hull(points)
#subdivision.plot(points, subdivision_ids, flat_edges)
#curve.plot(points, subdivision_ids, flat_edges)

points = np.array((0, 3))
points = parse("input.txt", points)
print(points)