from attention import *
from feature_map import draw_multiple
from time import clock, sleep
import multiprocessing.dummy as mp


def run_test(filename, width, height, scale, radius, cell_size, save_as=None, status=False, mode='rgb'):
    start = clock()
    if status:
        print "STATUS: STARTING TO LOOK AT", filename
        local = clock()
    if 'r' in mode:
        red = FeatureMap()
        red.load(filename, width, height, 'r')
        red = get_saliency_map(red, fc, fd, radius, cell_size)
        red.normalize()
        if status:
            print "STATUS: RED IS DONE IN", clock()-local
            local = clock()
    if 'g' in mode:
        green = FeatureMap()
        green.load(filename, width, height, 'g')
        green = get_saliency_map(green, fc, fd, radius, cell_size)
        green.normalize()
        if status:
            print "STATUS: GREEN IS DONE IN", clock()-local
            local = clock()
    if 'b' in mode:
        blue = FeatureMap()
        blue.load(filename, width, height, 'b')
        blue = get_saliency_map(blue, fc, fd, radius, cell_size)
        blue.normalize()
        if status:
            print "STATUS: BLUE IS DONE IN", clock()-local
    if 'h' in mode:
        hue = FeatureMap()
        hue.load(filename, width, height, 'h')
        hue = get_saliency_map(hue, fc, fd, radius, cell_size, True)
        hue.normalize()
        if status:
            print "STATUS: HUE IS DONE IN", clock()-local
            local = clock()
    if 's' in mode:
        sat = FeatureMap()
        sat.load(filename, width, height, 's')
        sat = get_saliency_map(sat, fc, fd, radius, cell_size)
        sat.normalize()
        if status:
            print "STATUS: SATURNATION IS DONE IN", clock()-local
            local = clock()
    if 'v' in mode:
        val = FeatureMap()
        val.load(filename, width, height, 'v')
        val = get_saliency_map(val, fc, fd, radius, cell_size)
        val.normalize()
        if status:
            print "STATUS: VALUE IS DONE IN", clock()-local
            local = clock()
    try:
        features = []
        if 'r' in mode:
            features.append(red)
        if 'g' in mode:
            features.append(green)
        if 'b' in mode:
            features.append(blue)
        if 'h' in mode:
            features.append(hue)
        if 's' in mode:
            features.append(sat)
        if 'v' in mode:
            features.append(val)
        draw_multiple(features, 0, 0, scale, save_as, bw=False)
    except SystemExit:
        if status:
            print "STATUS: DRAWN IN", clock()-local
        print "STATUS: ENDED IN", clock()-start


def thread_function(filename, width, height, feature, radius, cell_size):
    start = clock()
    feature_map = FeatureMap()
    feature_map.load(filename, width, height, feature)
    print feature+' loaded in '+str(clock()-start)+'\n'
    feature_map.normalize()
    print feature+' normalized in '+str(clock()-start)+'\n'
    feature_map = get_saliency_map(feature_map, fc, fd, radius, cell_size)
    print feature+' process in '+str(clock()-start)+'\n'
    feature_map.normalize(compress=True)
    print feature+' '+str(clock()-start)+'\n'
    return feature_map


def run_multiprocess_test(filename, width, height, scale, radius, cell_size, save_as=None, status=False, mode='rgb'):
    print "STARTING: ", filename
    start = clock()
    p = mp.Pool(3)
    features = p.map(lambda f: thread_function(filename, width, height, f, radius, cell_size), mode)
    try:
        draw_multiple(features, 0, 0, scale, save_as, bw=False)
    except SystemExit:
        print "STATUS: ENDED IN", clock()-start


def run_test_layers(filename, width, height, scale, layers, save_as=None, status=False, mode='rgb'):
    start = clock()
    if status:
        print "STATUS: STARTING TO LOOK AT", filename
        local = clock()
    if 'r' in mode:
        red = FeatureMap()
        red.load(filename, width, height, 'r')
        red = legal(red, fc, layers)
        red.normalize()
        if status:
            print "STATUS: RED IS DONE IN", clock()-local
            local = clock()
    if 'g' in mode:
        green = FeatureMap()
        green.load(filename, width, height, 'g')
        green = legal(green, fc, layers)
        green.normalize()
        if status:
            print "STATUS: GREEN IS DONE IN", clock()-local
            local = clock()
    if 'b' in mode:
        blue = FeatureMap()
        blue.load(filename, width, height, 'b')
        blue = legal(blue, fc, layers)
        blue.normalize()
        if status:
            print "STATUS: BLUE IS DONE IN", clock()-local
    if 'h' in mode:
        hue = FeatureMap()
        hue.load(filename, width, height, 'h')
        hue = legal(hue, fc, layers)
        hue.normalize()
        if status:
            print "STATUS: HUE IS DONE IN", clock()-local
            local = clock()
    if 's' in mode:
        sat = FeatureMap()
        sat.load(filename, width, height, 's')
        sat = legal(sat, fc, layers)
        sat.normalize()
        if status:
            print "STATUS: SATURNATION IS DONE IN", clock()-local
            local = clock()
    if 'v' in mode:
        val = FeatureMap()
        val.load(filename, width, height, 'v')
        val = legal(val, fc, layers)
        val.normalize()
        if status:
            print "STATUS: VALUE IS DONE IN", clock()-local
            local = clock()
    try:
        features = []
        if 'r' in mode:
            features.append(red)
        if 'g' in mode:
            features.append(green)
        if 'b' in mode:
            features.append(blue)
        if 'h' in mode:
            features.append(hue)
        if 's' in mode:
            features.append(sat)
        if 'v' in mode:
            features.append(val)
        draw_multiple(features, 0, 0, scale, save_as, bw=False)
    except SystemExit:
        if status:
            print "STATUS: DRAWN IN", clock()-local
        print "STATUS: ENDED IN", clock()-start
