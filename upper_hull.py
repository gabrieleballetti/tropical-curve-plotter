import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull

def upper_hull(pts):
    # find the upper hull of a list of 3d points, where upper is wrt the 
    # third coordinate
    hull = ConvexHull(points=pts)
    upper_ids = [i for i, eq in enumerate(hull.equations) if eq[2] > 0]
    triangles_ids = np.array([hull.simplices[i] for i in upper_ids])
    normals = np.take(hull.equations, upper_ids, 0)[:,0:3]
    
    # find duplicate edges
    flat_edges = []
    for i in range(len(triangles_ids)):
        for j in range(i+1, len(triangles_ids)):
            if np.allclose(normals[i],normals[j]):
                intersection = set(triangles_ids[i]).intersection(set(triangles_ids[j]))
                if len(intersection) == 2:
                    flat_edges.append(intersection)

    return triangles_ids, flat_edges

def plot_subdivision(pts, subdivision_ids, flat_edges=[]):
    for simplex in subdivision_ids:
        for i in range(3):
            id1, id2 = simplex[i], simplex[(i+1) % 3]
            if (set([id1, id2]) in flat_edges):
                continue
            edge = np.array([pts[id1], pts[id2]])
            plt.plot(edge[:,0], edge[:,1], color='black')
            plt.plot(pts[id1][0], pts[id1][1], 'ko')
        

        # plot edges and vertices
        #plt.plot(np.append(verts[:,0], verts[0][0]), np.append(verts[:,1], verts[0][1]), color='black')
        #plt.plot(verts[:,0], verts[:,1], 'ko')
    plt.axis('equal')
    plt.axis('off')
    plt.show()


#print([[pts[i][0:2] for i in simplex] for simplex in a])

pts = [
    [0,0,2],
    [1,0,2],
    [2,0,1],
    [3,0,1],
    [0,1,2],
    [1,1,2],
    [2,1,1],
    [0,2,1],
    [1,2,1],
    [0,3,1]
]


subdivision_ids, flat_edges = upper_hull(pts)
print(flat_edges)
plot_subdivision(pts, subdivision_ids, flat_edges)