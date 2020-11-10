import sys
import os
import time
#import numpy as np
#from datetime import date, datetime
from time import localtime, strftime
#
from _thread import *
import threading
#from datetime import datetime

import random
# ---------------------------------------------------------------------------------------
# System
# ---------------------------------------------------------------------------------------
sys.path.append('../DyEngine')
from System import _dyDrvMapTable, _dyIoMapTable,_dyAlarmTable, _dySequenceTable, _dySystemInfo

# -------------------------------------------------------------------------------------------------------------------------------------
# 모듈을 찾지 못함.
# -------------------------------------------------------------------------------------------------------------------------------------
#strRootDir = '{0}/Utility/'.format(os.getcwd())
#strRootDir = '{0}'.format(os.getcwd())
#sys.path.append(strRootDir)
# -------------------------------------------------------------------------------------------------------------------------------------
#strpath = '{0}/Utility/'.format(os.path.dirname(os.path.abspath(os.path.dirname(__file__))) )# 절대경로 path에 상위 경로에 대한 path를 추가해줘야 합니다
#print(strpath)
#sys.path.append(strpath)
# -------------------------------------------------------------------------------------------------------------------------------------
from .UtilFileController import FileManager   

# ---------------------------------------------------------------------------------------
COMMAND_COOL_BLOW = 11
CAMMAND_COOL_EVAP = 12
CAMMAND_COOL_CONDS = 13

