from PIL import Image, ImageDraw
from numpy import array
from numpy import zeros
from numpy import ndarray
import numpy as np
import cv2
import random
from elementtree import ElementTree as ET
from matplotlib import pyplot as plt
import os as os

class Feature:
    def __init__(self, x, y):
        self.x = x
        self.y = y
class Predictor:
    def __init__(self, F_src, S, F_tgt, A):
        self.F_src = F_src
        self.S = S
        self.F_tgt = F_tgt
        self.A = A
    def _out_(self):
        print self.A, " "

windowSize = 50 # size of area where cannot be more than 1 predictor
def isPointInRect ((Px, Py), (Rx, Ry), windowSize):
    if (Px < Rx - windowSize or Px > Rx + windowSize):
        return False
    if (Py < Ry - windowSize or Py > Ry + windowSize):
        return False
    return True
def saccadeDistance (S1, S2):
    delta_x = S1.x-S2.x
    delta_y = S1.y-S2.y
    return np.sqrt(delta_x*delta_x+delta_y*delta_y)

N = 3 # number of attractors
SD = 50 #epsilon of saccade distance
folder_name = ['Giraffe/', 'Cat/', 'Dog/']
predictors = []
Attractor = []
for i in range(N):
    Attractor.append([])

for attractor in range(N):
    path_to_image = folder_name[attractor]
    for j in os.listdir(path_to_image):
        img = cv2.imread(path_to_image + j)
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_img = np.float32(gray_img)
        blockSize = 2;
        kSize = 3;
        dst = cv2.cornerHarris(gray_img, blockSize, kSize, 0.04)
        features = []
        corners =  np.where (dst > 0.2*dst.max())
        for i in range(len(corners[0])):
            x = corners[0][i]
            y = corners[1][i]
            img[(x, y)] = [0, 255, 0]
            if len (features) == 0:
                features.append(Feature(y, x))
            else:
                f = False
                for j in features:
                    if isPointInRect((x, y), (j.y, j.x), windowSize) == True:
                        f = True
                        break
                if f == False:
                    features.append(Feature(y, x))
        for i in range (len(features)):
            img = cv2.circle (img, (features[i].x, features[i].y), 10, (0,255,0), 3)
            # print features[i].x, features[i].y
            # print '\n'
            l = i
            while (l == i):
                l = random.randint(0, len(features)-1)
                S = Feature (features[l].x-features[i].x, features[l].y-features[i].y)
                if l != i:
                    predictors.append(Predictor(features[i], S, features[l], attractor));
        # cv2.imwrite(path_to_image + "1_1.png", img)
        # cv2.imshow('', img)
        # if cv2.waitKey(0):
        #     cv2.destroyAllWindows()

root = ET.Element('root')
for i in range (len(predictors)):
    predictor_tag = ET.SubElement(root, 'Predictor', number = str(i))
    F_src_tag = ET.SubElement(predictor_tag, 'F_src')
    x_tag = ET.SubElement(F_src_tag, 'x').text = str(predictors[i].F_src.x)
    y_tag = ET.SubElement(F_src_tag, 'y').text = str(predictors[i].F_src.y)
    Saccade_tag = ET.SubElement(predictor_tag, 'S')
    x_tag = ET.SubElement(Saccade_tag, 'x').text = str(predictors[i].S.x)
    y_tag = ET.SubElement(Saccade_tag, 'y').text = str(predictors[i].S.y)
    F_tgt_tag = ET.SubElement(predictor_tag, 'F_tgt')
    x_tag = ET.SubElement(F_tgt_tag, 'x').text = str(predictors[i].F_tgt.x)
    y_tag = ET.SubElement(F_tgt_tag, 'y').text = str(predictors[i].F_tgt.y)
    A_tag = ET.SubElement(predictor_tag, 'Attractor').text = str(predictors[i].A)
tree = ET.ElementTree(root)
tree.write("predictors.xml")
