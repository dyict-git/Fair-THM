import sys
import os
import time
from Driver.ServerApiDrv import DrvServerAPI
from Driver.RpiGpioDrv   import DrvRpiGpio
# ---------------------------------------------------------------------------------------
# System
# ---------------------------------------------------------------------------------------
sys.path.append('../DyEngine')
from System import _dyDrvMapTable, _dyIoMapTable,_dyAlarmTable, _dySequenceTable, _dySystemInfo


sys.path.append('../DyEngine/IO')
from IoStruct import DI, DO, AI, AO, SI, SO, SEQ


# ---------------------------------------------------------------------------------------
# Define the IO :  실제통신 IO - Driver생성 -> IO 생성 -> _dyIoMapTable에 등록,
# --------------------------------------------------------------------- ------------------
# 단계1. 실제통신 IO - Driver생성
# ---------------------------------------------------------------------------------------
# Default None for Simulation Mode(Without H/W)
mDrvRpiGpio     = None
mDrvServerAPI   = None

if _dySystemInfo.SimulationMode is not True: # Real Mode(With H/W)
    mDrvRpiGpio = DrvRpiGpio('2|3','', 0, 0, 0, 0, 0, 0, 0, 0) 
    


moduleID = 1
#DrvSamjinAPI = DrvSamjinAPI('http://samjin.nescorp.kr', 0, 0, 0, 0, 0, 0, 0, 0, 500) # 'Samjin.nescorp.kr 80
mDrvServerAPI = DrvServerAPI('http://sy.nescorp.kr', 100001, 1001, 10000001, 0, 0, 0, 0, 0, 1) # 'Samjin.nescorp.kr 80, ID10(Timeout)=sec
#
_dyDrvMapTable.put('mDrvRpiGpio', mDrvRpiGpio)
_dyDrvMapTable.put('mDrvServerAPI', mDrvServerAPI)

# ---------------------------------------------------------------------------------------
# 단계2. IO 생성 -> _dyIoMapTable에 등록,
# ---------------------------------------------------------------------------------------
# mPMSnsDrv1 / mPMSnsDrv2    port(ID1), board(2), bytesze(3), stopbit(4), parity(5),ID6,ID7,ID8,ID9, (timeout)ID10

# mDrvRpiGpio  :  GPIO IN
Temp1           = DI(mDrvRpiGpio, 2, 1, 1, 1, 2,      '', '', ''); _dyIoMapTable.put('Temp1', Temp1)
Humidity1       = DI(mDrvRpiGpio, 2, 2, 1, 1, 2,      '', '', ''); _dyIoMapTable.put('Humidity1', Humidity1)
Temp2           = DI(mDrvRpiGpio, 3, 1, 1, 1, 2,      '', '', ''); _dyIoMapTable.put('Temp2', Temp2)
Humidity2       = DI(mDrvRpiGpio, 3, 2, 1, 1, 2,      '', '', ''); _dyIoMapTable.put('Humidity2', Humidity2)

# mDrvRpiGpio  :  GPIO OUT - 릴레이
#Evaporator1Heat     = DO(mDrvRpiGpio, 4, 1,  1, 1, 'poll', 'Off|On', '', ''); _dyIoMapTable.put('Evaporator1Heat', Evaporator1Heat)
                                                 
# mDrvServerAPI

SendMessageTempHui   = SO(mDrvServerAPI, 1, 1, 1, 1, 2, ); _dyIoMapTable.put('SendMessageTempHui', SendMessageTempHui)
SendMessageAlarm     = SO(mDrvServerAPI, 2, 1, 1, 1, 2, ); _dyIoMapTable.put('SendMessageAlarm',   SendMessageAlarm)
SendMessageStock     = SO(mDrvServerAPI, 3, 1, 1, 1, 2, ); _dyIoMapTable.put('SendMessageStock',   SendMessageStock)


# ---------------------------------------------------------------------------------------
# 단계2. 가상 IO - 전역변수 처럼 사용 가능 =>> DO
# ---------------------------------------------------------------------------------------
#TEMP1UI = DO('None', -1, -1, -1, -1, 2, '','0,10','');         _dyIoMapTable.put('TEMP1UI',TEMP1UI)
#HUMI1UI = DO('None', -1, -1, -1, -1, 2, '','0,10','');         _dyIoMapTable.put('HUMI1UI',HUMI1UI)
#TEMP2UI = DO('None', -1, -1, -1, -1, 2, '','0,10','');         _dyIoMapTable.put('TEMP2UI',TEMP2UI)
#HUMI2UI = DO('None', -1, -1, -1, -1, 2, '','0,10','');         _dyIoMapTable.put('HUMI2UI',HUMI2UI)


prmHostReportTime      = DO('None', -1, -1, -1, -1, 2, '','0, 10','');            _dyIoMapTable.put('prmHostReportTime',prmHostReportTime) # 단위 : 분
prmSetTemp             = DO('None', -1, -1, -1, -1, 2, '','-40,40','');           _dyIoMapTable.put('prmSetTemp',prmSetTemp)
prmValidTemp           = DO('None', -1, -1, -1, -1, 2, '','-40,40','');           _dyIoMapTable.put('prmValidTemp',prmValidTemp)
prmSetHumi             = DO('None', -1, -1, -1, -1, 2, '','0,100','');            _dyIoMapTable.put('prmSetHumi',prmSetHumi)
prmValidHumi           = DO('None', -1, -1, -1, -1, 2, '','0,100','');            _dyIoMapTable.put('prmValidHumi',prmValidHumi)
                      
prmSetTemp2            = DO('None', -1, -1, -1, -1, 2, '','-40,40','');          _dyIoMapTable.put('prmSetTemp2',prmSetTemp2)
prmValidTemp2          = DO('None', -1, -1, -1, -1, 2, '','-40,40','');          _dyIoMapTable.put('prmValidTemp2',prmValidTemp2)
prmSetHumi2            = DO('None', -1, -1, -1, -1, 2, '','0,100','');           _dyIoMapTable.put('prmSetHumi2',prmSetHumi2)
prmValidHumi2          = DO('None', -1, -1, -1, -1, 2, '','0,100','');           _dyIoMapTable.put('prmValidHumi2',prmValidHumi2)
                      
prmMouduleID           = DO('None', -1, -1, -1, -1, 2, '','0,100','');           _dyIoMapTable.put('prmMouduleID',prmMouduleID)
prmwhID                = DO('None', -1, -1, -1, -1, 2, '','0,100','');           _dyIoMapTable.put('prmwhID',prmwhID)
prmwhfunctionType      = DO('None', -1, -1, -1, -1, 2, '','0,100','');           _dyIoMapTable.put('prmwhfunctionType',prmwhfunctionType)
prmScreenParameter     = DO('None', -1, -1, -1, -1, 2, '','1,2','');             _dyIoMapTable.put('prmScreenParameter',prmScreenParameter)
                                                                                



# ---------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------
# 단계3. Define the Sequence : IO Loading -> SEQ Setup()
# ---------------------------------------------------------------------------------------
from Sequence.SeqEqControl import Sequence as SeqEqControl

sequence = SEQ('SeqEqControl', SeqEqControl() ); _dySequenceTable.put('SeqEqControl',  sequence)



# ---------------------------------------------------------------------------------------
# Entry or Tester
# ---------------------------------------------------------------------------------------
if __name__ == "__main__": 
    ioDistacne = _dyIoMapTable.get('DioDistance')
    for i in range(1,10):
        print('%d > %d' % (i, ioDistacne.Read()) )

    sys.exit(app.exec())
    
