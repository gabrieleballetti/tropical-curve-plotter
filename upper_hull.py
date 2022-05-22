import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import ConvexHull

def preprocess_points(pts):
    # add a dummy point to avoid "flat" configurations
    new_pt = [pts[0][0], pts[0][1], pts[0][2] - 1]
    pts.append(new_pt)
    return pts

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
    ax = plt.subplot()
    for simplex in subdivision_ids:
        for i in range(3):
            id1, id2 = simplex[i], simplex[(i+1) % 3]
            # skip flat edges ()
            if (set([id1, id2]) in flat_edges):
                continue
            edge = np.array([pts[id1], pts[id2]])
            ax.plot(edge[:,0], edge[:,1], color='black')
            ax.plot(pts[id1][0], pts[id1][1], 'ko')
    ax.axis('equal')
    ax.axis('off')
    plt.show()

def plot_curve(pts, subdivision_ids, flat_edges=[]):
    ax = plt.subplot()
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
        ax.plot(x[0], x[1], 'ko')
        ax.axis('equal')
        for i in range(3):
            edge = frozenset([simplex[i], simplex[(i+1) % 3]])
            if edge in flat_edges:
                continue
            if edge in edge_to_vert:
                x2 = edge_to_vert[edge]
                edge_to_vert.pop(edge)
                edge_to_third_pt.pop(edge)
                ax.plot([x[0], x2[0]], [x[1], x2[1]], color='black')
            else:
                edge_to_vert[edge] = x
                edge_to_third_pt[edge] = simplex[(i+2) % 3]
    
    # find bounding box, used to decide length of the tentacles (lazy way, don't judge)
    x_min = min([pt[0] for pt in vertices])
    x_max = max([pt[0] for pt in vertices])
    y_min = min([pt[1] for pt in vertices])
    y_max = max([pt[1] for pt in vertices])
    x_min -= max((x_max - x_min) * 0.1, 2)
    x_max += max((x_max - x_min) * 0.1, 2)
    y_min -= max((y_max - y_min) * 0.1, 2)
    y_max += max((y_max - y_min) * 0.1, 2)

    # draw the tentacles
    for edge in edge_to_vert:
        # find the direction
        e = np.take(pts, list(edge), 0)[:, :2]
        e_dir = e[1] - e[0]
        normal = np.array([-e_dir[1], e_dir[0]])
        normal = normal/np.linalg.norm(normal)
        
        # check that the edge normal points externally
        outer_vec = e[0] - pts[int(edge_to_third_pt[edge])][:2]
        normal = normal if np.dot(normal, outer_vec) > 0 else -normal

        point = edge_to_vert[edge]
        t_x = ((x_max if normal[0] >= 0 else x_min) - point[0]) / normal[0] if abs(normal[0]) > 1e-09 else float('inf')
        t_y = ((y_max if normal[1] >= 0 else y_min) - point[1]) / normal[1] if abs(normal[1]) > 1e-09 else float('inf')
        end = point + min(t_x, t_y)*normal
        ax.plot([point[0], end[0]], [point[1], end[1]], color='black')
        
    ax.set_xticks([]) 
    ax.set_yticks([])
    plt.show()



pts = []

deg = 4

for i in range(deg + 1):
    for j in range(deg + 1):
        if i + j > deg:
            continue
        k = deg - i - j
        pts.append([i,j,np.random.randint(-20, 20)])
        #pts.append([i, j, np.sqrt(i*j*k)])

print(pts)

pts = preprocess_points(pts)
subdivision_ids, flat_edges = upper_hull(pts)
plot_subdivision(pts, subdivision_ids, flat_edges)
plot_curve(pts, subdivision_ids, flat_edges)