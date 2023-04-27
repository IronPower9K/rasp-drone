
import pigpio
from time import sleep
import os
import sys
import time
import numpy as np
import smbus
from imusensor.MPU9250 import MPU9250

# ?��?��?�� I2C?��?�� ?��?�� �??��
address = 0x68
bus = smbus.SMBus(1)
imu = MPU9250.MPU9250(bus, address)
imu.begin()

pi = pigpio.pi()

# 모터 ???번호 ?��?�� �??���? ?��착후 �?경될 ?��?��
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



class param:              # ?��기에 ?��?�� �??��?�� ?���? ????�� �? 모터?�� 출력 계산 ?�� ????�� (?��루프?��?��?�� ?��?��백에 ?��?��)
    pos0 = np.zeros((3,1)) #
    pos1 = np.zeros((3,1)) #stable pos
    pos2 = np.zeros((3,1)) #
    
    #?���? 비행?�� ?��?��?�� ?��?�� 모터 출력
    posmotRFA = 100
    posmotLFA = 100
    posmotLBA = 100
    posmotRBA = 100

    
    
    


imu.readSensor()   ## �??��?���? ?��?�� �? ?��?��?���?
imu.computeOrientation()

print ("Accel x: {0} ; Accel y : {1} ; Accel z : {2}".format(imu.AccelVals[0], imu.AccelVals[1], imu.AccelVals[2]))   


"""
<모터?�� ?���?>
LFA           RFA


LBA           RBA

?��: RFA + ?��른쪽 ?�� 모터 출력 ?��?��, �? �??��?��값이 0?�� 경우 ?��?��?�� ?��?�� ?���? ?��?��

?�� X-(�??��?���?)  LFA + LBA + RFA - RBA -
?�� X+(�??��?���?)  RFA + RBA + LFA - LBA -
?�� Y-(�??��?���?)  RFA + LFA + RBA - RFA -
?�� Y+(�??��?���?)  RBA + LBA + RFA - LFA -




ipos �? [0] = x좌표 [1] = y좌표  [2] = z좌표 ([2]값�?? ?��?��?���? ?��?��)
�?면으로�???��?�� ?��?�� ==> �??��?��계의 yaw �? 참고 (?���? 구현 x)

"""
## ?���? 비행?�� ?��?��?�� 발생?���? ?��?���? ?��?�� ?��?���? ?��?�� ?��?��

def iRFA(iposx,iposy,iposz,imotorRFA):
    if iposx > +1.5:      ## �??��?��계의 x값이 ?��?��?�� ?��?��?��?��보다 1.5(????���? ?��?��) ?�� ????���? 경우 빠르�? ?��?��교정
        imotorRFA += 10
        
        
    elif iposy < -1.5:    
        imotorRFA += 10
        
            
    elif iposx <= 1.5 and iposx > 0 :      ## ?��?�� 코드보다 ?�� ?��?��?�� 모터 출력 조정?�� ?��?�� 조금?���? 조정
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
       


# ?���? 구동
def startmotor(val):
    
    if val == "start":
        #?���? 구동?�� ?���?비행 ?��?�� ?��기에 ?��?�� ?��?�� ?��?��?�� ?��?��방향?���? ???직이게끔 추�?? ?��?��
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
                
                # 초기 비행?�� ?��?��?��?���? ?���?비행?�� ?��?���? ?��?��?�� 구동?��?�� 코드 (?���?비행 ?��?��?��?�� 모듈)
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
                        
                        
                        
                        
                        # �? 모터�? ?��?��?��?�� 반환?�� 모터 출력?�� ?��?��?��?�� ?��?���? �? 출력?�� 모터�? ?��?��보냄
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
                
                # ?���?비행 ?��?��?�� ?�� ?��?�� 출력?���? ?��공에?�� ?���?
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
                    



        # 긴급 ?���? (?��보드?�� ?��?��?�� ?��?�� ?��)

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
startmotor(val)   ## ?��?��주행 모듈�? �??�� ?��?�� ?��?���? 받으�? ?��?��
 
 
  



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







