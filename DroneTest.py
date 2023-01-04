import pigpio
from time import sleep
import os
import sys
import time
import numpy as np
import smbus
from imusensor.MPU9250 import MPU9250

address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()

pi = pigpio.pi()


RBA = 13  
RBB = 19
RFA = 20  
RFB = 21  
LFA = 17 
LFB = 27
LBA = 6 
LBB = 5

pi.set_mode(RBA, pigpio.OUTPUT)
pi.set_mode(RBB, pigpio.OUTPUT)
pi.set_mode(RFA, pigpio.OUTPUT)
pi.set_mode(RFB, pigpio.OUTPUT)
pi.set_mode(LFA, pigpio.OUTPUT)
pi.set_mode(LFB, pigpio.OUTPUT)
pi.set_mode(LBA, pigpio.OUTPUT)
pi.set_mode(LBB, pigpio.OUTPUT)



class param:
    pos0 = np.zeros((3,1))
    pos1 = np.zeros((3,1))
    pos2 = np.zeros((3,1))
    
    
    


imu.readSensor()
imu.computeOrientation()
param.pos1[0] = imu.AccelVals[0]
param.pos1[1] = imu.AccelVals[1]
param.pos1[2] = imu.AccelVals[2]

print ("Accel x: {0} ; Accel y : {1} ; Accel z : {2}".format(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2]))   


def iRFA(iposx,iposy,iposz):
    if iposx < param.pos1[0]-2.5:      ## FAST X Y Z
        imotorRFA = 210
        return imotorRFA
    elif iposy > param.pos1[1]+2.5:    
        imotorRFA = 210
        return imotorRFA    
    elif iposx >= param.pos1[0]-2.5:      ## X Y Z SMOOTH
        if iposx >= param.pos1[0]-1:
            imotorRFA = 201
        else:
            imotorRFA = 205
        return imotorRFA
    elif iposy <= param.pos1[1]+2.5:    
        
        if iposy <= param.pos1[1]+1:    
            imotorRFA = 201
        
        else:
            imotorRFA = 205                 ## 210 to 200  210-count    count value count++ if count =9  
        return imotorRFA    

def iRBA(iposx,iposy,iposz):
    if iposx < param.pos1[0]-2.5:      ## FAST X Y Z
        imotorRBA = 210
        return imotorRBA
    elif iposy < param.pos1[1]-2.5:
        imotorRBA = 210
        return imotorRBA   
    elif iposx >= param.pos1[0]-2.5:      ## X Y Z SMOOTH
        if iposx >= param.pos1[0]-1:
            imotorRBA = 201
        else:
            imotorRBA = 205
        return imotorRBA   
    elif iposy >= param.pos1[1]-2.5:
        if iposy >= param.pos1[1]-1:
            imotorRBA = 201
        
        else:
            imotorRBA = 205
        return imotorRBA  

def iLFA(iposx,iposy,iposz):
    if iposx > param.pos1[0]+2.5:
        imotorLFA = 210
        return imotorLFA
    elif iposy > param.pos1[1]+2.5:    
        imotorLFA = 210
        return imotorLFA   
    elif iposx >= param.pos1[0]+2.5:
        if iposx >= param.pos1[0]+1:
            imotorLFA = 201
        
        else:
            imotorLFA = 205
        return imotorLFA
    elif iposy <= param.pos1[1]+2.5:    
        
        if iposy <= param.pos1[1]+1:    
            imotorLFA = 201
        
        else:
            imotorLFA = 205
        return imotorLFA    


def iLBA(iposx,iposy,iposz):
    if iposx > param.pos1[0]+2.5:
        imotorLBA = 210
        return imotorLBA
    elif iposy < param.pos1[1]-2.5:
        imotorLBA = 210
        return imotorLBA   
    elif iposx >= param.pos1[0]+2.5:
        if iposx >= param.pos1[0]+1:
            imotorLBA = 201
        
        else:
            imotorLBA = 205
        return imotorLBA 
    elif iposy >= param.pos1[1]-2.5:
        if iposy >= param.pos1[1]-1:
            imotorLBA = 201
        
        else:
            imotorLBA = 205
        return imotorLBA        



