'''
Main file
'''

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import matplotlib.pyplot as plt
import numpy as np

import config
import hull
import curve
import subdivision

def parse(filename):
    '''
    Parse points from the input files
    '''
    file = open(filename, 'r', encoding="utf-8")
    points = []
    for line in file:
        point = [float(n) for n in line.split()]
        if len(point) == 3:
            points.append(point)
    file.close()
    return points

def preprocess_points(points, use_min_convention):
    '''
    Add a dummy point to avoid "flat" configurations
    '''
    sign = 1 if use_min_convention else -1
    new_pt = [points[0][0], points[0][1], points[0][2] + sign]
    points.append(new_pt)
    return np.array(points)

def main():
    '''
    Main function. Parse arguments and plot depending on the given flags
    '''
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("input", help="Input file name")
    parser.add_argument("-c", "--convention", default="min", const="min", nargs="?",
        choices=['min', 'max'], help="Choos between min/max convention (default: %(default)s)")
    parser.add_argument("-n", "--newton", action="store_true",
        help="Plot the subdivided Newton polygon instead")
    parser.add_argument("-o", "--output", help="Output file name (default = .png)")
    args = vars(parser.parse_args())

    # parse arguments
    use_min_convention = args["convention"] != "max"
    plot_newton = args['newton']
    in_filename = args['input']
    out_filename = args['output']

    # load the list of points
    list_points = parse(in_filename)
    if len(list_points) < 3:
        raise SystemExit('At least three monomials are needed')

    # preprocessing
    points = preprocess_points(list_points, use_min_convention)
    subdivision_ids, flat_edges = hull.compute_lu_hull(points, use_min_convention)

    # plot
    ax = plt.subplot()
    if plot_newton:
        subdivision.plot(ax, points, subdivision_ids, flat_edges)
    else:
        curve.plot(ax, points, subdivision_ids, flat_edges, use_min_convention)
    ax.axis('equal')
    ax.axis('off')

    if out_filename is not None:
        plt.savefig(out_filename, dpi=config.OUTPUT_DPI)
    else:
        plt.show()

if __name__ == "__main__":
    main()
