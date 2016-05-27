from PIL import Image, ImageDraw
from numpy import array
from numpy import zeros
from numpy import ndarray
import numpy as np
import cv2
import random
from elementtree import ElementTree as ET
np.set_printoptions(threshold=np.nan)

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

# function defines if some point is laying within some square area
def isPointInRect ((Px, Py), (Rx, Ry), predictorArea):
    if (Px < Rx - predictorArea or Px > Rx + predictorArea):
        return False
    if (Py < Ry - predictorArea or Py > Ry + predictorArea):
        return False
    return True
# Euclidean 2-D distance
def distance (S1, S2):
    delta_x = S1.x-S2.x
    delta_y = S1.y-S2.y
    return np.sqrt(delta_x*delta_x+delta_y*delta_y)
# sign function
def sign (a):
    ans = np.zeros((Constants.n, 1))
    for i in range(Constants.n):
        if (a[i,0] <= 0):
            ans[i,0] = -1
        else:
            ans[i,0] = 1
    return ans

#Habor filter
def getFeatures (img):
    predictorArea = 50 # area size containing only 1 predictor
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    grayimg = np.float32(gray_img)
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
                if isPointInRect((x, y), (j.y, j.x), predictorArea) == True:
                    f = True
                    break
            if f == False:
                features.append(Feature(y, x))
    return features

def getPredictors ():
    predictors = []
    tree = ET.parse('predictors.xml')
    root = tree.getroot()
    for predictor in root:
        F_src = Feature(int(predictor[0][0].text), int(predictor[0][1].text))
        S = Feature (int(predictor[1][0].text), int(predictor[1][1].text))
        F_tgt = Feature(int(predictor[2][0].text), int(predictor[2][1].text))
        A = int(predictor[3].text)
        predictors.append(Predictor(F_src, S, F_tgt, A))
    return predictors

#Constants
class Constants:
    N = 3; # number of attractors
    saccadeEps = 50 #epsilon of saccade distance
    folder_name = ['Giraffe/', 'Cat/', 'Dog/']
    n = 0; # number of predictors
    a = 50; #number of random chosen predictors which are 1
    t = 0.5; #threshold
    foveaArea = 50
    s = 5; #number of activated predictors of same attractor

def setPredictorsNumber (predictors):
    Constants.n = len(predictors)

def getInputImage (pathToImage):
    img = cv2.imread(pathToImage)
    return img

#initialize Attractors (matrix)
def getAttractors(predictors):
    A_mu = np.zeros((Constants.N, Constants.n))
    for i in range(Constants.n):
        for j in range(Constants.N):
            if predictors[i].A == j:
                A_mu[j,i] = 1
            else:
                A_mu[j,i] = -1
    return A_mu

# marking features on picture
def setFeaturesOnImage (features, img, color):
    for i in features:
        img = cv2.circle (img, (i.x, i.y), 10, color, 3)
# function
def showImage(title, img):
    cv2.imshow(title, img)
    if cv2.waitKey(0):
        cv2.destroyAllWindows()

# matrix of Hopfield network
def createMatrixJ (predictors):
    J = np.zeros((Constants.n, Constants.n))
    for i in range(Constants.n):
        for j in range(Constants.n):
            if predictors[i].A == predictors[j].A:
                J[i,j] = 1
                J[j,i] = 1
    np.fill_diagonal(J, 0)
    return J

#generate A vector where P(A[i] = 1) = a
def getAVector (a):
    A = np.zeros((Constants.n,1))
    A.fill(-1)
    A[random.sample(range(Constants.n), a), 0] = 1
    return A
# function
def setPointOnImage (point, img, color):
    img = cv2.circle (img, (point.x, point.y), 10, color, 3)
# function
def showInitialPredictors (A, img, color):
    for i in range(Constants.n):
        if A[i,0] == 1:
            setPointOnImage(predictors[i].F_src, img, color)
    showImage("Active Predictors after step", img)
# function
def showRP (RP, img, color):
    for i in RP:
        setPointOnImage(predictors[i].F_src, img, color)
    showImage("Relevant predictors", img)
# function
def showSaccade (fovea, S_best, img):
     img = cv2.arrowedLine(img, (fovea.x-predictors[S_best].S.x, fovea.y-predictors[S_best].S.y), (fovea.x, fovea.y), (0,255,0))
     img = cv2.circle (img, (fovea.x, fovea.y), 10, (0,100,255), 3)
     showImage("Saccade and F_tgt", img)
