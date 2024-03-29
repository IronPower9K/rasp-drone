
import pigpio
from time import sleep
import os
import sys
import time
import numpy as np
import smbus
from imusensor.MPU9250 import MPU9250
form pynput import keyboard

# ?Ό?? I2C?΅?  ?¬?Έ μ§?? 
address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()

pi = pigpio.pi()

# λͺ¨ν° ???λ²νΈ ? ?Έ λ³??κΈ? ?₯μ°©ν λ³?κ²½λ  ?? 
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



class param:              # ?¬κΈ°μ ??¬ κ°??? ? λ³? ????₯ λ°? λͺ¨ν°? μΆλ ₯ κ³μ° ? ????₯ (?λ£¨ν??? ?Ό?λ°±μ ?΄?Ή)
    pos0 = np.zeros((3,1)) #
    pos1 = np.zeros((3,1)) #stable pos
    pos2 = np.zeros((3,1)) #
    
    #? μ§? λΉν? ?? ? ?? λͺ¨ν° μΆλ ₯
    posmotRFA = 100
    posmotLFA = 100
    posmotLBA = 100
    posmotRBA = 100

    
    
    


imu.readSensor()   ## κ°???κ³? ?Ό? κ°? ?½?΄?€κΈ?
imu.computeOrientation()

print ("Accel x: {0} ; Accel y : {1} ; Accel z : {2}".format(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2]))   


"""
<λͺ¨ν°? ?μΉ?>
LFA           RFA


LBA           RBA

?: RFA + ?€λ₯Έμͺ½ ? λͺ¨ν° μΆλ ₯ ??Ή, κ°? κ°???κ°μ΄ 0?Ό κ²½μ° ?? ? ?? ? μ§? ??

?Ό X-(κ°???κ°?)  LFA + LBA + RFA - RBA -
?€ X+(κ°???κ°?)  RFA + RBA + LFA - LBA -
? Y-(κ°???κ°?)  RFA + LFA + RBA - RFA -
?€ Y+(κ°???κ°?)  RBA + LBA + RFA - LFA -




ipos κ°? [0] = xμ’ν [1] = yμ’ν  [2] = zμ’ν ([2]κ°μ?? ?¬?©?μ§? ??)
μ§?λ©΄μΌλ‘λ???°? ??΄ ==> κ°???κ³μ yaw κ°? μ°Έκ³  (?μ§? κ΅¬ν x)

"""
## ? μ§? λΉν? ?Έ? ₯?΄ λ°μ?λ©? ?€?€λ‘? ??Έ ? ?΄λ₯? ?? ?¨?

def iRFA(iposx,iposy,iposz,imotorRFA):
    if iposx > +1.5:      ## κ°???κ³μ xκ°μ΄ ?? ? ???Ό?λ³΄λ€ 1.5(????΄μ§? ? ?) ? ????΄μ§? κ²½μ° λΉ λ₯΄κ²? ??Έκ΅μ 
        imotorRFA += 10
        
        
    elif iposy < -1.5:    
        imotorRFA += 10
        
            
    elif iposx <= 1.5 and iposx > 0 :      ## ?΄?  μ½λλ³΄λ€ ? ??Έ? λͺ¨ν° μΆλ ₯ μ‘°μ ? ??΄ μ‘°κΈ?©λ§? μ‘°μ 
        if iposx <= 0.8:
            imotorRFA += 1
        else:
            imotorRFA += 5
        
        
    elif iposy >= -1.5 and iposy < 0:    
        
        if iposy >= -0.8:    
            imotorRFA += 1
        
        else:
            imotorRFA += 5        
        
        
    
    elif iposx < -1.5:      
        imotorRFA -= 10
        
        
    elif iposy > +1.5:   
        imotorRFA -= 10
        
            
    elif iposx >= -1.5 and iposx < 0 :      
        if iposx >= -0.8:
            imotorRFA -= 1
        else:
            imotorRFA -= 5
        
        
    elif iposy <= +1.5 and iposy > 0:    
        
        if iposy <= +0.8:    
            imotorRFA -= 1
        
        else:
            imotorRFA -= 5                 
        
    
    if imotorRFA > 10 and imotorRFA <=245:
        param.posmotRFA = imotorRFA
    return imotorRFA    
    



