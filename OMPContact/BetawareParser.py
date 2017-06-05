import os
import sys
import linecache

class BetwareParser():
    
    def _loadFile(self,file): 
        ''' Open the file with the path
            @return: The lines of the file
            @param file: The full path of the file, str
        '''                 
        try: 
            with open(file) as fh:
                filelines = fh.readlines() #read file and get all lines
            return filelines 
        except IOError as err:
            print('File error: '+err)
            
    def _convertBetawareResult(self,betawareResultPath):
        betawareResultlist=os.listdir(betawareResultPath)
        for each in betawareResultlist:
            wholepath = betawareResultPath+'//'+each
            pdbid = each.split('.')[0]
            lines = self._loadFile(wholepath)
            topologyFile = open('/home/yangyn533/tool/betaware/betawareSVMInput/'+pdbid+'.parsed.out','w+')
            for each in lines:
                if len(each.split()) > 0:
                    if each.split()[0] == 'SS':
                        line = each.split()[2]
                        topologyFile.write(line+'\n')
            topologyFile.close()
            
def main():
    _BetwareParser=BetwareParser()
    _BetwareParser._convertBetawareResult('/home/yangyn533/tool/betaware/betawareResult')
if  __name__ == '__main__' :
    main()    

                    