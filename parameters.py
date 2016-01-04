# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 19:52:29 2015

@author: lvanhulle
"""
import math
import numpy as np
from operator import itemgetter
#import handleParameters

"""
Printing Parameters.
"""
fullExtrusionRate = 0.7 #fill for grips
extrusionRate = [0.0212]#, 0.1, 0.05] #mm of filament/mm of travel
pathWidth = 0.5 #mm distance between centerline of paths
printSpeed = [2000] #mm/min head travel speed
shiftX = [20]#, 70]
shiftY = [0]#, 20, 40, 60, 80]

"""
Part Parameters
"""
#mainShape = ps.wideDogBone
layerHeight = [0.3] #mm height per layer
numLayers = [2] #number of layers to make
infillAngleDegrees = 90 #degrees infill angle 90 is in Y direction 0 is in X direction

"""
File Parameters
"""
outputFileName = 'DB_10-23_Test.gcode' #the name of the file you want output. git will ignore all .gcode unless they start with SAVE
start_Gcode_FileName = 'Start_Gcode_Taz5.txt' #the file name for the starting gcode
end_Gcode_FileName = 'End_Gcode_Taz5.txt' #The file name for the end gcode
outputSubDirectory = 'Gcode'
startEndSubDirectory = 'Start_End_Gcode'

"""
Misc Parameters
"""
maxFeedStep = 5.0 #not implemented yet
slopeOverX = 0.0 #not yet implemented how much you want it to move over in X per level
slopeOverY = 0 #not implemented yet how much you want it to move over in Y per level
backgroundAngle = (infillAngleDegrees/360.0*2*math.pi) #angle of the paths in the layer 0 = X direction, PI/2 = Y direction
solidityRatio = None #get calculation from Karsten

def zipVariables_gen(inputLists):
    variableGenorators = []
    for sublist in inputLists:
        variableGenorators.append(variable_gen(sublist))
        
    for _ in max(inputLists, key=len):
        tempList = []
        for varGen in variableGenorators:
            tempList.append(next(varGen))
        yield tempList
    
def variable_gen(variableList):
    while True:
        for var in variableList: 
            yield var
            
everyPartsParameters = zipVariables_gen((
                          extrusionRate, printSpeed, shiftX, shiftY,
                          layerHeight, numLayers
                          ))
                                                   

"""
Standard printing settings
"""
OMIT_Z = True
INCLUDE_Z = False
RAPID = 8000 #mm/min
TRAVERSE_RETRACT = 0.5 #mm to retract when traversing longer distances
MAX_EXTRUDE_SPEED = 100 #mm/min max speed to move filament
Z_CLEARANCE = 10.0 #mm to move Z up
APPROACH_FR = 2000 #mm/min aproach feedrate


def nearestLine_Coro(inGroupM, key=None):
    inGroup = [line.deepCopy() for line in inGroupM]
    used, testPoint = yield
    normList = []
    for line in inGroup:
        normList.append(line.start.normalVector)
        normList.append(line.end.normalVector)
    normList = np.array(normList)
    while len(inGroup) > 0:
        """
        This got a little complicated but sped up this section by about 10X
        This next line inside out does as follows:
        1) take the normList and subtract the normVector from the test point
            This actually subtracts the testPointNormVector from each individual
            element in the normList
        2) Use numpy.linalg.norm to get the length of each element. The first
            object is our subtracted array, None is for something I don't understand
            1 is so that it takes the norm of each element and not of the whole
            array
        3) enumerate over the array of norms so we can later have the index
        4) enumerate is a generator, so we are using a for comprehension to
            send the tuple (index, dist) to the min function. The norm stored
            in each element of the array is the distance from the testPoint to
            the point which was at that index
        5) Find the min of the tuples (index, dist) key-itemgetter(1) is telling min
            to look at dist when comparing the tuples
        6) min returns the lowest tuple, which we split into index and dist
        """
        index, dist = min(((index, dist) for index, dist in
            enumerate(np.linalg.norm(normList-testPoint.normalVector, None, 1))),
            key=itemgetter(1))
        if index%2: #If index is odd we are at the end of a line so the line needs to be flipped
            inGroup[index/2].flip()

        used, testPoint = yield inGroup[index/2], key, dist
        if not used and index%2:
            inGroup[index/2].flip()
        if used:
            index /= 2
            inGroup.pop(index)
            normList = np.delete(normList, [index*2, index*2+1],0)

"""
Constants
"""
class constants:
    ARC_NUMPOINTS = 20
    CW = -1 #Circle direction clock wise
    CCW = 1 #circle direction counter clowise
    X, Y, Z = 0, 1, 2
    START = 0 #start of circle
    END = 1 #end of circle
    DIR = 2 #direction to travel
    CENTER = 3 #center of circle
    INSIDE = 1 #Point is inside shape
    OUTSIDE = 0 #point is outside shape
    ALLOW_PROJECTION = True
    EXTRUSION_RATE = 0
    PRINT_SPEED = 1
    SHIFT_X = 2
    SHIFT_Y = 3
    LAYER_HEIGHT = 4
    NUM_LAYERS = 5
