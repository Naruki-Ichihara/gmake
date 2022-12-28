from svgpathtools import svg2paths, Line, Path, Arc
import numpy as np
from tsp_solver.greedy import solve_tsp

def _bezier2lines(bezier, division=10):
    ts = np.arange(0, 1+1/division, 1/division)
    points = bezier.points(ts)
    lines = []
    for i in range(len(points)-1):
        lines.append(Line(points[i], points[i+1]))
    return lines

def _arc2lines(arc, division=10):
    ts = np.arange(0, 1+1/division, 1/division)
    points = [arc.point(t) for t in ts]
    lines = []
    for i in range(len(points)-1):
        lines.append(Line(points[i], points[i+1]))
    return lines

def _curve2lines(curve, division=10):
    if isinstance(curve, Arc):
        lines = _arc2lines(curve, division)
    else:
        lines = _bezier2lines(curve, division)
    return lines

def bezierPath2LinePaths(path, division=10):
    elements = []
    for element in path:
        elements.extend(_curve2lines(element, division))
    return Path(*elements)

def paths2LinePaths(paths, division=10, sorting=True, tsp_step=10):
    linepaths = [bezierPath2LinePaths(path, division) for path in paths]
    if sorting:
        linepaths = sortPaths(linepaths, step=tsp_step)
    return linepaths

def readSVG(fname, sorting=False, tsp_step=10, with_attr=False):
    paths, attrs = svg2paths(fname)
    if sorting:
        paths = sortPaths(paths, step=tsp_step)
    if with_attr:
        return paths, attrs
    else:
        return paths

def _make_points(paths):
    xy = []
    for path in paths:
        x0 = path.start.real
        y0 = path.start.imag
        xy.append([x0, y0])
    for path in paths:
        x1 = path.end.real
        y1 = path.end.imag
        xy.append([x1, y1])
    return np.array(xy)

def _make_distance(x, y):
    N = len(x)
    N_path = int(len(x)/2)
    xx = np.vstack((x,)*N)
    yy = np.vstack((y,)*N)
    dist = np.sqrt((xx - xx.T)**2 + (yy - yy.T)**2)
    np.fill_diagonal(dist, 0)
    np.fill_diagonal(dist[:, N_path:], 0)
    np.fill_diagonal(dist[N_path:, :], 0)
    return dist

def sortPaths(paths, step=3):
    for i in range(step):
        xy = _make_points(paths)
        dist = _make_distance(xy[:,0], xy[:,1])
        routes = solve_tsp(dist, optim_steps=10, endpoints=(0, None))
        sorted_paths = []
        for i in range(len(routes[::2])):
            if routes[::2][i] >= len(routes)/2:
                index = int(routes[::2][i] - len(routes)/2)
                sorted_paths.append(paths[index].reversed())
            else:
                sorted_paths.append(paths[routes[::2][i]])
        paths = sorted_paths
    return sorted_paths



