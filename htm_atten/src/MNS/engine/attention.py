from feature_map import FeatureMap
from math import log, exp, sin, pi


def d(v0, v1, cycled=False):
    max_value = 360
    k = pi/max_value
    alpha = 0.8
    if cycled:
        max_value = 180
    else:
        max_value = 255
    return max_value*sin(k*(abs(v0-v1)))**alpha

def F(dx, dy, sigma):
    if dx == dy == 0:
        return 0
    return 1/(dx**2+dy**2)**sigma


def fc(a, b, sigma=0.1, cycled=False):
    x0, y0, v0 = a
    x1, y1, v1 = b
    return d(v0, v1, cycled)*F(x1-x0, y1-y0, sigma)


def fd(a, b, sigma=0.05, cycled=False):
    x0, y0, v0 = a
    x1, y1, v1 = b
    return d(v0, v1, cycled)*F((x1-x0)/2, (y1-y0)/2, sigma)


def get_saliency_layer(feature, function, radius, cell_size, cycled):
    w = len(feature.map)
    h = len(feature.map[0])
    saliency = FeatureMap()
    saliency.map = [[0 for i in range(h)] for j in range(w)]
    cw = w/cell_size
    ch = h/cell_size
    cells = FeatureMap()
    cells.map = [[0 for i in range(ch)] for j in range(cw)]
    for x in range(w):
        for y in range(h):
            cells.map[x/cell_size][y/cell_size] += feature.map[x][y]/float(cell_size)**2
    for x0 in range(w):
        for y0 in range(h):
            n = 0
            for x in range(max(0, x0/cell_size-radius), min(x0/cell_size+radius+1, cw)):
                for y in range(max(0, y0/cell_size-radius), min(y0/cell_size+radius+1, ch)):
                    saliency.map[x0][y0] += function([x0, y0, feature.map[x0][y0]], [x, y, cells.map[x][y]], cycled=cycled)
                    n += 1
            if saliency.map[x0][y0]:
                saliency.map[x0][y0] /= n
    saliency.normalize(True)
    return saliency



def get_close_map(feature, radius, function, cycled):
    w = len(feature.map)
    h = len(feature.map[0])
    saliency = FeatureMap()
    saliency.map = [[0 for i in range(h)] for j in range(w)]
    for x0 in range(w):
        for y0 in range(h):
            n = 0
            for x in range(max(0, x0-radius), min(x0+radius+1, w-1)):
                for y in range(max(0, y0-radius), min(y0+radius+1, h-1)):
                    saliency.map[x0][y0] += function([x0, y0, feature.map[x0][y0]], [x, y, feature.map[x][y]], cycled=cycled)
                    n += 1
            saliency.map[x0][y0] /= n
    saliency.normalize(True)
    return saliency


def get_distant_map(feature, cell_size, function, cycled):
    w = len(feature.map)
    h = len(feature.map[0])
    saliency = FeatureMap()
    saliency.map = [[0 for i in range(h)] for j in range(w)]
    cw = w/cell_size
    ch = h/cell_size
    cells = FeatureMap()
    cells.map = [[0 for i in range(ch)] for j in range(cw)]
    for x in range(w):
        for y in range(h):
            cells.map[x/cell_size][y/cell_size] += feature.map[x][y]/float(cell_size)**2
    for x0 in range(w):
        for y0 in range(h):
            n = 0
            for x in range(w/cell_size):
                for y in range(h/cell_size):
                    saliency.map[x0][y0] += function([x0, y0, feature.map[x0][y0]], [x, y, cells.map[x][y]], cycled=cycled)
                    n += 1
            saliency.map[x0][y0] /= n
    saliency.normalize(True)
    return saliency


def get_saliency_map(feature, close_function, distant_function, radius, cell_size, cycled=False):
    dm = get_distant_map(feature, cell_size, distant_function, cycled)
    return get_close_map(feature, radius, close_function, cycled)+dm


def legal(feature, function, layers, cycled=False):
    saliency = get_saliency_layer(feature, function, layers[0][0], layers[0][1], cycled)
    for i in range(1, len(layers)):
        saliency = saliency + get_saliency_layer(feature, function, layers[i][0], layers[i][1], cycled)
    return saliency