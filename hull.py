'''
Module in charge of computing lower/upper hull of a point configuration
'''

import numpy as np
from scipy.spatial import ConvexHull

def compute_lu_hull(points, use_min_convention):
    '''
    Given a list of 3D points compute the lower/upper hull (depending on the convention)
    and return a subdivision and a list of "flat" edges (those between faces with same normal)
    '''
    lu_hull = ConvexHull(points=points)
    sign = 1 if use_min_convention else -1
    lu_hull_ids = [i for i, eq in enumerate(lu_hull.equations) if eq[2] * sign < 0]
    triangles_ids = np.array([lu_hull.simplices[i] for i in lu_hull_ids])
    normals = np.take(lu_hull.equations, lu_hull_ids, 0)[:,0:3]

    # find "flat" edges, could be done faster than quadratic times
    # (for example by sorting the equations), but I'm lazy :)
    flat_edges = []
    for i in range(len(triangles_ids)):
        for j in range(i+1, len(triangles_ids)):
            if np.allclose(normals[i], normals[j]):
                intersection = set(triangles_ids[i]).intersection(set(triangles_ids[j]))
                if len(intersection) == 2:
                    flat_edges.append(intersection)

    return triangles_ids, flat_edges
    