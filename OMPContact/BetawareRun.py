import os
import sys
import linecache

class UseBetawareToolMethod():
   
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
    
    def _runBetaware(self,fastaParsedPath,profilePath):
        ''' Use Betaware to predict topology
            @return: None
            @param fastaFilefile: The full path of the fastaFile, str
        ''' 
        Fastafilelist=os.listdir(fastaParsedPath)
        for each in Fastafilelist:
            wholepath = fastaParsedPath+'//'+each
            fastaFileLines = self._loadFile(wholepath)
            fastaFilecount = len(fastaFileLines)
            line = linecache.getlines(wholepath)
            i=0       
            while i <= fastaFilecount-1:
                myfile=open('//home//yangyn533//tool//experiment.fasta','w')
                myfile.write(line[i])
                myfile.write(line[i+1])
                myfile.close()
                pdbid=line[i][1:7]
                pdbid1 = pdbid.split(':')[0]
                pdbid2 = pdbid.split(':')[1]
                pdbid = pdbid1+'_'+pdbid2  
                i=i+2 
                cmd='export BETAWARE_ROOT=/home/yangyn533/betaware' and ' python /home/yangyn533/betaware/bin/betaware.py -t -o /home/yangyn533/tool/betaware/betawareResult/'+pdbid+'.out -f /home/yangyn533/tool/experiment.fasta -p /home/yangyn533/tool/profile/' + pdbid+'.prof'
                os.system(cmd)
                
def main():
    BetawareTool = UseBetawareToolMethod()
    BetawareTool._runBetaware('/home/yangyn533/tool/fastaparsed','/home/yangyn533/tool/profile')
if  __name__ == '__main__' :
    main()