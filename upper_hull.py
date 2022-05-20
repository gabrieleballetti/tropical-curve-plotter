import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull

def upper_hull(pts):
    # find the upper hull of a list of 3d points, where upper is wrt the 
    # third coordinate
    hull = ConvexHull(points=pts)
    simplices = hull.simplices
    subdivision_ids = np.array([simplices[i] for i, eq in enumerate(hull.equations) if eq[2] > 0])
    return subdivision_ids

def plot_subdivision(pts, subdivision_ids):
    for simplex in subdivision_ids:
        verts = np.array([pts[id][0:2] for id in simplex])

        # plot edges and vertices
        plt.plot(np.append(verts[:,0], verts[0][0]), np.append(verts[:,1], verts[0][1]), color='black')
        plt.plot(verts[:,0], verts[:,1], 'ko')
    plt.axis('equal')
    plt.axis('off')
    plt.show()


#print([[pts[i][0:2] for i in simplex] for simplex in a])

pts = [
    [0,0,1],
    [1,0,3],
    [2,0,1],
    [3,0,3],
    [0,1,2],
    [1,1,2],
    [2,1,6],
    [0,2,4],
    [1,2,1],
    [0,3,3]
]

print(upper_hull(pts))
plot_subdivision(pts, upper_hull(pts))