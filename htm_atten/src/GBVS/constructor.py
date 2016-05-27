# -*- coding: Windows-1251 -*-

from graph import Graph
from math import log, exp
from time import clock
import numpy

'''Я не знаю, как наззвать этот файл. Он по карте характеристики (feature  map) строить граф'''


def solve(A, eps=1e-15):
    print "SOLVING MATRIX |",
    u, s, vh = numpy.linalg.svd(A)
    null_space = numpy.compress(s <= eps, vh, axis=0)
    print "SOLVED |",
    return null_space.T


def get_name(i, j):
    return '-'.join([str(i), str(j)])


def distance(a, b, kind):
    if kind == 'log':
        if a == 0:
            a = 0.01
        if b == 0:
            b = 0.01
        return abs(log(float(a)/float(b)))
    if kind == 'mod':
        return abs(a-b)


def f(a, b, sigma):
    return exp(-(a**2+b**2)/(2*sigma**2))


def weight(M, a, b, kind, sigma):
    return distance(M[a[0]][a[1]], M[b[0]][b[1]], kind)*f(a[0]-b[0], a[1]-b[1], sigma)


def normalization_weight(M, a, b, sigma):
    return M[b[0]][b[1]]*f(a[0]-b[0], a[1]-b[1], sigma)


def get_markov_chain(M, sigma, kind='log'):
    start = clock()
    print "MARKOV |",
    g = Graph()
    for i in xrange(len(M)):
        for j in xrange(len(M[i])):
            for p in xrange(len(M)):
                for q in xrange(len(M[i])):
                    if p != i or q != j:
                        g.add_edge(get_name(i, j), get_name(p, q), weight(M, [i, j], [p, q], kind, sigma))
    print "NORMALIZE |",
    g.normalize()
    print "BUILT |",
    return g


def get_normalization_chain(M, sigma):
    g = Graph()
    for i in range(len(M)):
        for j in range(len(M[i])):
            for p in range(len(M)):
                for q in range(len(M[i])):
                    if p != i or q != j:
                        g.add_edge(get_name(i, j), get_name(p, q), normalization_weight(M, [i, j], [p, q], sigma))
    g.normalize()
    return g


def get_matrix(graph):
    start = clock()
    matrix = []
    points = graph.points.keys()
    for p in range(len(points)):
        line = []
        for q in range(len(points)):
            if p == q:
                line.append(-1)
            else:
                element = graph.points[points[q]].edges[points[p]].weight
                #for edge in graph.points[points[q]].edges:
                #    if graph.points[points[q]].edges[edge].destination == points[p]:
                #        element = graph.points[points[q]].edges[edge].weight
                line.append(element)
        matrix.append(line)
    print "MATRIX RECEIVED |",
    return matrix, points


def get_activity_map(matrix, points, width, height):
    activity_map = [[0 for j in range(height)] for i in range(width)]
    a = numpy.array(matrix)
    sol = solve(a)
    try:
        sol = [float(i[0]) for i in sol]
        for i in range(len(sol)):
            x, y = [int(j) for j in points[i].split('-')]
            activity_map[x][y] = sol[i]
        return activity_map
    except IndexError:
        print sol
        return activity_map
    except:
        print 'SOMETHING WENT TERRIBLY WRONG!\nIf this message is on your screen, you are doomed.\nDon`t even try to fix this.'


def normalize_am(am, sigma):
    width = len(am)
    height = len(am[0])
    g = get_normalization_chain(am, sigma)
    m, p = get_matrix(g)
    out = get_activity_map(m, p, width, height)
    del m, p
    return out