#Write a python function for the following declarations:
#Note: the location tuple contains: 
#(x-coordinate, y-coordinate, orientation)
#Note: orientation is N,S,E,W

import re

class Robot:
    def __init__(self, sLocation):
        #finish the constructor
        #Define locationX, locationY, orientation
        #using the given value
        print(sLocation)

    def moveForward(self,sLocation,distance):
        # finish the moveForward definition
        #accepts the tuple of location and distance
        #returns a tuple of the new location
        #The coordinate modified (x or y) is dependent
        #upon the orientation

        if sLocation[2] == 'N':
            newLocation = (sLocation[0],sLocation[1]+distance,sLocation[2])
        elif sLocation[2] == 'E':
            newLocation = (sLocation[0]+distance,sLocation[1],sLocation[2])
        elif sLocation[2] == 'W':
            newLocation = (sLocation[0]-distance,sLocation[1],sLocation[2])
        elif sLocation[2] == 'S':
            newLocation = (sLocation[0],sLocation[1]-distance,sLocation[2])

        return newLocation
    
    def rotate(self,sLocation, orientation):
        #finish the rotate definition
        #accepts the tuple of location and the 
        #new orientation
        #returns the tuple of the new loaction and
        #orientation
        newLocation = (sLocation[0],sLocation[1],orientation)

        return newLocation    