#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 19:18:02 2018

@author: gershow
"""
import numpy as np
import matplotlib.pyplot as plt
import math

tank1Color = 'b'
tank2Color = 'r'
obstacleColor = 'k'

##### functions provided to you #####
def getNumberInput (prompt, validRange = [-np.Inf, np.Inf]):
    """displays prompt and converts user input to a number
    
       in case of non-numeric input, re-prompts user for numeric input
       
       Parameters
       ----------
           prompt : str
               prompt displayed to user
           validRange : list, optional
               two element list of form [min, max]
               value entered must be in range [min, max] inclusive
        Returns
        -------
            float
                number entered by user
    """
    while True:
        try:
            num = float(input(prompt))
        except Exception:
            print ("Please enter a number")
        else:
            if (num >= validRange[0] and num <= validRange[1]):
                return num
            else:
                print ("Please enter a value in the range [", validRange[0], ",", validRange[1], ")") #Python 3 sytanx
            
    return num    

def showWindow():
    """
    shows the window -- call at end of drawBoard and tankShot
    """
    plt.draw()
    plt.pause(0.001)
    plt.show()


def drawBox(box, color):
    """
    draws a filled box in the current axis
    parameters
    ----------
    box : tuple
        (left,right,bottom,top) - extents of the box
     color : str
        color to fill the box with, e.g. 'b'
    """    
    x = (box[0], box[0], box[1], box[1])
    y = (box[2], box[3], box[3], box[2])
    ax = plt.gca()
    ax.fill(x,y, c = color)



def endTrajectoryAtIntersection (x,y,box):
    """
    portion of trajectory prior to first intersection with box
    
    paramaters
    ----------
    x,y : np array type
        position to check
    box : tuple
        (left,right,bottom,top)
    
    returns
    ----------
    (x,y) : tuple of np.array of floats
        equal to inputs if (x,y) does not intersect box
        otherwise returns the initial portion of the trajectory
        up until the point of intersection with the box
    """
    i = firstInBox(x,y,box)
    if (i < 0):
        return (x,y)
    return (x[0:i],y[0:i])


##### functions you need to implement #####
def trajectory (x0,y0,v,theta,g = 9.8, npts = 1000):
    """
    finds the x-y trajectory of a projectile
    
    parameters
    ----------
    x0 : float 
        initial x - position
    y0 : float
        initial y - position, must be >0
        initial velocity
    theta : float
        initial angle (in degrees)
    g : float (default 9.8)
        acceleration due to gravity
    npts : int
        number of points in the sample
    
    returns
    -------
    (x,y) : tuple of np.array of floats
        trajectory of the projectile vs time
    
    notes
    -----
    trajectory is sampled with npts time points between 0 and 
    the time when the y = 0 (regardless of y0)
    y(t) = y0 + vsin(theta) t - 0.5 g t^2
    0.5g t^2 - vsin(theta) t - y0 = 0
    t_final = v/g sin(theta) + sqrt((v/g)^2 sin^2(theta) + 2 y0/g)
    """
    vy = math.sin(np.deg2rad(theta)) * v
    vx = math.cos(np.deg2rad(theta)) * v
    t_final = vy/g + math.sqrt((vy * vy/(g*g)) + 2*y0/g)
    t = [ (t_final * i) / npts for i in range(npts+1)]
    x = [ x0 + vx * t[i] for i in range(npts+1)]
    y = [ y0 + vy *  t[i] - g * t[i] * t[i] / 2 for i in range(npts+1)]
    return(x,y)    

def firstInBox (x,y,box):
    """ 
    finds first index of x,y inside box
    
    parameters
    ----------
    x,y : np array type
        positions to check
    box : tuple
        (left,right,bottom,top)
    
    returns
    -------
    int
        the lowest j such that
        x[j] is in [left,right] and 
        y[j] is in [bottom,top]
        -1 if the line x,y does not go through the box
    """
    for i in range(len(x)):
        if box[0] <= x[i] and x[i] <= box[1] and box[2] <= y[i] and y[i] <= box[3]:
            return(i)
    return -1

"""(x,y) = trajectory(0,0, 10, 45)
box = (0,10,0,10)
j = firstInBox(x,y, box)
print( j> -1)"""

def tankShot (targetBox, obstacleBox, x0, y0, v, theta, g = 9.8):
    """
    executes one tank shot
    
    parameters
    ----------
    targetBox : tuple
        (left,right,bottom,top) location of the target
    obstacleBox : tuple
        (left,right,bottom,top) location of the central obstacle
    x0,y0 :floats
        origin of the shot
    v : float
        velocity of the shot
    theta : float
        angle of the shot
    g : float 
        accel due to gravity (default 9.8)
    returns
    --------
    int
        code: 0 = miss, 1 = hit
        
    hit if trajectory intersects target box before intersecting
    obstacle box
    draws the truncated trajectory in current plot window
    """
    (x,y) = trajectory(x0, y0, v, theta)
    plt.figure(1)
    (x1,y1) = endTrajectoryAtIntersection (x,y, obstacleBox)
    
    if firstInBox(x, y, obstacleBox) > -1: 
        plt.plot(x1, y1, color = 'k')
        return 0
    if firstInBox(x, y, targetBox) > -1:
        plt.plot(x, y, color = 'k')
        return 1
    plt.plot(x, y, color = 'k')
    return 0

        
    


def drawBoard (tank1box, tank2box, obstacleBox, playerNum):
    """
    draws the game board, pre-shot
    parameters
    ----------
    tank1box : tuple
        (left,right,bottom,top) location of player1's tank
    tank2box : tuple
        (left,right,bottom,top) location of player1's tank
    obstacleBox : tuple
        (left,right,bottom,top) location of the central obstacle
    playerNum : int
        1 or 2 -- who's turn it is to shoot
 
    """    
    drawBox(obstacleBox, obstacleColor)
    drawBox(tank1box, tank1Color)
    drawBox(tank2box, tank2Color)
    #print("It is player " + str(playerNum) + "'s turn to shoot." )
    #your code here
    
    showWindow() #this makes the figure window show up


def oneTurn (tank1box, tank2box, obstacleBox, playerNum, g = 9.8):   
    """
    parameters
    ----------
    tank1box : tuple
        (left,right,bottom,top) location of player1's tank
    tank2box : tuple
        (left,right,bottom,top) location of player1's tank
    obstacleBox : tuple
        (left,right,bottom,top) location of the central obstacle
    playerNum : int
        1 or 2 -- who's turn it is to shoot
     g : float 
        accel due to gravity (default 9.8)
    returns
    -------
    int
        code 0 = miss, 1 or 2 -- that player won
    
    clears figure
    draws tanks and obstacles as boxes
    prompts player for velocity and angle
    displays trajectory (shot originates from center of tank)
    returns 0 for miss, 1 or 2 for victory
    """
    plt.figure(1)
    plt.clf()
    drawBoard(tank1box, tank2box, obstacleBox, playerNum)
    v = getNumberInput("Please enter your velocity:", [0, np.Inf])
    theta = getNumberInput("Please enter your angle in degrees:", [0,180])
    x0 = 0
    y0 = 0
    hit = 0
    if playerNum == 1:
        x0 = (tank1box[0] + tank1box[1])/2
        y0 = (tank1box[2] + tank1box[3])/2
        hit = tankShot(tank2box, obstacleBox, x0, y0, v, theta)
    else:
        x0 = (tank2box[0] + tank2box[1])/2
        y0 = (tank2box[2] + tank2box[3])/2
        hit = tankShot(tank1box, obstacleBox, x0, y0, v, theta)
        
    if hit == 0:
        return hit
    else:
        return playerNum
    
obstacleBox = (40,60,0,50)
tank1box = (10,15,0,5)
tank2box = (90,95,0,5)
oneTurn (tank1box, tank2box, obstacleBox, 1)
   


def playGame(tank1box, tank2box, obstacleBox, g = 9.8):
    """
    parameters
    ----------
    tank1box : tuple
        (left,right,bottom,top) location of player1's tank
    tank2box : tuple
        (left,right,bottom,top) location of player1's tank
    obstacleBox : tuple
        (left,right,bottom,top) location of the central obstacle
    playerNum : int
        1 or 2 -- who's turn it is to shoot
     g : float 
        accel due to gravity (default 9.8)
    """
    playerNum = 1
    win = False
    while win == False:
        z = oneTurn (tank1box, tank2box, obstacleBox, playerNum)
        if z > 0:
            break
        input("Press Enter to continue:")
        if playerNum == 1:
            playerNum = 2
        else:
            playerNum = 1
    print("Congratulations player " + playerNum + "!")
        
#playGame(tank1box, tank2box, obstacleBox)
        
        
    
        



##### fmain -- edit box locations for new games #####
def main():
    tank1box = [10,15,0,5]
    tank2box = [90,95,0,5]
    obstacleBox = [40,60,0,50]
    playGame(tank1box, tank2box, obstacleBox)
    

#don't edit the lines below;
if __name__== "__main__":
    main()  
        
    