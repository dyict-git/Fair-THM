#import socket
#from _thread import *
import time
#import threading
import sys
import os
from time import localtime, strftime

import requests

# ---------------------------------------------------------------------------------------
# System
# ---------------------------------------------------------------------------------------
sys.path.append('../DyEngine')
from System import _dyIoMapTable, _dySystemInfo

# -------------------------------------------------------------------------------------------------------------------------------------
# System Log - 기능삭제 20200619
# -------------------------------------------------------------------------------------------------------------------------------------
#strRootDir = os.getcwd() + '/'
#sys.path.append(strRootDir)
#from Starter import dySystemLog, dyErrorLog

#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------------------------------------------------
class DrvServerAPI():

    def __init__(self, ID1, ID2, ID3, ID4, ID5, ID6, ID7, ID8, ID9, ID10 ):
        try:
            print('> url({0}), giUID({1}), ciUID({2}), fiUID({3}), {4}, {5}, {6}, {7}, {8}, ID10({9})sec'.format(ID1, ID2, ID3, ID4, ID5, ID6, ID7, ID8, ID9, ID10))
            self.url        = ID1
            self.giUID      = ID2
            self.ciUID      = ID3
            self.fiUID      = ID4
            
            
            self.Timeout    = ID10

            # 내부변수 선언
            
            self.ErrorCode = 0

           #----------------------------------------------------------
        except Exception as e:
            print('{0} __init__ is happened the exception! url({1}, error({2}'.format(__name__, self.url, e))
    #-----------------------------------------------------------------------------------------------------------------------------------
    #def __del__(self):
    #    try:
    #       clientsocket.close() # 20200610
    #    except Exception as e:
    #        print('%s is detory, exception > %s'% (__name__, e))
    #-----------------------------------------------------------------------------------------------------------------------------------
    #-----------------------------------------------------------------------------------------------------------------------------------
    def Send(self, strSubUrl, sendData):
        try:
          # print('[%s][%s] - Send(%s)'% (strftime('%H:%M:%S',localtime()), __name__, sendData))
            sendUrl = self.url + strSubUrl
            res = requests.post( url=sendUrl, data = sendData, timeout=self.Timeout)

           #---------------------------------------------------------------------------
            # 비정상 : 받은데이타 유효성 검증
            #---------------------------------------------------------------------------
            if res.status_code != 200:
                self.ErrorCode = res.status_code
                #if res.reason == 'Not Found': # happened the Error : <Response [404]>
                print('{0} Communication Error! > Send {1}. But receive the Error({2}, {3})'.format(__name__, sendData, res.status_code, res.reason))
                return False, ''

            #---------------------------------------------------------------------------
            # 정상시 : 받은데이타 유효성 검증
            #---------------------------------------------------------------------------
            res.close()
            #print(res.text)
            return True, res.text
            #return True, res
        except Exception as e:
            print('%s > Send is happened the exception > %s'% (__name__, e))
    #-----------------------------------------------------------------------------------------------------------------------------------
    def DrvReadDigital(self, ID1, ID2, ID3, ID4): # IO 선언시 DI
        try:
            #----------------------------------------------------
            # 커맨드 포맷 만들기
            #----------------------------------------------------
            if ID1 == 101: # ErrorCode Report by User
                return True, self.ErrorCode
            return False, -3

        except Exception as e:
            return False, -1
    #-----------------------------------------------------------------------------------------------------------------------------------
    def DrvWriteDigital(self, ID1, ID2, ID3, ID4, setValue): # IO 선언시 DO
        print( '[%s] >> DO : [%d][%d][%d][%d] -> SetData[%s]' % (__name__, ID1, ID2, ID3, ID4, setValue) )

        return CommStatus, 0

    #-----------------------------------------------------------------------------------------------------------------------------------
    def DrvReadAnalog(self, ID1, ID2, ID3, ID4):
        print( '[%s] >> AI : [%d][%d][%d][%d]' % (__name__, ID1, ID2, ID3, ID4) )

    #-----------------------------------------------------------------------------------------------------------------------------------
    def DrvWriteAnalog(self, ID1, ID2, ID3, ID4, setValue):
        print( '[%s] >> AO : [%d][%d][%d][%d] -> SetData[%s]' % (__name__, ID1, ID2, ID3, ID4, setValue) )

    #-----------------------------------------------------------------------------------------------------------------------------------
    def DrvReadString(self, ID1, ID2, ID3, ID4):
        print( '[%s] >> SI : [%d][%d][%d][%d]' % (__name__, ID1, ID2, ID3, ID4) )
        
        if ID1 == 1:
            return True, self.localMaterialRegReportResult
        if ID1 == 20:
            return True, self.dataInfobyBarcode

        return False, ''
    #-----------------------------------------------------------------------------------------------------------------------------------
    def DrvWriteString(self, ID1, ID2, ID3, ID4, setValue):
        #print( '[%s] >> SO : [%d][%d][%d][%d] -> SetData[%s]' % (__name__, ID1, ID2, ID3, ID4, setValue) )

        if ID1 == 1: # 온습도 보고
            subUrl   = '/API/THMSystem/temphumi.api'
            value  = '{0},{1},{2},{3}'.format(self.giUID, self.ciUID, self.fiUID, setValue)
        elif ID1 == 2: # 알람보고
            subUrl   = '/API/THMSystem/alarm.api'
            value  = '{0},{1},{2},{3}'.format(self.giUID, self.ciUID, self.fiUID, setValue)
        elif ID1 == 3: # Stock 요청
            subUrl   = '/API/THMSystem/itemStockList.api'    
            value  = '{0},{1},{2},{3}'.format(self.giUID, self.ciUID, self.fiUID, setValue)
            saveFile = 'Parameter/stockinfo.cfg'

        else:
            print('Unknown ID Information {0},{1},{2},{3}. set({4})'.format(ID1, ID2, ID3, ID4, setValue) )
            return

        #----------------------------------------------------
        # 커맨드 보내기 및 데이타 분석
        #----------------------------------------------------
        sendData = dict(data = value)
        CommStatus, response = self.Send(subUrl, sendData)
        #print(response) 
        if CommStatus:
            if ID1 == 3: # 파일로 정보전달 데이타 저장
                self.SaveInfoFile(saveFile, response)
            return CommStatus

        return False
            
    #-----------------------------------------------------------------------------------------------------------------------------------
    def SaveInfoFile(self, saveFileName, strData):
        try:
          
            saveFileFullName = os.getcwd() + '/' + saveFileName
            with open(saveFileFullName, 'w') as fp:
                tokens = strData.split('|')
                for key in tokens:
                    fp.write( key )
                    fp.write('\n')
            
        except Exception as e:
            print('DrvserverAPI > SaveInfoFile >  Happened the exception! ({0})'.format(e))
        finally:
            fp.close() # 20200623 위치변경 - File Close
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

