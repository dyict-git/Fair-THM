# *******************************************
# Raspyberry GpioPin
# 수정 : 2020. 05. 12
# 제작 : DoYeong ICT
# SW ver. 1.0.0
# *******************************************
import os
import sys
import time
from time import localtime, strftime
import threading

import RPi.GPIO as GPIO
#import Adafruit_DHT  # 20200520, 현진이가 직접설치) -> 사용하는 선언문 : 실제사용 선언문 *************


GPIO.setmode(GPIO.BCM)

class DrvRpiGpio: # GPIO Pin is using the IN by by Single pin
	#def __init__(self):
    def __init__(self, ID1, ID2, ID3, ID4, ID5, ID6, ID7, ID8, ID9, ID10 ): # ID1 = DI Pin, ID2 = DO, ID3 = AI, ID4 = AO
        
      
        self.Temp1      = 0.0
        self.Huminity1  = 0.0
        self.Temp2      = 0.0
        self.Huminity2  = 0.0
        #print('------------------------------------------------------')
        #print('%s > __init__ > (%s), (%s), %d, %d, %d, %d, %d, %d, %d, %d' % (__name__,  ID1, ID2, ID3, ID4, ID5, ID6, ID7, ID8, ID9, ID10))
        try:
            #-------------------------------------------------------------------------
            # ID1 - DI
            #-------------------------------------------------------------------------
            GPIO.setwarnings(False)
            ch = 0
            try:           
                if len(ID1) > 0 and ID1.find('|'):
                    ID1.strip() #공백제거
                    Tokens = ID1.split('|')
                    for i in range(0, len(Tokens)):
                        #print('%d , %d'% (i, int(InTokens[i]) ))
                        if str(Tokens[i]).isdecimal():
                            ch = int(Tokens[i])
                            if ch > 0 and ch < 28 : #
                                GPIO.setup(ch, GPIO.IN) # GPI 설정
            except Exception as e:
                print("%s is happened the exception when PIO.IN"% __name__)            

            #-------------------------------------------------------------------------
            # ID2 - DI
            #-------------------------------------------------------------------------
            try:    
                if len(ID2) > 0 and ID2.find('|'):
                    ID2.strip() #공백제거
                    Tokens = ID2.split('|')
                    for i in range(0, len(Tokens)):
                        #print(str(OutTokens[i]))   
                        if str(Tokens[i]).isdecimal():
                            ch = int(Tokens[i])
                            if ch > 0 and ch < 28 : #
                                GPIO.setup(ch, GPIO.OUT) # GPI 설정
                                #-----------------------------------------------
                                # PIN 18 : PWM (Inverter)
                                #-----------------------------------------------
                                self.pwm_inverter = GPIO.PWM(ch, 500)
                                self.pwm_inverter.start(0) # 초기화 0 : 초기에 0으로 시작

            except Exception as e:
                print("%s is happened the exception when PIO.OUT"% __name__)
           
            #-------------------------------------------------------------------------
            # ID3 / ID4 - AI/AO -> PWM
            #-------------------------------------------------------------------------


            # ---------------------------------------------------------------------------------------
            # Option
            # ---------------------------------------------------------------------------------------
            self.itemData = 0
            #
            t1 = threading.Thread(target=self.DrvMonitoringThread, args=(2,), daemon=True) # 20200610
            t1.start()

        except Exception as e:
            self.ErrorLog(0, ID1, ID2, ID3, ID4, 'Exeption!-{0}'.format(e) )
    #-----------------------------------------------------------------------------------------------------------------------------------
    def __del__(self):
        print("%s is destroy"% __name__)

    #-----------------------------------------------------------------------------------------------------------------------------------
    def DrvMonitoringThread(self, polling): # Option 
        try:
            CH1 = 2
            CH2 = 3
            self.CommError1 = False
            self.CommErrorCntCH1 = 0
            self.CommError2 = False
            self.CommErrorCntCH2 = 0
            while True:
                time.sleep(polling)
                #self.ser._update_rts_state()  # 20200521
                readHuminity, readTemp =Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, CH1)
                if readTemp == None or readHuminity == None:
                    self.CommErrorCntCH1 += 1
                    if self.CommErrorCntCH1 > 3: # 3회이상 에러이면, 에러 정보 출력
                        print('[{0}][{1}], DHT22 온도센서1 Received Data is none.  H({2}), T({3})'.format(strftime('%H:%M:%S', localtime()), __name__ ,readHuminity, readTemp) )
                        self.CommError1 = True
                        self.CommErrorCntCH1 = 0 # 에러메시지 출력, 카우트 초기화
                else:
                    self.Huminity1 = readHuminity
                    self.Temp1     = readTemp
                     #
                    self.CommError1 = False
                    self.CommErrorCntCH1 = 0 # 정상 : 에러 카운트 초기화
                #
                time.sleep(1)
                readHuminity, readTemp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, CH2)
                if readTemp == None or readHuminity == None:
                    self.CommErrorCntCH2 += 1

                    if self.CommErrorCntCH2 > 3: # 3회이상 에러이면, 에러 정보 출력
                        print('[{0}][{1}], DHT22 온도센서2 Received Data is none.  H({2}), T({3})'.format(strftime('%H:%M:%S', localtime()), __name__ ,readHuminity, readTemp) )
                        self.CommError2 = True
                        self.CommErrorCntCH2 = 0 # 에러메시지 출력, 카우트 초기화
                else:
                    self.Huminity2 = readHuminity
                    self.Temp2 = readTemp
                    #
                    self.CommError2 = False
                    self.CommErrorCntCH2 = 0 # 정상 : 에러 카운트 초기화

        except Exception as e:
            print('{0} > DrvMonitoringThread() is happened the exception! {1}'.format(__name__, e) )
    #-----------------------------------------------------------------------------------------------------------------------------------
    def DrvReadDigital(self, ID1, ID2, ID3, ID4):
        #start_time = time.time()
        try:

            #print('A : %fsecs'% (time.time() - start_time))
            if ID1 > 0 and ID1 <= 27:
                if ID1 == 2 : # DHT22 - Temp / Humidity
                    if ID2 == 1: # temp 일때만 통신으로 읽고, Huminity는 Buffer값을 활용한다
                        #self.Huminity1, self.Temp1 = Adafruit_DHT.read_retry( Adafruit_DHT.DHT22, ID1 )
                        ## -> 센서 에러시 40초정도의 타임아웃 걸림.????
                        if self.CommError1:
                            return False, 0
                        else:
                            return True, round(self.Temp1, 2)
                    elif ID2 == 2: # Humidity
                        if self.CommError1:
                            return False, 0
                        else:
                            return True, round(self.Huminity1, 2) 
                    else:
                         print( '[%s] >> DI ID is Error : [%d][%d][%d][%d]' % (__name__, ID1, ID2, ID3, ID4) )
                         return False, 0
                #
                elif ID1 == 3: # DHT22 - Temp / Humidity
                     if  ID2 == 1: # temp
                         #self.Huminity2, self.Temp2 = Adafruit_DHT.read_retry( Adafruit_DHT.DHT22, ID1 )
                         ##
                         if self.CommError2 :
                            return False, 0
                         else:
                            return True, round(self.Temp2, 2) 
                     elif ID2 == 2: # Humidity
                        if self.CommError2 :
                            return False, 0 
                        else:
                            return True, round(self.Huminity2, 2) 
                     else:
                         print( '[%s] >> DI ID is Error : [%d][%d][%d][%d]' % (__name__, ID1, ID2, ID3, ID4) )
                         return False, 0
                else:
                    if GPIO.input(ID1) == False: # GPI 읽기
                        return True, 1
                    else:
                        return True, 0
            else:
                self.ErrorLog(1, ID1, ID2, ID3, ID4, 'ID1 is range error')
            return False, -1
        except Exception as e:
            self.ErrorLog(1, ID1, ID2, ID3, ID4, 'Exeption!-{0}'.format(e) )
            #print('B : %fsecs'% (time.time() - start_time))
            return False, -1

    #-----------------------------------------------------------------------------------------------------------------------------------
    def DrvWriteDigital(self, ID1, ID2, ID3, ID4, setValue):
        try:
            if ID1 > 0 and ID1 <= 27:
                #-----------------------------------------------
                # PIN 18 : PWM (Inverter)
                #-----------------------------------------------
                if ID1 == 18: # Inverter : using PWM
                    self.pwm_inverter.ChangeDutyCycle(setValue)

                #-----------------------------------------------
                # Normal Pin : Off(0) / On(1)
                #-----------------------------------------------
                else:
                    if setValue == 1:
                        GPIO.output(ID1, setValue) # GPI 쓰기
                    else:
                         GPIO.output(ID1, 0)
                return True
            else:
                self.ErrorLog(2, ID1, ID2, ID3, ID4, 'ID1 is range error')
            return False
        except Exception as e:
            self.ErrorLog(2, ID1, ID2, ID3, ID4, 'Exeption!-{0}'.format(e) )
            return False

    #-----------------------------------------------------------------------------------------------------------------------------------
    def DrvReadAnalog(self, ID1, ID2, ID3, ID4):
        print( '[%s] >> AI : [%d][%d][%d][%d]' % (__name__, ID1, ID2, ID3, ID4) )

    #-----------------------------------------------------------------------------------------------------------------------------------
    def DrvWriteAnalog(self, ID1, ID2, ID3, ID4, setValue):
        print( '[%s] >> AO : [%d][%d][%d][%d] -> SetData[%s]' % (__name__, ID1, ID2, ID3, ID4, setValue) )

    #-----------------------------------------------------------------------------------------------------------------------------------
    def DrvReadString(self, ID1, ID2, ID3, ID4):
        print( '[%s] >> SI : [%d][%d][%d][%d]' % (__name__, ID1, ID2, ID3, ID4) )

    #-----------------------------------------------------------------------------------------------------------------------------------
    def DrvWriteString(self, ID1, ID2, ID3, ID4, setValue):
        print( '[%s] >> SO : [%d][%d][%d][%d] -> SetData[%s]' % (__name__, ID1, ID2, ID3, ID4, setValue) )

    #-----------------------------------------------------------------------------------------------------------------------------------
    def ErrorPrint(self, IOType, ID1, ID2, ID3, ID4):
        if IOType == 0: # Driver Init
            print( '{0} >> Init Error : [{1},{2},{3},{4}]'.format(__name__, ID1, ID2, ID3, ID4) )
        elif IOType == 1: # DI
            print( '{0} >> DI Error : [{1},{2},{3},{4}]'.format(__name__, ID1, ID2, ID3, ID4) )
        elif IOType == 2: # DO
            print( '{0} >> DO Error : [{1},{2},{3},{4}]'.format(__name__, ID1, ID2, ID3, ID4) )
        elif IOType == 3: # AI
            print( '{0} >> AI Error : [{1},{2},{3},{4}]'.format(__name__, ID1, ID2, ID3, ID4) )
        elif IOType == 4: #AO
            print( '{0} >> AO Error : [{1},{2},{3},{4}]'.format(__name__, ID1, ID2, ID3, ID4) )
        elif IOType == 5: # SI
            print( '{0} >> SI Error : [{1},{2},{3},{4}]'.format(__name__, ID1, ID2, ID3, ID4) )
        elif IOType == 6: # SO
            print( '{0} >> SO Error : [{1},{2},{3},{4}]'.format(__name__, ID1, ID2, ID3, ID4) )
        else: #DO
            print( '[%s] >> Unknown data type' % __name__)	
             
    def ErrorLog(self, IOType, ID1, ID2, ID3, ID4, strError):
        strTime = strftime('%H:%M:%S', localtime())
        if IOType == 0: # Driver Init
            print( '[{0}][{1}], Init Error[{2},{3},{4},{5}],[{6}]'.format(strTime, __name__, ID1, ID2, ID3, ID4, strError) )
        elif IOType == 1: # DI
            print( '[{0}][{1}], DI Error[{2},{3},{4},{5}],[{6}]'.format(strTime, __name__, ID1, ID2, ID3, ID4, strError) )
        elif IOType == 2: # DO
            print( '[{0}][{1}], DO Error[{2},{3},{4},{5}],[{6}]'.format(strTime, __name__, ID1, ID2, ID3, ID4, strError) )
        elif IOType == 3: # AI
            print( '[{0}][{1}], AI Error[{2},{3},{4},{5}],[{6}]'.format(strTime, __name__, ID1, ID2, ID3, ID4, strError) )
        elif IOType == 4: #AO
            print( '[{0}][{1}], AO Error[{2},{3},{4},{5}],[{6}]'.format(strTime, __name__, ID1, ID2, ID3, ID4, strError) )
        elif IOType == 5: # SI
            print( '[{0}][{1}], SI Error[{2},{3},{4},{5}],[{6}]'.format(strTime, __name__, ID1, ID2, ID3, ID4, strError) )
        elif IOType == 6: # SO
            print( '[{0}][{1}], SO Error[{2},{3},{4},{5}],[{6}]'.format(strTime, __name__, ID1, ID2, ID3, ID4, strError) )
        else: #DO
            print( '[%s][%s] >> Unknown data type' %(strTime, __name__))	
    #-----------------------------------------------------------------------------------------------------------------------------------

def main():
    drv = DrvRpiGpioSI(21,20,16,0,0,0,0,0,0,0)
    print( drv.DrvReadDigital(21,1,1,1) )
    print( drv.DrvReadDigital(20,1,1,1) )
    print( drv.DrvReadDigital(16,1,1,1) )
    pass

if __name__=="__main__":
	main()
