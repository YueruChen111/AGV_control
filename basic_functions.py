from CO_command import *
from numpy import *
import math

# parameter based on model
wheel_distance = 30
posTol = 0.01
NewPos = 0
NewAngle = 0

# v w speed mode
def moveVW(v,w):
    vl=int(v+w*wheel_distance/2)
    vr=int(v-w*wheel_distance/2)
    setSpeed(vl,vr)
    return

# v w soft-start speed mode
def softmoveVW(v,w):
    vl=int(v+w*wheel_distance/2)
    vr=int(v-w*wheel_distance/2)
    softsetSpeed(vl,vr)
    return

# vl vr speed mode
def moveLR(vl,vr):
    setSpeed(vl,vr)
    return

# vl vr soft-start speed mode
def softmoveLR(vl,vr):
    softsetSpeed(vl,vr)
    return

# actual forward position(mm)
def getForwardPos():
    return (getLPos()+getRPos())/2 - NewPos

# actual rotate degree(rad)
def getAngle():
    return (getLPos()-getRPos())/4/wheel_distance - NewAngle

# reset zero position
def resetForwardPos():
    global NewPos 
    NewPos = getForwardPos()
    return

# reset zero degree
def resetAngle():
    global NewAngle 
    NewAngle = getAngle()
    return

# moveVW for t seconds
def timerMove(v,w,t):
    startTime = time.time()
    moveVW(v,w)
    while(1):
        endTime = time.time()
        if endTime == startTime + t:
            break
    lockBase()
    return

# softmoveVW for t seconds
def softStartTimerMove(v,w,t):
    startTime = time.time()
    softmoveVW(v,w)
    while(1):
        endTime = time.time()
        if endTime == startTime + t:
            break
    lockBase()
    return

# position mode move dis(mm) with v rpm
def posMove(v,dis):
    positionMode(leftID,v,dis)
    #positionMode(rightID,v,dis)
    return

# position mode retote angle(rad) with v rpm
def posRotate(v,angle):
    dis = wheel_distance*angle/2
    positionMode(leftID,v,dis)
    positionMode(rightID,v,-dis)
    return

# from (0, 0) to (x_goal, y_goal)
def posMoveTo(v,k,T,x_goal,y_goal):
    x=y=0
    theta=math.pi/2
    while(x-x_goal)**2+(y-y_goal)**2 >posTol**2:
        theta_goal=math.atan((y_goal-y)/(x_goal-x))
        theta_error=theta-theta_goal
        vl=v-k*theta_error
        vr=v+k*theta_error
        moveLR(vl,vr)
        x=x+v*math.cos(theta)*T
        y=y+v*math.sin(theta)*T
        w=(vr-vl)/wheel_distance
        theta=theta+w*T
        time.sleep(T)
        print(y-y_goal)
    lockBase()
    return