def startmotor(val):
    
    if val == "start":
        motorRFA = 200
        motorRBA = 200
        motorLFA = 200
        motorLBA = 200

        pi.set_PWM_dutycycle(RFA, motorRFA)
        pi.set_PWM_dutycycle(RFB, 0)
        pi.set_PWM_dutycycle(LFA, motorLFA)
        pi.set_PWM_dutycycle(LFB, 0)
        pi.set_PWM_dutycycle(RBA, motorRBA)
        pi.set_PWM_dutycycle(RBB, 0)
        pi.set_PWM_dutycycle(LBA, motorLBA)
        pi.set_PWM_dutycycle(LBB, 0)
        time.sleep(4) 
        try:
            while True:
                imu.readSensor()
                imu.computeOrientation()
                time.sleep(0.1)
                
                param.pos2[0] = imu.AccelVals[0]
                param.pos2[1] = imu.AccelVals[1]
                param.pos2[2] = imu.AccelVals[2]
                print("pos2: ",param.pos2)
                print ("Accel x: {0} ; Accel y : {1} ; Accel z : {2}".format(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2]))
                
            
                if abs(param.pos2[0]) >= abs(param.pos1[0])+0.1 or abs(param.pos2[1]) >= abs(param.pos1[1])+0.1 or param.pos2[2] >= abs(param.pos1[2]):

                    while abs(param.pos2[0]) >= abs(param.pos1[0])+0.1 or abs(param.pos2[1]) >= abs(param.pos1[1])+0.1 or abs(param.pos2[2]) >= abs(param.pos1[2])+0.1:
                        imu.readSensor()
                        imu.computeOrientation()
                        param.pos2[0] = imu.AccelVals[0]
                        param.pos2[1] = imu.AccelVals[1]
                        param.pos2[2] = imu.AccelVals[2]

                        print("while pos2: ",param.pos2)
                        
                        
                        
                        
                        
                        pi.set_PWM_dutycycle(RFA, iRFA(param.pos2[0],param.pos2[1],param.pos2[2]))
                        pi.set_PWM_dutycycle(RFB, 0)
                        pi.set_PWM_dutycycle(LFA, iLFA(param.pos2[0],param.pos2[1],param.pos2[2]))
                        pi.set_PWM_dutycycle(LFB, 0)
                        pi.set_PWM_dutycycle(RBA, iRBA(param.pos2[0],param.pos2[1],param.pos2[2]))
                        pi.set_PWM_dutycycle(RBB, 0)
                        pi.set_PWM_dutycycle(LBA, iLBA(param.pos2[0],param.pos2[1],param.pos2[2]))
                        pi.set_PWM_dutycycle(LBB, 0)

                        print(iRFA(param.pos2[0],param.pos2[1],param.pos2[2]))
                        print(iLFA(param.pos2[0],param.pos2[1],param.pos2[2]))
                        print(iRBA(param.pos2[0],param.pos2[1],param.pos2[2]))
                        print(iLBA(param.pos2[0],param.pos2[1],param.pos2[2]))
                 
                       
                 
                 
                        time.sleep(0.1)
                        '''idle(param.pos2[0],param.pos2[1],param.pos2[2])'''

                else:
                    
            
                    pi.set_PWM_dutycycle(RFA, motorRFA)
                    pi.set_PWM_dutycycle(RFB, 0)
                    pi.set_PWM_dutycycle(LFA, motorLFA)
                    pi.set_PWM_dutycycle(LFB, 0)
                    pi.set_PWM_dutycycle(RBA, motorRBA)
                    pi.set_PWM_dutycycle(RBB, 0)
                    pi.set_PWM_dutycycle(LBA, motorLBA)
                    pi.set_PWM_dutycycle(LBB, 0)
                    time.sleep(0.1)
                    

                    print("else")
                    print(motorRFA)
                    print(motorLFA)
                    print(motorRBA)
                    print(motorLBA)




        except KeyboardInterrupt:
            pi.set_PWM_dutycycle(RFA, 0)
            pi.set_PWM_dutycycle(RFB, 0)
            pi.set_PWM_dutycycle(LFA, 0)
            pi.set_PWM_dutycycle(LFB, 0)
            pi.set_PWM_dutycycle(RBA, 0)
            pi.set_PWM_dutycycle(RBB, 0)
            pi.set_PWM_dutycycle(LBA, 0)
            pi.set_PWM_dutycycle(LBB, 0) 
           



   
   
val=input()
startmotor(val)  
 
 
  



try:
    while True:
        sleep(1)

except KeyboardInterrupt:
   pi.set_PWM_dutycycle(RFA, 0)
   pi.set_PWM_dutycycle(LFA, 0)
   pi.set_PWM_dutycycle(RBA, 0)
   pi.set_PWM_dutycycle(LBA, 0)

print ("Accel x: {0} ; Accel y : {1} ; Accel z : {2}".format(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2]))  ## use this

time.sleep(0.1)







