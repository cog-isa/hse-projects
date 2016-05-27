from engine.datasets import *

layers_vars = [[[10, 2], [10, 4], [10, 8], [10, 16]],
               [[6, 1], [10, 8]],
               [[6, 1], [6, 2], [10, 8]],
               [[6, 1], [6, 2], [6, 4], [10, 8]]]

try_layers(test_people_64x48, 10, 5, layers_vars, ['rgb'])
