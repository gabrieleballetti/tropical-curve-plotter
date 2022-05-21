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
    
    # find flat edges
    flat_edges = []
    for i in range(len(triangles_ids)):
        for j in range(i+1, len(triangles_ids)):
            if np.allclose(normals[i],normals[j]):
                intersection = set(triangles_ids[i]).intersection(set(triangles_ids[j]))
                if len(intersection) == 2:
                    flat_edges.append(intersection)

    return triangles_ids, flat_edges

def plot_subdivision(pts, subdivision_ids, flat_edges=[]):
    # plot the subdivision of the Newton polygon
    for simplex in subdivision_ids:
        for i in range(3):
            id1, id2 = simplex[i], simplex[(i+1) % 3]
            # skip flat edges ()
            if (set([id1, id2]) in flat_edges):
                continue
            edge = np.array([pts[id1], pts[id2]])
            plt.plot(edge[:,0], edge[:,1], color='black')
            plt.plot(pts[id1][0], pts[id1][1], 'ko')
    plt.axis('equal')
    plt.axis('off')
    plt.show()

def plot_curve(pts, subdivision_ids, flat_edges=[]):
    vertices = set()
    edge_to_vert = dict()
    edge_to_third_pt = dict()

    # draw the inner part
    for simplex in subdivision_ids:
        verts = np.take(pts, simplex, 0)
        b = -verts[:, 2]
        A = np.append(verts[:, :2], -np.ones((3,1)), axis=1)
        x = np.linalg.solve(A, b)[:2]
        vertices.add(tuple(x))
        plt.plot(x[0], x[1], 'ko')
        plt.axis('equal')
        for i in range(3):
            edge = frozenset([simplex[i], simplex[(i+1) % 3]])
            if edge in flat_edges:
                continue
            if edge in edge_to_vert:
                x2 = edge_to_vert[edge]
                edge_to_vert.pop(edge)
                edge_to_third_pt.pop(edge)
                plt.plot([x[0],x2[0]], [x[1],x2[1]], color='black')
            else:
                edge_to_vert[edge] = x
                edge_to_third_pt[edge] = simplex[(i+1) % 3]
    
    # draw the tentacles
    for edge in edge_to_vert:
        normals = 
        direction = []]
        print(normals)
        print(direction)



    print(vertices)
    print(edge_to_vert)
    plt.axis('off')
    #plt.show()

pts = [
    [0,0,1],
    [1,0,2],
    [2,0,2],
    [3,0,1],
    [0,1,2],
    [1,1,3],
    [2,1,2],
    [0,2,2],
    [1,2,2],
    [0,3,1]
]


subdivision_ids, flat_edges = upper_hull(pts)
#plot_subdivision(pts, subdivision_ids, flat_edges)
plot_curve(pts, subdivision_ids, flat_edges)