

from time import sleep
import os
import sys
import time
import numpy as np


# �꽱�꽌�쓽 I2C�넻�떊 �룷�듃 吏��젙



# 紐⑦꽣 ���踰덊샇 �꽑�뼵 蹂��냽湲� �옣李⑺썑 蹂�寃쎈맆 �삁�젙




class param:              # �뿬湲곗뿉 �쁽�옱 媛��냽�룄 �젙蹂� ����옣 諛� 紐⑦꽣�쓽 異쒕젰 怨꾩궛 �썑 ����옣 (�룓猷⑦봽�뿉�꽌�쓽 �뵾�뱶諛깆뿉 �빐�떦)
    pos0 = np.zeros((3,1)) #
    pos1 = np.zeros((3,1)) #stable pos
    pos2 = np.zeros((3,1)) #
    
    #�젙吏� 鍮꾪뻾�떆 �븞�젙�솕 �릺�뒗 紐⑦꽣 異쒕젰
    posmotRFA = 100
    posmotLFA = 100
    posmotLBA = 100
    posmotRBA = 100

    
    
    


"""
<紐⑦꽣�쓽 �쐞移�>
LFA           RFA


LBA           RBA

�삁: RFA + �삤瑜몄そ �븵 紐⑦꽣 異쒕젰 �긽�듅, 媛� 媛��냽�룄媛믪씠 0�씪 寃쎌슦 �셿�쟾�븳 �닔�룊 �쑀吏� �긽�깭

�쇊 X-(媛��냽�룄媛�)  LFA + LBA + RFA - RBA -
�삤 X+(媛��냽�룄媛�)  RFA + RBA + LFA - LBA -
�븵 Y-(媛��냽�룄媛�)  RFA + LFA + RBA - RFA -
�뮘 Y+(媛��냽�룄媛�)  RBA + LBA + RFA - LFA -




ipos 媛� [0] = x醫뚰몴 [1] = y醫뚰몴  [2] = z醫뚰몴 ([2]媛믪�� �궗�슜�븯吏� �븡�쓬)
吏�硫댁쑝濡쒕���꽣�쓽 �넂�씠 ==> 媛��냽�룄怨꾩쓽 yaw 媛� 李멸퀬 (�븘吏� 援ы쁽 x)

"""
## �젙吏� 鍮꾪뻾�떆 �쇅�젰�씠 諛쒖깮�릺硫� �뒪�뒪濡� �옄�꽭 �젣�뼱瑜� �븯�뒗 �븿�닔

def iRFA(iposx,iposy,iposz,imotorRFA):
    if iposx > +1.5:      ## 媛��냽�룄怨꾩쓽 x媛믪씠 �븞�젙�맂 �긽�깭�씪�븣蹂대떎 1.5(����뼱吏� �젙�룄) �뜑 ����뼱吏� 寃쎌슦 鍮좊Ⅴ寃� �옄�꽭援먯젙
        imotorRFA += 10
        
        
    elif iposy < -1.5:    
        imotorRFA += 10
        
            
    elif iposx <= 1.5 and iposx > 0 :      ## �씠�쟾 肄붾뱶蹂대떎 �뜑 �옄�꽭�엳 紐⑦꽣 異쒕젰 議곗젙�쓣 �쐞�빐 議곌툑�뵫留� 議곗젙
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
        
       


# �뱶濡� 援щ룞
def startmotor(val):
    
    if val == "s":
        #�뱶濡� 援щ룞�썑 �젙吏�鍮꾪뻾 �뼢�썑 �뿬湲곗뿉 �듅�젙 �떊�샇 �엯�젰�떆 �뿬�윭諛⑺뼢�쑝濡� ���吏곸씠寃뚮걫 異붽�� �삁�젙
        try:
            while True:
                
                
                motorRFA = param.posmotRFA
                motorLFA = param.posmotLFA
                motorRBA = param.posmotRBA
                motorLBA = param.posmotLBA

                param.pos2[0] = -0.5
                param.pos2[1] = 1.5
                param.pos2[2] = 0
               
                # 珥덇린 鍮꾪뻾�떆 �븞�젙�쟻�쑝濡� �젙吏�鍮꾪뻾�씠 �븞�릺怨� �엳�쓣�떆 援щ룞�릺�뒗 肄붾뱶 (�젙吏�鍮꾪뻾 �옄�꽭�젣�뼱 紐⑤뱢)
                if abs(param.pos2[0]) >= abs(0)+0.3 or abs(param.pos2[1]) >= abs(0)+0.3 or param.pos2[2] >= abs(0):

                    while abs(param.pos2[0]) >= abs(0)+0.1 or abs(param.pos2[1]) >= abs(0)+0.1 or abs(param.pos2[2]) >= abs(0)+0.1:
                       

                        motorRFA = param.posmotRFA
                        motorLFA = param.posmotLFA
                        motorRBA = param.posmotRBA
                        motorLBA = param.posmotLBA

                        print("while pos2: ",param.pos2)
                        
                        
                        
                        
                        # 媛� 紐⑦꽣蹂� �븿�닔�뿉�꽌 諛섑솚�맂 紐⑦꽣 異쒕젰�쓣 �씠�슜�븯�뿬 �떎�젣濡� 洹� 異쒕젰�쓣 紐⑦꽣濡� �떊�샇蹂대깂
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
                
                # �젙吏�鍮꾪뻾 �븞�젙�솕 �떆 �빐�떦 異쒕젰�쑝濡� �긽怨듭뿉�꽌 �젙吏�
                else:
                    
                    
                       
                        time.sleep(0.1)
                        
                        

                        print("stable")
                        print(motorRFA)
                        print(motorLFA)
                        print(motorRBA)
                        print(motorLBA)
                    



        # 湲닿툒 �젙吏� (�궎蹂대뱶�뿉 �엯�젰�씠 �엳�쓣 �떆)

        except KeyboardInterrupt:
           exit()



   
   
val=input("Start Drone?")
startmotor(val)   ## �옄�쑉二쇳뻾 紐⑤뱢濡� 遺��꽣 �떆�옉 �떊�샇瑜� 諛쏆쑝硫� �떆�옉
 
 
  











