from pgmvis.visualizer import load_test, draw_picture, draw_merged_picture
from activity_map import build_activity_map
from time import clock
import pygame

# standard of pictures
X0 = 0
X1 = 290
Y0 = 0
SCALE = 10


def process_fmap(fmap, sigma, iterations, save_as):
    start = clock()
    print "STARTING |",
    try:
        fmap = build_activity_map(fmap, sigma, iterations)
        print "ACTIVITY MAP WAS BUILT |",
    except:
        print "ACTIVITY MAP WAS FAILED |"
    try:
        draw_picture(fmap, save_as, X0, Y0, SCALE, 'normalized', to_save=True)
    except SystemExit:
        pass
    print "TOTAL TIME:", clock()-start
    print "============================================="


def full_work(path, save_as, w, h, sigma, iterations, mode='a'):
    fmap = load_test(path, w, h, mode)
    process_fmap(fmap, sigma, iterations, save_as)


def full_for_all(path, save_as, w, h, sigma, iterations, mode):
    print "STATUS: LOADING",
    features = [load_test(path, w, h, m) for m in mode]
    print '|'
    features = [build_activity_map(i, sigma, iterations) for i in features]
    draw_merged_picture(features, save_as, 0, 0, 10, "normalized", True)


def main():
    start = clock()
    for n in [5]:
        for sigma in [2, 2.5, 3, 3.5, 4]:
            for iterations in [0, 1, 2]:
                for mode in ["all", "r", "g", "b"]:
                    filename = "pgmvis/pictures/" + str(n) + "-" + str(int(2*sigma)) + "-" + str(iterations) + "-" + \
                               mode + ".bmp"
                    print "PROCESSING:", filename
                    try:
                        full_work("pgmvis/pictures/test"+str(n)+".bmp", filename, 40, 40, sigma, iterations, mode)
                    except:
                        pass
    t = clock()-start
    print 'total time for 3*5*3*4 =',  t
    print 'per one =', t/180


#main()


inputs = []
for sigma in [4, 5, 6]:
        for iterations in range(3):
            inputs.append([sigma, iterations])

process_people = False
if process_people:
    for name in ["test"+str(i) for i in range(1, 8)]:
        try:
            full_for_all("pgmvis/pictures/tests/people/"+name+".bmp", 'pgmvis/pictures/results/rgb/people/' + name + '.png',
                         64, 48, 5, 0, 'rgb')
        except SystemExit:
            pass

go = False
if go:
    for j in range(5, 10):
        i = str(j)
        for inp in inputs:
            sigma, iterations = inp
            print 'No:', i, 'Sigma:', sigma, 'Iterations:', iterations
            start = clock()
            try:
                full_for_all("pgmvis/pictures/tests/people/test"+i+".bmp", 'pgmvis/pictures/results/people/test'+i+'-'+str(sigma)+'-'+str(iterations)+'.png',
                             64, 48, sigma, iterations, 'rgb')
            except SystemExit:
                print 'total:', clock()-start
go = True
if go:
    for j in range(13, 42):
        i = str(j)
        for inp in inputs:
            sigma, iterations = inp
            print 'No:', i, 'Sigma:', sigma, 'Iterations:', iterations
            start = clock()
            try:
                full_for_all("pgmvis/pictures/tests/people/test"+i+".bmp", 'pgmvis/pictures/results/people/test'+i+'-'+str(sigma)+'-'+str(iterations)+'.png',
                             64, 48, sigma, iterations, 'rgb')
            except SystemExit:
                print 'total:', clock()-start