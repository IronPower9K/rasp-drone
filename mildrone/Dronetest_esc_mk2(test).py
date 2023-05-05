

from time import sleep
import os
import sys
import time
import numpy as np


# 센서의 I2C통신 포트 지정



# 모터 핀번호 선언 변속기 장착후 변경될 예정




class param:              # 여기에 현재 가속도 정보 저장 및 모터의 출력 계산 후 저장 (폐루프에서의 피드백에 해당)
    pos0 = np.zeros((3,1)) #
    pos1 = np.zeros((3,1)) #stable pos
    pos2 = np.zeros((3,1)) #
    
    #정지 비행시 안정화 되는 모터 출력
    posmotRFA = 100
    posmotLFA = 100
    posmotLBA = 100
    posmotRBA = 100

    
    
    


"""
<모터의 위치>
LFA           RFA


LBA           RBA

예: RFA + 오른쪽 앞 모터 출력 상승, 각 가속도값이 0일 경우 완전한 수평 유지 상태

왼 X-(가속도값)  LFA + LBA + RFA - RBA -
오 X+(가속도값)  RFA + RBA + LFA - LBA -
앞 Y-(가속도값)  RFA + LFA + RBA - RFA -
뒤 Y+(가속도값)  RBA + LBA + RFA - LFA -




ipos 값 [0] = x좌표 [1] = y좌표  [2] = z좌표 ([2]값은 사용하지 않음)
지면으로부터의 높이 ==> 가속도계의 yaw 값 참고 (아직 구현 x)

"""
## 정지 비행시 외력이 발생되면 스스로 자세 제어를 하는 함수

def iRFA(iposx,iposy,iposz,imotorRFA):
    if iposx > +1.5:      ## 가속도계의 x값이 안정된 상태일때보다 1.5(틀어진 정도) 더 틀어진 경우 빠르게 자세교정
        imotorRFA += 10
        
        
    elif iposy < -1.5:    
        imotorRFA += 10
        
            
    elif iposx <= 1.5 and iposx > 0 :      ## 이전 코드보다 더 자세히 모터 출력 조정을 위해 조금씩만 조정
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
        
       


# 드론 구동
def startmotor(val):
    
    if val == "s":
        #드론 구동후 정지비행 향후 여기에 특정 신호 입력시 여러방향으로 움직이게끔 추가 예정
        try:
            while True:
                
                
                motorRFA = param.posmotRFA
                motorLFA = param.posmotLFA
                motorRBA = param.posmotRBA
                motorLBA = param.posmotLBA

                param.pos2[0] = -0.5
                param.pos2[1] = 1.5
                param.pos2[2] = 0
               
                # 초기 비행시 안정적으로 정지비행이 안되고 있을시 구동되는 코드 (정지비행 자세제어 모듈)
                if abs(param.pos2[0]) >= abs(0)+0.3 or abs(param.pos2[1]) >= abs(0)+0.3 or param.pos2[2] >= abs(0):

                    while abs(param.pos2[0]) >= abs(0)+0.1 or abs(param.pos2[1]) >= abs(0)+0.1 or abs(param.pos2[2]) >= abs(0)+0.1:
                       

                        motorRFA = param.posmotRFA
                        motorLFA = param.posmotLFA
                        motorRBA = param.posmotRBA
                        motorLBA = param.posmotLBA

                        print("while pos2: ",param.pos2)
                        
                        
                        
                        
                        # 각 모터별 함수에서 반환된 모터 출력을 이용하여 실제로 그 출력을 모터로 신호보냄
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
                
                # 정지비행 안정화 시 해당 출력으로 상공에서 정지
                else:
                    
                    
                       
                        time.sleep(0.1)
                        
                        

                        print("stable")
                        print(motorRFA)
                        print(motorLFA)
                        print(motorRBA)
                        print(motorLBA)
                    



        # 긴급 정지 (키보드에 입력이 있을 시)

        except KeyboardInterrupt:
           exit()



   
   
val=input("Start Drone?")
startmotor(val)   ## 자율주행 모듈로 부터 시작 신호를 받으면 시작
 
 
  











