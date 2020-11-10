
import sys
import time
import os

# ---------------------------------------------------------------------------------------
# System
# ---------------------------------------------------------------------------------------
sys.path.append('../DyEngine')
#from System import IoMapTable, SimulationMode
from System import IoMapTable, SystemInfo

#sys.path.append('Y:/Ui/Class')
#sys.path.append('../DyEngine/Ui/Class')
#from UiPopupAlarm import UiPopupAlarm
# ---------------------------------------------------------------------------------------

from SeqMonitoring import SeqMonitoring



class SeqClassMainProcess: # Don't Change Class Name
    def __init__(self):
        try:
            print('%s __init__ is Started'% __name__)
  
        except Exception as e:
            print('%s __init__ Happened the exception! %s '% (__name__, e))

    # ---------------------------------------------------------------------------------------
    #  Define User Sequence. It is called by Engine
    # ---------------------------------------------------------------------------------------
    def SequenceMapTable(self): # Don't Change Sequence Name 
        try:
            # thread or Monitoring 정의
            #UiClassScreen Button 연동 정의 등...
            fSeqMonitoring = SeqMonitoring()

            print('%s SequenceMapTable is called'% (__name__) )
        except Exception as e:
            print('%s SequenceMapTable Happened the exception! %s '% (__name__, e))

 
# ---------------------------------------------------------------------------------------
# Entry or Tester
# ---------------------------------------------------------------------------------------
if __name__ == "__main__":

    userSeq = SeqClassMainProcess()
   

    sys.exit()
    