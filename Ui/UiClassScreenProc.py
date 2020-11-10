
import sys
import time
import os


# ---------------------------------------------------------------------------------------
# System
# ---------------------------------------------------------------------------------------
sys.path.append('../DyEngine')
from System import _dyDrvMapTable, _dyIoMapTable,_dyAlarmTable, _dySequenceTable, _dySystemInfo

sys.path.append('../DyEngine/IO')
from AlarmStruct  import ALARM

sys.path.append('../DyEngine/Utility')
from UtilAlarmManager   import UtilAlarmManager 
# ---------------------------------------------------------------------------------------


class UiClassScreenProc: # Don't Change Class Name
    #def __init__(self, ScreenList:dict):
    def __init__(self, mainWindow, ScreenList):

        self.mainWindow = mainWindow
        self.ScreenList = ScreenList

        self.SeqControl          = _dySequenceTable.get('SeqEqControl')
        self.prmwhfunctionType   = _dyIoMapTable.get('prmwhfunctionType')
        self.prmScreenParameter         = _dyIoMapTable.get('prmScreenParameter')            # 화면 ID / 모드 ID
        ComStatus, prmScreenParameter = self.prmScreenParameter.Read()

        #

        #print('%s __init__ is Started'% __name__ )

        try:
            # ---------------------------------------------------------------------------------------
            #  Do Make the Screen Class for Signal and Procedure
            # ---------------------------------------------------------------------------------------
            for keyValue in self.ScreenList:
                #print('\n\n KeyValue(%s)' %( keyValue ) ) 
                self.screen = ScreenList.get(keyValue)
                print('keyVaule = {0}'.format(keyValue))
                if keyValue == 'UiScreenTop': #
                    self.screen.Show()     
                    
                elif keyValue == 'UiScreenRight': # 필수 : Screen별 정리
                    '''print( '\n------------------>> ', self.screen.GetInstacne('MainBtn'), self.screen.GetInstacne('StockBtn'), self.screen.GetInstacne('ConfigBtn') )'''
                    self.MainBtn = self.screen.GetObject('MainBtn')
                    self.MainBtn.GetInstance().clicked.connect(lambda:self.Navigation(self.MainBtn.GetScreenName(), self.MainBtn.GetOjbectName(), self.MainBtn.GetEventParam()) ) # Add the Signal Function                 
                                        
                    self.StockBtn = self.screen.GetObject('StockBtn')
                    self.StockBtn.GetInstance().clicked.connect(lambda:self.Navigation(self.StockBtn.GetScreenName(), self.StockBtn.GetOjbectName(), self.StockBtn.GetEventParam()) ) # Add the Signal Function                 
        
                    self.ConfigBtn = self.screen.GetObject('ConfigBtn')
                    self.ConfigBtn.GetInstance().clicked.connect(lambda:self.Navigation(self.ConfigBtn.GetScreenName(), self.ConfigBtn.GetOjbectName(), self.ConfigBtn.GetEventParam()) ) # Add the Signal Function                 
                     
        
                    self.screen.Show()
        
                #
                if keyValue == 'UiScreenMain':
                    if prmScreenParameter  == 1:
                       self.screen.Show()
                    else:
                       self.screen.Hide()
                elif keyValue == 'UiScreenMain2':
                    if prmScreenParameter == 2:
                        self.screen.Show()
                    else:
                        self.screen.Hide()
                elif keyValue == 'UiScreenStock':
                    self.screen.Hide()  
                #
                elif keyValue == 'UiScreenConfig': #
                    self.screen.Hide()
                   
                   
        
            #print('%s __init__ is Success'% __name__)
        
        except Exception as e:
            print('%s __init__ is Happened the exception! '%(__name__, e))

  # ---------------------------------------------------------------------------------------
    #  Define ths Slot(Procedure)
    # ---------------------------------------------------------------------------------------
    def Navigation(self, strOwerScreen, event, strScreenName): # User Area
        try:
            if strOwerScreen != None:
                #self.pAlarmManager.Hide()

                #print('%s Navigation 클릭이벤트 발생. KeyValue(%s > %s), Info(%s)'% (__name__, strOwerScreen, event, strScreenName) )
               #self.pAlarmManager.Hide()

                # ---------------------------------------------------------
                # 1. 버튼 상태값 조작
                # ---------------------------------------------------------
                #print('%s Navigation 클릭이벤트 발생. KeyValue(%s > %s), Info(%s)'% (__name__, strOwerScreen, event, strScreenName) )
                if event == 'MainBtn': # 버튼이 눌리면 명령수행 -> 액션
                    self.MainBtn.GetInstance().SetButtonStatus(1)
                    self.StockBtn.GetInstance().SetButtonStatus(0)
                    self.ConfigBtn.GetInstance().SetButtonStatus(0)
                    ComStatus, prmScreenParameter = self.prmScreenParameter.Read()
                    if   prmScreenParameter == 1:
                       strScreenName = 'UiScreenMain'

                    elif prmScreenParameter == 2:
                       strScreenName = 'UiScreenMain2'
                    
                  

                elif event == 'StockBtn': # 버튼이 눌리면 명령수행 -> 액션
                    self.MainBtn.GetInstance().SetButtonStatus(0)
                    self.StockBtn.GetInstance().SetButtonStatus(1)
                    self.ConfigBtn.GetInstance().SetButtonStatus(0)
                    #
                    self.SeqControl.Run('StockRead')
                elif event == 'ConfigBtn': # 버튼이 눌리면 명령수행 -> 액션
                    self.MainBtn.GetInstance().SetButtonStatus(0)
                    self.StockBtn.GetInstance().SetButtonStatus(0)
                    self.ConfigBtn.GetInstance().SetButtonStatus(1)

                #screen = self.ScreenList.get(strOwerScreen) # UiScreenRight
                for keyValue in self.ScreenList: 
                    #print('\n\n KeyValue(%s)' %( keyValue ) ) 
                    screen = self.ScreenList.get(keyValue)

                    if   keyValue == 'UiScreenTop': # default - always show
                         screen.Show()
                    elif keyValue == 'UiScreenRight': # default - always show
                         screen.Show() 
                    elif keyValue == strScreenName:
                            screen.Show()  
                    else:
                        screen.Hide()
                    
            #elif strScreenName == 'AlarmManager':
            #    #print('{0} : {1} : {2}'.format(strOwerScreen, event, strScreenName) )
            #    self.pAlarmManager.Show()

        except Exception as e:
            print('%s EventMainBtn Happened the exception! %s '%(__name__, e) )
    # ---------------------------------------------------------------------------------------
    # ---------------------------------------------------------------------------------------
    # UiClassScreenProc : Sequence로 등록 # 20200709KHK 
    # ---------------------------------------------------------------------------------------
    def SeqLoadComplete(self, strParam ): # Io Define
        try:
            print('%s > SeqLoadComplete is called (%s)'% (__name__, strParam))
            return True
        except Exception as e:
            print('%s SeqLoadComplete Happened the exception! %s '% (__name__, e))
            return False
    # ---------------------------------------------------------------------------------------
    def SeqInitComplete(self, strParam ): # Io Define -> 및 초기화
        try:
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
        try:
            print('%s > SeqMain is called (%s)'% (__name__, runCommand))
            if runCommand == 'receivedOrderNoLoadParameter':
                self.receivedOrderNo.GetInstance().LoadParameter()

            return 'SEQ_SUCCESS'
        except Exception as e:
            print('%s SeqMain Happened the exception! %s '% (__name__, e))

# ---------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------------------
# Entry or Tester
# ---------------------------------------------------------------------------------------
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    
    # ---------------------------------------------------------------------------------------
    # Create Windows
    # ---------------------------------------------------------------------------------------
    strScreenName   = 'UiClassScreenRight'
    strUiResource   = 'Y:/Ui/Resource/UiRightScreen.ui'
    strCoordinate   = '700, 100, 100, 380'
    stritemFile     = 'ScreenRight.xml'
    #stritemFile     = 'D:/DYICT/Engine/DyDevelopment/Development/UiClassScreen/ScreenRight.xml'
    #stritemFile     = 'D:\\DYICT\\Engine\\DyDevelopment\\Development\\UiClassScreen\\ScreenRight.xml'
    #
    # Case2. Seperate by Screen -> 20200401 Version 참고
    #UiClassScreenCreator(strScreenName, strUiResource, strCoordinate, stritemFile)
    #
    # Case3. Using the Screen List
    ScreenList = {}
    ScreenList[strScreenName] = UiClassScreen(strUiResource, strCoordinate, stritemFile)
    UiEventProcedure = UiClassEventProcedure(ScreenList)   


    sys.exit(app.exec())
    