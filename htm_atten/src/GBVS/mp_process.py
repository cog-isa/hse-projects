import multiprocessing.dummy as multiprocessing
from process import *
from time import sleep


def process(sigma, iterations):
    start = clock()
    print "STATUS: STARTING"
    mode = 'rgb'
    tests = []
    results = []
    for j in range(3):
        tests.append(load_test("pgmvis/pictures/test3.bmp", 40, 40, mode[j]))
    print "STATUS: BUILDING ACTIVITY MAPS"
    p = multiprocessing.Pool(processes=3)
    results = p.map(lambda i: build_activity_map(tests[i], sigma, iterations), range(3))
    p.close()
    p.join()
    print "STATUS: ACTIVITY MAP WAS BUILT SUCCESSFULLY"
    #except:
    #    print "STATUS: ACTIVITY MAP WAS FAILED"
    for j in range(3):
        try:
            print j
            print results[j]
            draw_picture(results[j], "pgmvis/pictures/"+str(j)+".bmp", 0, 0, 10, "normalized", True)
        except SystemExit:
            sleep(1)
    print "STATUS: FINISHED"
    print "TOTAL TIME:", clock()-start
    print "============================================="

#from multiprocessing import cpu_count
#print cpu_count()
#process(2, 0)
#main()