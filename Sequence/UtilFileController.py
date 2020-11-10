#print("importing_ ",__name__)

class FileManager:
    def __init__(self, filepath):
        #self.Files=["Action.txt","Drain.txt","OnOff.txt","Rest.txt"]

        self.FilePath = filepath + '/'

        self.Files={"Action.txt":"state|ation|cool,compS|On$",
                    "Drain.txt":"time|drain|00:00,00:00,00:00,00:00,00:00,00:00|19961009$",
                    "OnOff.txt":"time|onoff|00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00|20200000$",
                    "RestDay.txt":"time|rest|0101,0505,0827,1009,1225|19961009$",
                    "Inve.txt":"inve|3$"}
        self.initFile()

        '''
        self.actionFile="Action.txt"
        self.drainFile="Drain.txt"
        self.onoffFile="OnOff.txt"
        self.restFile="Rest.txt"
        '''
    '''파일의 존재 확인, 없으면 임의값으로 초기화'''
    def initFile(self):
        for File in self.Files.keys():
            try:
                #with open(File,"r") as f:
                FileFullName = self.FilePath + File
                with open(FileFullName,"r") as f:
                    f.close()
                    #print("Read File is success. [%s]"% FileFullName)
                    pass
            except Exception as e:
                try:
                #f=open(File,"w")
                    #f.write(self.Files[File])
                    #f.close()
                    FileFullName = self.FilePath + File
                    print("There is no File, execute auto initializing. [%s]"% FileFullName)
                    f=open(FileFullName,"w")
                    f.write( self.Files[File] )
                    f.close()
                except Exception as e:
                    print("There is no File, execute auto initializing is exception! [%s]"% e)

    '''해당 파일의 내용 반환'''
    def readFile(self, filename):
        try:
            #with open(filename,"r") as f:
            FileFullName = self.FilePath + filename
            with open(FileFullName,"r") as f:
                data = f.readline()
                f.close()
                return data
        except Exception as e:
            print("getData. Excepiton! %s"% e)
        pass

    '''해당 파일에 내용 작성'''
    def writeFile(self,filename,contents):
        try:
           #with open(filename,"w") as f:
            FileFullName = self.FilePath + filename
            #print( FileFullName,' : ', contents)
            with open(FileFullName,"w") as f:
                f.write(contents)
                f.close()
        except Exception as e:
            print("writeFile. Excepiton! %s"% e)
        pass

    '''해당 파일의 버전정보 반환'''
    def getVersion(self,filename):
        try:
            #with open(filename,"r") as f:
             FileFullName = self.FilePath + filename
             with open(FileFullName,"r") as f:
                version = (f.readline()).split('$') #끝의 필요없는 $ 자르고
                version = version[0].split('|') #구분자 ('|')로 나누고
                version = version[-1]           #맨 마지막 문자열이 버전
                f.close()
                return version
        except Exception as e:
            print("getVersion. Excepiton! %s"% e)


def main():
    test= FileManager()
    teststr = "time|onoff|01:00,02:00,20:00,21:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00,00:00|19961009"
    test.writeFile("OnOff.txt",teststr)
    print(test.getVersion("OnOff.txt"))
    pass

if __name__ == "__main__":
    main()