def iRBA(iposx,iposy,iposz,imotorRBA):
    if iposx > 1.5:      ## FAST X Y Z
        imotorRBA += 10
        
        
    elif iposy > 1.5:
        imotorRBA += 10
           
    elif iposx <= 1.5 and iposx > 0 :      ## X Y Z smooth
        if iposx <= 0.8:
            imotorRBA += 1
        else:
            imotorRBA += 5
           
    elif iposy <= 1.5 and iposy > 0:
        if iposy <= 0.8:
            imotorRBA += 1
        
        else:
            imotorRBA += 5
          
    elif iposx < -1.5:      ## FAST X Y Z
        imotorRBA -= 10
        
    
    elif iposy < -1.5:
        imotorRBA -= 10
           
    elif iposx >= -1.5 and iposx < 0 :      ## X Y Z smooth
        if iposx >= -0.8:
            imotorRBA -= 1
        else:
            imotorRBA -= 5
        
       
    elif iposy >= -1.5 and iposy < 0:
        if iposy >= -0.8:
            imotorRBA -= 1
        
        else:
            imotorRBA -= 5
        
    if imotorRBA > 10 and imotorRBA <=245:
        param.posmotRBA = imotorRBA
    return imotorRBA  
    

def iLFA(iposx,iposy,iposz,imotorLFA):
    if iposx < -1.5:
        imotorLFA += 10
        
        
    elif iposy < -1.5:    
        imotorLFA += 10
           
    elif iposx >= -1.5 and iposx < 0 :
        if iposx >= -0.8:
            imotorLFA += 1
        
        else:
            imotorLFA += 5
        
        
    elif iposy >= -1.5 and iposy < 0:    
        
        if iposy >= -0.8:    
            imotorLFA += 1
        
        else:
            imotorLFA += 5
        
    
    elif iposx > 1.5:
        imotorLFA -= 10
        
        
    elif iposy > 1.5:    
        imotorLFA -= 10
        
           
    elif iposx <= 1.5 and iposx > 0 :
        if iposx <= 0.8:
            imotorLFA -= 1
        
        else:
            imotorLFA -= 5
        
        
    elif iposy <= 1.5 and iposy > 0:    
        
        if iposy <= 0.8:    
            imotorLFA -= 1
        
        else:
            imotorLFA -= 5
    if imotorLFA > 10 and imotorLFA <= 245:
        param.posmotLFA = imotorLFA
    return imotorLFA    
    


def iLBA(iposx,iposy,iposz,imotorLBA):
    if iposx < -1.5:
        imotorLBA += 10
        
        
    elif iposy > 1.5:
        imotorLBA += 10
        
           
    elif iposx >= -1.5 and iposx < 0 :
        if iposx >= -0.8:
            imotorLBA += 1
        
        else:
            imotorLBA += 5
        
         
    elif iposy <= 1.5 and iposy > 0:
        if iposy <= 0.8:
            imotorLBA += 1
        
        else:
            imotorLBA += 5
        
             
    
    
    elif iposx > 1.5:
        imotorLBA -= 10
        
        
    elif iposy < -1.5:
        imotorLBA -= 10
        
        
    elif iposx <= 1.5 and iposx > 0:
        if iposx <= 0.8:
            imotorLBA -= 1
        
        else:
            imotorLBA -= 5
        
        
    elif iposy >= -1.5 and iposy < 0:
        if iposy >= -0.8:
            imotorLBA -= 1
        
        else:
            imotorLBA -= 5
    if imotorLBA > 10 and imotorLBA <= 245:
        param.posmotLBA = imotorLBA
    return imotorLBA      
       


