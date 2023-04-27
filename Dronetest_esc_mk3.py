
import pigpio
from time import sleep
import os
import sys
import time
import numpy as np
import smbus
from imusensor.MPU9250 import MPU9250

# ?Ñº?Ñú?ùò I2C?Üµ?ã† ?è¨?ä∏ Ïß??†ï
address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()

pi = pigpio.pi()

# Î™®ÌÑ∞ ???Î≤àÌò∏ ?Ñ†?ñ∏ Î≥??ÜçÍ∏? ?û•Ï∞©ÌõÑ Î≥?Í≤ΩÎê† ?òà?†ï
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



class param:              # ?ó¨Í∏∞Ïóê ?òÑ?û¨ Í∞??Üç?èÑ ?†ïÎ≥? ????û• Î∞? Î™®ÌÑ∞?ùò Ï∂úÎ†• Í≥ÑÏÇ∞ ?õÑ ????û• (?èêÎ£®ÌîÑ?óê?Ñú?ùò ?îº?ìúÎ∞±Ïóê ?ï¥?ãπ)
    pos0 = np.zeros((3,1)) #
    pos1 = np.zeros((3,1)) #stable pos
    pos2 = np.zeros((3,1)) #
    
    #?†ïÏß? ÎπÑÌñâ?ãú ?ïà?†ï?ôî ?êò?äî Î™®ÌÑ∞ Ï∂úÎ†•
    posmotRFA = 100
    posmotLFA = 100
    posmotLBA = 100
    posmotRBA = 100

    
    
    


imu.readSensor()   ## Í∞??Üç?èÑÍ≥? ?Ñº?Ñú Í∞? ?ùΩ?ñ¥?ò§Í∏?
imu.computeOrientation()

print ("Accel x: {0} ; Accel y : {1} ; Accel z : {2}".format(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2]))   


"""
<Î™®ÌÑ∞?ùò ?úÑÏπ?>
LFA           RFA


LBA           RBA

?òà: RFA + ?ò§Î•∏Ï™Ω ?ïû Î™®ÌÑ∞ Ï∂úÎ†• ?ÉÅ?äπ, Í∞? Í∞??Üç?èÑÍ∞íÏù¥ 0?ùº Í≤ΩÏö∞ ?ôÑ?†Ñ?ïú ?àò?èâ ?ú†Ïß? ?ÉÅ?Éú

?ôº X-(Í∞??Üç?èÑÍ∞?)  LFA + LBA + RFA - RBA -
?ò§ X+(Í∞??Üç?èÑÍ∞?)  RFA + RBA + LFA - LBA -
?ïû Y-(Í∞??Üç?èÑÍ∞?)  RFA + LFA + RBA - RFA -
?í§ Y+(Í∞??Üç?èÑÍ∞?)  RBA + LBA + RFA - LFA -




ipos Í∞? [0] = xÏ¢åÌëú [1] = yÏ¢åÌëú  [2] = zÏ¢åÌëú ([2]Í∞íÏ?? ?Ç¨?ö©?ïòÏß? ?ïä?ùå)
Ïß?Î©¥ÏúºÎ°úÎ???Ñ∞?ùò ?Üí?ù¥ ==> Í∞??Üç?èÑÍ≥ÑÏùò yaw Í∞? Ï∞∏Í≥† (?ïÑÏß? Íµ¨ÌòÑ x)

"""
## ?†ïÏß? ÎπÑÌñâ?ãú ?ô∏?†•?ù¥ Î∞úÏÉù?êòÎ©? ?ä§?ä§Î°? ?ûê?Ñ∏ ?†ú?ñ¥Î•? ?ïò?äî ?ï®?àò

def iRFA(iposx,iposy,iposz,imotorRFA):
    if iposx > +1.5:      ## Í∞??Üç?èÑÍ≥ÑÏùò xÍ∞íÏù¥ ?ïà?†ï?êú ?ÉÅ?Éú?ùº?ïåÎ≥¥Îã§ 1.5(????ñ¥Ïß? ?†ï?èÑ) ?çî ????ñ¥Ïß? Í≤ΩÏö∞ Îπ†Î•¥Í≤? ?ûê?Ñ∏ÍµêÏ†ï
        imotorRFA += 10
        
        
    elif iposy < -1.5:    
        imotorRFA += 10
        
            
    elif iposx <= 1.5 and iposx > 0 :      ## ?ù¥?†Ñ ÏΩîÎìúÎ≥¥Îã§ ?çî ?ûê?Ñ∏?ûà Î™®ÌÑ∞ Ï∂úÎ†• Ï°∞Ï†ï?ùÑ ?úÑ?ï¥ Ï°∞Í∏à?î©Îß? Ï°∞Ï†ï
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
       


# ?ìúÎ°? Íµ¨Îèô
def startmotor(val):
    
    if val == "start":
        #?ìúÎ°? Íµ¨Îèô?õÑ ?†ïÏß?ÎπÑÌñâ ?ñ•?õÑ ?ó¨Í∏∞Ïóê ?äπ?†ï ?ã†?ò∏ ?ûÖ?†•?ãú ?ó¨?ü¨Î∞©Ìñ•?úºÎ°? ???ÏßÅÏù¥Í≤åÎÅî Ï∂îÍ?? ?òà?†ï
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
                
                # Ï¥àÍ∏∞ ÎπÑÌñâ?ãú ?ïà?†ï?†Å?úºÎ°? ?†ïÏß?ÎπÑÌñâ?ù¥ ?ïà?êòÍ≥? ?ûà?ùÑ?ãú Íµ¨Îèô?êò?äî ÏΩîÎìú (?†ïÏß?ÎπÑÌñâ ?ûê?Ñ∏?†ú?ñ¥ Î™®Îìà)
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
                        
                        
                        
                        
                        # Í∞? Î™®ÌÑ∞Î≥? ?ï®?àò?óê?Ñú Î∞òÌôò?êú Î™®ÌÑ∞ Ï∂úÎ†•?ùÑ ?ù¥?ö©?ïò?ó¨ ?ã§?†úÎ°? Í∑? Ï∂úÎ†•?ùÑ Î™®ÌÑ∞Î°? ?ã†?ò∏Î≥¥ÎÉÑ
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
                
                # ?†ïÏß?ÎπÑÌñâ ?ïà?†ï?ôî ?ãú ?ï¥?ãπ Ï∂úÎ†•?úºÎ°? ?ÉÅÍ≥µÏóê?Ñú ?†ïÏß?
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
                        
                        

                        print("stable")
                        print(motorRFA)
                        print(motorLFA)
                        print(motorRBA)
                        print(motorLBA)
                    



        # Í∏¥Í∏â ?†ïÏß? (?Ç§Î≥¥Îìú?óê ?ûÖ?†•?ù¥ ?ûà?ùÑ ?ãú)

        try 
        
        
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
startmotor(val)   ## ?ûê?ú®Ï£ºÌñâ Î™®ÎìàÎ°? Î∂??Ñ∞ ?ãú?ûë ?ã†?ò∏Î•? Î∞õÏúºÎ©? ?ãú?ûë
 
 
  



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







