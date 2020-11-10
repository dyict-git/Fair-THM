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
from System import IoMapTable, SimulationMode

#sys.path.append('Y:/Ui/Class')
#sys.path.append('../DyEngine/Ui/Class')
#from UiPopupAlarm import UiPopupAlarm
# ---------------------------------------------------------------------------------------


class SeqEquipCtrl: # Don't Change Class Name
    def __init__(self):
        try:
            # IO 선언 및 유효성 체크
            self.PMSns1 = IoMapTable.get('DioPMSns1')
            self.PMSns2 = IoMapTable.get('DioPMSns2')
  
        except Exception as e:
            print('%s __init__ Happened the exception! %s '% (__name__, e))


    # ---------------------------------------------------------------------------------------
    # 
    # ---------------------------------------------------------------------------------------
    def RecvCommand(self, strCommand, strParam=''):
        print('%s MonitoringThread is started.'% (__name__))

        try:
            while True:
                result, data = PMSns1.Read()
                print('%s DioPMSns1 -> %s, %d'% (__name__, result, data) )

                result, data = PMSns2.Read()
                print('%s DioPMSns2 -> %s, %d'% (__name__, result, data) )
                
                time.sleep(1)

        except Exception as e:
            print('%s MonitoringThread is happened the exception! %s'% (__name__, e))



 
# ---------------------------------------------------------------------------------------
# Entry or Tester
# ---------------------------------------------------------------------------------------
if __name__ == "__main__":

    userSeq = SeqClassMainProcess()
   

    sys.exit()
    