# Activate s random same category predictors
def activateSameAttractorPredictors (j, A):
    category = predictors[j].A
    freePositions = []
    for i in range(Constants.n):
        if A[i,0] == -1 and predictors[i].A == category:
            freePositions.append(i)
    #list of s random indexes of freepoStition
    if (Constants.s > len(freePositions)):
        Constants.s = len(freePositions)
    randPositions = random.sample(freePositions, Constants.s)
    finalPositions = []
    for i in randPositions:
        finalPositions.append(i)
    A[finalPositions] = 1
    for i in finalPositions:
        setPointOnImage(predictors[i].F_src, img, (128,256,128))
    #showImage("S activated predictors", img)
# getting R vector (Equation 6)
def getR (A_, J):
    return np.dot(J, A_)/2
# updating A (Equation 5)
def updateA (A, R, NR):
    A = sign(R-NR)
def showUpdatedVectorA(A, img, color):
    for i in range(Constants.n):
        if (A[i,0] == 1):
            setPointOnImage(predictors[i].F_src, img, color)
    showImage("Updated Vector A", img)
# get Percentage of similar active predictors for each category
def getSimilarityPercentage (A, A_mu):
    votes = np.zeros((Constants.N, Constants.n))
    ans = []
    for i in range (Constants.n):
        for j in range (Constants.N):
            if (A[i,0] == 1 and A_mu[j, i] == 1): #if 1 on the same position in A and Attractor, then give 1 vote for that
                votes[j, i] = 1
    for i in range(Constants.N):
        ans.append(sum(votes[i,:])/sum(A_mu[i,:] == 1))
    return ans
# define a winner, i.e. attractor, having percent of active predictors > t
def getWinner (percentages):
    for i in range(Constants.N):
        if (percentages[i] > Constants.t):
            print Constants.folder_name[i]
            return i
    return -1
predictors = getPredictors()
img = getInputImage(Constants.folder_name[2] + '1.png')
setPredictorsNumber(predictors)
features = getFeatures(img)
setFeaturesOnImage(features, img, (0,255,0))
A_mu = getAttractors(predictors)
# showImage("Detected Features", img)
A = getAVector(Constants.a)
#showGeneratedPredictors(A, img, (100, 255, 255))
J = createMatrixJ(predictors)

A_ = np.zeros((Constants.n, 1))
NR = np.zeros((Constants.n, 1)) # Necessary resources
R = np.zeros((Constants.n, 1))
fovea = Feature(0, 0)
for step in range (50):
    print step
    #showInitialPredictors(A, img, (100, 255, 255))
    RP = []

    #RP selection
    # setting fovea at random position
    fovea = features[random.randint(0, len(features)-1)]
    for i in range(Constants.n):
        if A[i,0] == 1:
            # if F_src belongs to fovea area view
            if isPointInRect((predictors[i].F_src.x, predictors[i].F_src.y), (fovea.x, fovea.y), Constants.foveaArea):
                sCurrent = predictors[i].S
                for j in features:
                    # ...and if saccade of this predictor lead to some feature
                    if (isPointInRect((sCurrent.x + fovea.x, sCurrent.y+fovea.y), (j.x, j.y), Constants.foveaArea) == True):
                        RP.append(i)
    #showRP(RP, img, (255, 0, 0))

    while len (RP)!=0:

        #best saccade choice
        sUsage = [0 for i in predictors] # list of saccade voting numbers
        for i in RP:
            sCurrent = predictors[i].S
            for j in RP:
                # if distance between Saccade less then some constant means that they lead to the same point
                if (distance(sCurrent, predictors[j].S) < Constants.saccadeEps):
                    sUsage[i] = sUsage[i] + 1
        S_best = np.argmax(sUsage)
        fovea.x = fovea.x + predictors[S_best].S.x
        fovea.y = fovea.y + predictors[S_best].S.y
        # showSaccade(fovea, S_best, img)
        # selection of successful predictors
        A_[:] = A[:]
        SP = []

        #SP selection
        usedPredictors = [] # list of checked predictors
        for j in RP:
            # if current saccade is S_best
            if distance(predictors[S_best].S, predictors[j].S) < Constants.saccadeEps:
            # if target area is within fovea view
                if (isPointInRect((predictors[j].F_tgt.x, predictors[j].F_tgt.y), (fovea.x, fovea.y), Constants.foveaArea)):
                    #showSaccade(fovea, S_best, img)
                    SP.append(j)
                    activateSameAttractorPredictors(j, A)
                else:
                    A_[j,0] = -1
                usedPredictors.append(j)
        for i in usedPredictors:
            RP.remove(i)
        #returning fovea to test other relevant predictors
        fovea.x = fovea.x-predictors[S_best].S.x
        fovea.y = fovea.y-predictors[S_best].S.y
#
#
    # update network
    # equation 7
    R = getR(A_, J)
    updateA(A, R, NR)
    #showUpdatedVectorA(A, img, (255, 255, 0))
    percentages = getSimilarityPercentage(A, A_mu)
    print percentages
    if getWinner(percentages) != -1:
        break
