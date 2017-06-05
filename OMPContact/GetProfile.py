import os
import sys
import linecache
from numpy import *

class GetProfile():
    
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
            
    def _GenerateProfile(self,pssmResultPath):
        ''' To get the conservation feature by pdbid 
            @return: None
        '''
        PSSMfilelist=os.listdir(pssmResultPath)
        for each in PSSMfilelist:
            WholePath = pssmResultPath+'//'+each
            pdbid = each.split('.')[0]
            outfile = pdbid + '.prof'
            writefile = open('//home//yangyn533//tool//profile//'+outfile, 'w')
            lines = linecache.getlines(WholePath)
            pssmlist = []
            for line in lines:
                content = line.split()
                if len(content) == 44:
                    linelist = []
                    for i in range(22,42):
                        linelist.append(float(content[i]))
                    pssmlist.append(linelist)
            pssmMatrix = array(pssmlist)
            linenum,colnum = pssmMatrix.shape
            for a in range(linenum):
                for b in range(colnum):
                    if b != colnum-1:
                        writenum = pssmMatrix[a,b]/100
                        writefile.write('%.2f'%writenum)           
                        writefile.write(' ')
                    else:
                        writenum = pssmMatrix[a,b]/100
                        writefile.write('%.2f'%writenum)
                        writefile.write('\n')
            writefile.close()

def main():
    _GetProfile = GetProfile()
    _GetProfile._GenerateProfile('/home/yangyn533/tool/psiblastResult/pssm')
if  __name__ == '__main__' :
    main()    

        