# ?λ‘? κ΅¬λ
def startmotor(val):
    
    if val == "start":
        #?λ‘? κ΅¬λ? ? μ§?λΉν ?₯? ?¬κΈ°μ ?Ή?  ? ?Έ ?? ₯? ?¬?¬λ°©ν₯?Όλ‘? ???μ§μ΄κ²λ μΆκ?? ?? 
        try:
            while True:
                imu.readSensor()
                imu.computeOrientation()
                time.sleep(0.1)
                
                motorRFA = param.posmotRFA
                motorLFA = param.posmotLFA
                motorRBA = param.posmotRBA
                motorLBA = param.posmotLBA

                param.pos2[0] = imu.AccelVals[0]
                param.pos2[1] = imu.AccelVals[1]
                param.pos2[2] = imu.AccelVals[2]
                print("pos2: ",param.pos2)
                print ("Accel x: {0} ; Accel y : {1} ; Accel z : {2}".format(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2]))
                
                # μ΄κΈ° λΉν? ?? ? ?Όλ‘? ? μ§?λΉν?΄ ??κ³? ??? κ΅¬λ?? μ½λ (? μ§?λΉν ??Έ? ?΄ λͺ¨λ)
                if abs(param.pos2[0]) >= abs(0)+0.3 or abs(param.pos2[1]) >= abs(0)+0.3 or param.pos2[2] >= abs(0):

                    while abs(param.pos2[0]) >= abs(0)+0.1 or abs(param.pos2[1]) >= abs(0)+0.1 or abs(param.pos2[2]) >= abs(0)+0.1:
                        imu.readSensor()
                        imu.computeOrientation()
                        param.pos2[0] = imu.AccelVals[0]
                        param.pos2[1] = imu.AccelVals[1]
                        param.pos2[2] = imu.AccelVals[2]

                        motorRFA = param.posmotRFA
                        motorLFA = param.posmotLFA
                        motorRBA = param.posmotRBA
                        motorLBA = param.posmotLBA

                        print("while pos2: ",param.pos2)
                        
                        
                        
                        
                        # κ°? λͺ¨ν°λ³? ?¨??? λ°ν? λͺ¨ν° μΆλ ₯? ?΄?©??¬ ?€? λ‘? κ·? μΆλ ₯? λͺ¨ν°λ‘? ? ?Έλ³΄λ
                        """pi.set_PWM_dutycycle(RFA, iRFA(param.pos2[0],param.pos2[1],param.pos2[2]))
                        pi.set_PWM_dutycycle(RFB, 0)
                        pi.set_PWM_dutycycle(LFA, iLFA(param.pos2[0],param.pos2[1],param.pos2[2]))
                        pi.set_PWM_dutycycle(LFB, 0)
                        pi.set_PWM_dutycycle(RBA, iRBA(param.pos2[0],param.pos2[1],param.pos2[2]))
                        pi.set_PWM_dutycycle(RBB, 0)
                        pi.set_PWM_dutycycle(LBA, iLBA(param.pos2[0],param.pos2[1],param.pos2[2]))
                        pi.set_PWM_dutycycle(LBB, 0)"""

                        print(iLFA(param.pos2[0],param.pos2[1],param.pos2[2],motorLFA),"     ",iRFA(param.pos2[0],param.pos2[1],param.pos2[2],motorRFA))
                        print(iLBA(param.pos2[0],param.pos2[1],param.pos2[2],motorLBA),"     ",iRBA(param.pos2[0],param.pos2[1],param.pos2[2],motorRBA))
                 
                        

                 
                        time.sleep(1)
                        '''idle(param.pos2[0],param.pos2[1],param.pos2[2])'''
                
                # ? μ§?λΉν ?? ? ? ?΄?Ή μΆλ ₯?Όλ‘? ?κ³΅μ? ? μ§?
                else:
                    
                    while True:
                        
                        pi.set_PWM_dutycycle(RFA, motorRFA)
                        pi.set_PWM_dutycycle(RFB, 0)
                        pi.set_PWM_dutycycle(LFA, motorLFA)
                        pi.set_PWM_dutycycle(LFB, 0)
                        pi.set_PWM_dutycycle(RBA, motorRBA)
                        pi.set_PWM_dutycycle(RBB, 0)
                        pi.set_PWM_dutycycle(LBA, motorLBA)
                        pi.set_PWM_dutycycle(LBB, 0)
                        time.sleep(0.1)
                            
                            

                        print("stable")
                        print(motorRFA)
                        print(motorLFA)
                        print(motorRBA)
                        print(motorLBA)
                        if keyboard.read_key() == "w":
                            while 
                        
                         



        # κΈ΄κΈ ? μ§? (?€λ³΄λ? ?? ₯?΄ ?? ?)

        
        
        
        except KeyboardInterrupt:
            pi.set_PWM_dutycycle(RFA, 0)
            pi.set_PWM_dutycycle(RFB, 0)
            pi.set_PWM_dutycycle(LFA, 0)
            pi.set_PWM_dutycycle(LFB, 0)
            pi.set_PWM_dutycycle(RBA, 0)
            pi.set_PWM_dutycycle(RBB, 0)
            pi.set_PWM_dutycycle(LBA, 0)
            pi.set_PWM_dutycycle(LBB, 0) 
           



   
   
val=input("Start Drone?")
startmotor(val)   ## ??¨μ£Όν λͺ¨λλ‘? λΆ??° ?? ? ?Έλ₯? λ°μΌλ©? ??
 
 
  



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







