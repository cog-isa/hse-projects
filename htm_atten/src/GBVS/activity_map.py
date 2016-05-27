from constructor import *


def build_activity_map(test, sigma, iterations):
    try:
        width, height = len(test), len(test[0])
        graph = get_markov_chain(test, sigma)
        matrix, points = get_matrix(graph)
        del graph
        activity_map = get_activity_map(matrix, points, width, height)
        for i in range(iterations):
            print "NORMALIZATION STEP", i+1, '|',
            activity_map = normalize_am(activity_map, sigma)
        print
        return activity_map
    except:
        print "something went  wrong"
        return test

M = [[1, 2, 3, 2, 1],
     [2, 2, 3, 2, 2],
     [3, 3, 3, 3, 3],
     [2, 2, 2, 2, 2],
     [1, 2, 3, 2, 1]]
