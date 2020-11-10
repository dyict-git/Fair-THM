import sys
import time
import os
import time
#
from _thread import *
import threading

# ---------------------------------------------------------------------------------------
# System
# ---------------------------------------------------------------------------------------
sys.path.append('../DyEngine')
from System import IoMapTable, SystemInfo

#sys.path.append('Y:/Ui/Class')
#sys.path.append('../DyEngine/Ui/Class')
#from UiPopupAlarm import UiPopupAlarm
# ---------------------------------------------------------------------------------------


class SeqMonitoring: # Don't Change Class Name
    def __init__(self):
        try:
            # IO 선언 및 유효성 체크
            self.PMSns1 = IoMapTable.get('PMSns1')
            self.PMSns2 = IoMapTable.get('PMSns2')
            #
            start_new_thread(self.MonitoringThread, ('AAA','BBB') ) 
  
        except Exception as e:
            print('%s __init__ Happened the exception! %s '% (__name__, e))


    # ---------------------------------------------------------------------------------------
    # 온도/습도/.... 모니터링 예제
    # ---------------------------------------------------------------------------------------
    def MonitoringThread(self, ParamA, ParamB):
        print('%s MonitoringThread is started.'% (__name__))
 
        try:
            count = 0
            CommStatus = False
            while True:
                count += 1
                CommStatus, data = self.PMSns1.Read()
                print('%s DioPMSns1 -> %s, %d'% (__name__, CommStatus, data) )

                CommStatus, data = self.PMSns2.Read()
                print('%s DioPMSns2 -> %s, %d'% (__name__, CommStatus, data) )
                
                break;
                #time.sleep(5)

        except Exception as e:
            print('%s MonitoringThread is happened the exception! %s'% (__name__, e))
        
        finally:
            print('------------------------------------------\n%s MonitoringThread is end'% (__name__))


 
# ---------------------------------------------------------------------------------------
# Entry or Tester
# ---------------------------------------------------------------------------------------
if __name__ == "__main__":

    userSeq = SeqClassMainProcess()
   

    sys.exit()
    