CAMMAND_HEAT_BLOW = 21
CAMMAND_HEAT_EVAP = 22
# ---------------------------------------------------------------------------------------
eOFF = 0
eON  = 1
eCLOSE = 0
eOPEN = 1
# ---------------------------------------------------------------------------------------
#
# ---------------------------------------------------------------------------------------
class Sequence: # Don't Change Class Name
    def __init__(self):
        #try:
        #
        #    # ---------------------------------------------------------------------------------------
        #except Exception as e:
        #    print('%s __init__ Happened the exception! %s '% (__name__, e))
        print('%s > __init__ is called'% (__name__))

    # ---------------------------------------------------------------------------------------
    def SeqLoadComplete(self, strParam ): # Io Define
        try:
            print('%s > SeqLoadComplete is called (%s)'% (__name__, strParam))
            self.SendMessageTempHui     = _dyIoMapTable.get('SendMessageTempHui')
            self.SendMessageAlarm       = _dyIoMapTable.get('SendMessageAlarm')
            self.SendMessageStock       = _dyIoMapTable.get('SendMessageStock')
            #
            self.Temp1                  = _dyIoMapTable.get('Temp1')
            self.Humidity1              = _dyIoMapTable.get('Humidity1')
            self.Temp2                  = _dyIoMapTable.get('Temp2')
            self.Humidity2              = _dyIoMapTable.get('Humidity2')
            #
            self.prmHostReportTime      = _dyIoMapTable.get('prmHostReportTime')
            self.prmSetTemp             = _dyIoMapTable.get('prmSetTemp')
            self.prmValidTemp           = _dyIoMapTable.get('prmValidTemp')
            self.prmSetHumi             = _dyIoMapTable.get('prmSetHumi')
            self.prmValidHumi           = _dyIoMapTable.get('prmValidHumi')
            #
            self.prmSetTemp2             = _dyIoMapTable.get('prmSetTemp2')
            self.prmValidTemp2           = _dyIoMapTable.get('prmValidTemp2')
            self.prmSetHumi2             = _dyIoMapTable.get('prmSetHumi2')
            self.prmValidHumi2           = _dyIoMapTable.get('prmValidHumi2')

            #self.TEMP1UI                 = _dyIoMapTable.get('TEMP1UI')
            #self.HUMI1UI                 = _dyIoMapTable.get('HUMI1UI')
            #self.TEMP2UI                 = _dyIoMapTable.get('TEMP2UI')
            #self.HUMI2UI                 = _dyIoMapTable.get('HUMI2UI')
            #self.HUMI2UI                 = _dyIoMapTable.get('HUMI2UI')
            #                            
            self.prmMouduleID           = _dyIoMapTable.get('prmMouduleID')
            self.prmwhID                = _dyIoMapTable.get('prmwhID')
            self.prmwhfunctionType      = _dyIoMapTable.get('prmwhfunctionType')
            
            
            
            
            
            
     

            return True
        except Exception as e:
            print('%s SeqLoadComplete Happened the exception! %s '% (__name__, e))
            return False
    # ---------------------------------------------------------------------------------------
    def SeqInitComplete(self, strParam ): # Io Define -> 및 초기화
        try:
            print('%s > SeqInitComplete is called (%s)'% (__name__, strParam))

            t1 = threading.Thread(target=self.SeqMonitoringThread, args=('AAA',), daemon = True)
            t1.start()

            return True
        except Exception as e:
            print('%s SeqInitComplete Happened the exception! %s '% (__name__, e))
            return False
    # ---------------------------------------------------------------------------------------
    def SeqUnload(self, strParam ): # 프로그램 종료시
          try:
              print('%s > SeqUnload is called (%s)'% (__name__, strParam))
              return True
          except Exception as e:
              print('%s SeqUnload Happened the exception! %s '% (__name__, e))
              return False
    # ---------------------------------------------------------------------------------------
    def SeqOnEvent(self, strParam ): # 프로그램 동작시 이벤트형태로 명령을 전달받는다
          try:
              print('%s > SeqOnEvent is called (%s)'% (__name__, strParam))
          except Exception as e:
              print('%s SeqOnEvent Happened the exception! %s '% (__name__, e))
    # ---------------------------------------------------------------------------------------
    def SeqMain(self, runCommand, runParam='' ):
 

        if runCommand == 'StockRead':
            self.SeqStockRead()


        return 'SEQ_SUCCESS'

   # ---------------------------------------------------------------------------------------
    def SeqStockRead(self): 
          try:
               prmMouduleID = self.prmMouduleID.ReadValue()     
               prmwhID =  self.prmwhID.ReadValue()          
               prmwhfunctionType =   self.prmwhfunctionType.ReadValue()
              
               self.SendMessageStock.Write('{0},{1},{2}'.format(prmMouduleID,prmwhID,prmwhfunctionType))
          except Exception as e:
              print('%s SeqStockRead Happened the exception! %s '% (__name__, e))
    # ---------------------------------------------------------------------------------------
    def SeqHostReport(self,CurrentTemp1,CurrentHumi1,CurrentTemp2,CurrentHumi2,stdmaxtemp1,stdmintemp1,stdmaxhumid1,stdminhumid1,stdmaxtemp2,stdmintemp2,stdmaxhumid2,stdminhumid2): 
        try:
            moduleID =  self.prmMouduleID.ReadValue()
            whID    =  self.prmwhID.ReadValue()
           
            
            reportTime = strftime('%Y-%m-%d %H:%M:%S',localtime())
            message = ("{0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18}".
                                             format(moduleID,whID,CurrentTemp1,CurrentHumi1,stdmaxtemp1,stdmintemp1,stdmaxhumid1,stdminhumid1, reportTime, self.GetDateTimeStamp(),
                                                    whID,CurrentTemp2,CurrentHumi2,stdmaxtemp2,stdmintemp2,stdmaxhumid2,stdminhumid2, reportTime, self.GetDateTimeStamp()))
            #print('seqhostReport message :{0}'.format(message))
            self.SendMessageTempHui.Write(message)
        except Exception as e:
              print('%s SeqHostReport Happened the exception! %s '% (__name__, e))

    # ---------------------------------------------------------------------------------------
    def GetDateTimeStamp(self):
        return strftime('%Y-%m-%d %H:%M:%S', localtime())
    # ---------------------------------------------------------------------------------------
    def SeqMonitoringThread(self, seqParameter):

       # print('>>>>>>>>>>>>>>>>>>> Start SeqMonitoringThread >>>>>>>>>>>>>>>>>>>>>')
        try:
            CurrentTemp1 = 0
            CurrentHumi1 = 0
            CurrentTemp2 = 0
            CurrentHumi2 = 0

            prmSetTemp   = 0
            prmValidTemp = 0
            prmSetHumi   = 0
            prmValidHumi = 0
            
            prmSetTemp2   = 0
            prmValidTemp2 = 0
            prmSetHumi2   = 0
            prmValidHumi2 = 0
            
            stdmaxtemp1  = 0
            stdmintemp1  = 0
            stdmaxhumid1 = 0
            stdminhumid1 = 0
            stdmaxtemp2  = 0
            stdmintemp2  = 0
            stdmaxhumid2 = 0
            stdminhumid2 = 0

            # initialize for simulaiton

            time.sleep(10)
            prmSetTemp   = self.prmSetTemp.ReadValue()            
            prmValidTemp = self.prmValidTemp.ReadValue()          
            prmSetHumi   = self.prmSetHumi.ReadValue()            
            prmValidHumi = self.prmValidHumi.ReadValue()
            
            prmSetTemp2   = self.prmSetTemp2.ReadValue()            
            prmValidTemp2 = self.prmValidTemp2.ReadValue()          
            prmSetHumi2   = self.prmSetHumi2.ReadValue()            
            prmValidHumi2 = self.prmValidHumi2.ReadValue()

            

            #
            reportTime = 0
            startTime = time.time()
            while True:

                # ---------------------------------------------------------------------------------------
                # Simualtion Coding
                # ---------------------------------------------------------------------------------------
                if _dySystemInfo.SimulationMode is True: # Real Mode(With H/W)
                    randvalue = random.randint(25,26)
                    randvalue2 = random.randint(55,57)
                    randvalue3 = random.randint(26,27)
                    randvalue4 = random.randint(56,58)
                    
                    self.Temp1.Write(randvalue)
                    self.Humidity1.Write(randvalue2)
                   
                    self.Temp2.Write(randvalue3)
                    self.Humidity2.Write(randvalue4)


                # ---------------------------------------------------------------------------------------
                # 모니터링 시나리오
                # ---------------------------------------------------------------------------------------
                commStatus, reportTime = self.prmHostReportTime.Read()
                reportTime = reportTime * 60 # sec
                if (time.time() - startTime) > reportTime:
                    #Host Report
                    self.SeqHostReport(CurrentTemp1,CurrentHumi1,CurrentTemp2,CurrentHumi2,stdmaxtemp1,stdmintemp1,stdmaxhumid1,stdminhumid1,stdmaxtemp2,stdmintemp2,stdmaxhumid2,stdminhumid2)
                    startTime = time.time()
                #
                CommStatus, moduleID = self.prmMouduleID.Read()
                CommStatus, CurrentTemp1 = self.Temp1.Read()
                CommStatus, CurrentHumi1 = self.Humidity1.Read()

                CommStatus, CurrentTemp2 = self.Temp2.Read()
                CommStatus, CurrentHumi2 = self.Humidity2.Read()

                CommStatus, prmSetTemp   = self.prmSetTemp.Read()
                CommStatus, prmValidTemp = self.prmValidTemp.Read()      
                
                CommStatus, prmSetHumi   = self.prmSetHumi.Read()            
                CommStatus, prmValidHumi = self.prmValidHumi.Read() 
             
                CommStatus, prmSetTemp2   = self.prmSetTemp2.Read()
                CommStatus, prmValidTemp2 = self.prmValidTemp2.Read()
                
                CommStatus, prmSetHumi2   = self.prmSetHumi2.Read()            
                CommStatus, prmValidHumi2 = self.prmValidHumi2.Read() 
               
                stdmaxtemp1  = prmSetTemp + prmValidTemp
                stdmintemp1  = prmSetTemp - prmValidTemp

                stdmaxhumid1 = prmSetHumi + prmValidHumi
                stdminhumid1 = prmSetHumi - prmValidHumi

                stdmaxtemp2  = prmSetTemp2 + prmValidTemp2
                stdmintemp2  = prmSetTemp2 - prmValidTemp2

                stdmaxhumid2 = prmSetHumi2 + prmValidHumi2
                stdminhumid2 = prmSetHumi2 - prmValidHumi2


                if  CurrentTemp1 > stdmaxtemp1 or CurrentTemp1 < stdmintemp1 :
                    # 알람포스트
                   
                    message = ('{0},{1},Temp is Error'.format(moduleID,self.GetDateTimeStamp()))
                    #print('Temp1 현재온도:{0} 기준최대온도:{1} 기준최소온도:{2}'.format(CurrentTemp1,stdmaxtemp1,stdmintemp1))
                    self.SendMessageAlarm.Write(message)
                
                #                
                if CurrentHumi1 > stdmaxhumid1 or CurrentHumi1 < stdminhumid1 :
                    # 알람포스트
                   
                    message = ('{0},{1},Humidity is Error'.format(moduleID,self.GetDateTimeStamp()))
                    #print('Humi1 현재습도:{0} 기준최대습도:{1} 기준최소습도:{2}'.format(CurrentHumi1,stdmaxhumid1,stdminhumid1))
                    self.SendMessageAlarm.Write(message)

                #

                if  CurrentTemp2 > stdmaxtemp2 or CurrentTemp2 < stdmintemp2 :
                    # 알람포스트
                   
                    message = ('{0},{1},Temp2 is Error'.format(moduleID,self.GetDateTimeStamp()))
                    #print('Temp2 현재온도:{0} 기준최대온도:{1} 기준최소온도:{2}'.format(CurrentTemp2,stdmaxtemp2,stdmintemp2))
                    self.SendMessageAlarm.Write(message)

                #
                if  CurrentHumi2 > stdmaxhumid2 or CurrentHumi2 < stdminhumid2 :
                    # 알람포스트
                    
                    message = ('{0},{1},Humidity2 is Error'.format(moduleID,self.GetDateTimeStamp()))
                    #print('Humi2 현재습도:{0} 기준최대습도:{1} 기준최소습도:{2}'.format(CurrentHumi2,stdmaxhumid2,stdminhumid2))
                    self.SendMessageAlarm.Write(message)



                # ---------------------------------------------------------------------------------------
                # loop - Time Delay
                # ---------------------------------------------------------------------------------------
                time.sleep(10) # 600초(10분)마다 체크

        except Exception as e:
            print('%s SeqAutoMonitoring is happened the exception > %s'% (__name__, e))
        finally:
            print('************** %s SeqAutoMonitoring is finish!'% (__name__))
# ---------------------------------------------------------------------------------------
# Entry or Tester
# ---------------------------------------------------------------------------------------
if __name__ == "__main__":

    userSeq = SeqClassMainProcess()
   

    sys.exit()
    