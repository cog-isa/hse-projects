from test import run_test, run_test_layers
import os

def get_complex_name(layers):
    name = ''
    for layer in layers:
        name += str(layer[0]) + '-' + str(layer[1])+'_'
    return name[:-1]


def add_to_dataset(dataset, info):
    item = {}
    item['path'] = info[0]
    item['name'] = info[1]
    item['width'] = info[2]
    item['height'] = info[3]
    item['scale'] = info[4]
    item['radius'] = info[5]
    item['cellsize'] = info[6]
    item['saveas'] = info[7]
    dataset.append(item)
    return dataset


def test_formed_set(name, number, size, scale, layers, mode, subfolder=''):
    if subfolder:
        try:
            os.stat('results/'+name+subfolder)
        except:
            os.mkdir('results/'+name+subfolder)
    for i in range(1, number+1):
        run_test_layers('tests/'+name+'/test'+str(i)+'.bmp', size[0], size[1], scale, layers,
                 save_as='results/'+name+subfolder+'/test'+str(i)+mode+'.png', status=True, mode=mode)



def test_raw_set(dataset, mode):
    for item in dataset:
        run_test_layers(item['path']+item['name'], item['width'], item['height'], item['scale'], item['radius'],
                 item['cellsize'], save_as=item['path']+item['saveas'], status=True, mode=mode)


def form_people_set():
    people_dataset = []
    people_dataset = add_to_dataset(people_dataset, ['tests/people2/', 'gosha.bmp', 90, 120, 3, 10, 5, 'results/people2/gosha-rgb.png'])
    people_dataset = add_to_dataset(people_dataset, ['tests/people2/', 'batya.bmp', 100, 100, 3, 10, 5, 'results/people2/batya-rgb.png'])
    people_dataset = add_to_dataset(people_dataset, ['tests/people2/', 'steffy.bmp', 100, 100, 3, 10, 5, 'results/people2/steffy-rgb.png'])
    people_dataset = add_to_dataset(people_dataset, ['tests/people2/', 'valera.bmp', 100, 130, 3, 10, 5, 'results/people2/valera-rgb.png'])
    people_dataset = add_to_dataset(people_dataset, ['tests/people2/', 'larik.bmp', 100, 100, 3, 10, 5, 'results/people2/larik-rgb.png'])
    people_dataset = add_to_dataset(people_dataset, ['tests/people2/', 'me.bmp', 180, 200, 3, 10, 5, 'results/people2/me-rgb.png'])
    people_dataset = add_to_dataset(people_dataset, ['tests/people2/', 'artur.bmp', 240, 320, 3, 10, 5, 'results/people2/artur-rgb.png'])
    people_dataset = add_to_dataset(people_dataset, ['tests/people2/', 'igor.bmp', 200, 360, 3, 10, 5, 'results/people2/igor-rgb.png'])
    return people_dataset


def test_people_64x48(number, scale, layers, mode, subfolder=''):
    test_formed_set('people', number, [64, 48], scale, layers, mode, subfolder)


def test_dogs_120x90(number, scale, layers, mode, subfolder=''):
    test_formed_set('dogs', number, [120, 90], scale, layers, mode, subfolder)


def test_people_320x240(number, scale, layers, mode, subfolder=''):
    test_formed_set('people_big', number, [320, 240], scale, layers, mode, subfolder)


def try_layers(test_function, tests_number, scale, layers_vars, mods):
    for layers in layers_vars:
        for mode in mods:
            print "TESTING..."
            print "MODE:", mode
            print "LAYERS:", layers
            test_function(tests_number, scale, layers, mode, subfolder='/'+mode+'_'+get_complex_name(layers)+'/')
