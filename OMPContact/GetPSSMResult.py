import os
import sys
import linecache
import numpy as np

class DealPSSM():
    
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

    def _dealPssmFile(self,psiblastResultPath):
        ''' To get the conservation feature by pdbid 
            @return: None
        '''
        PSSMfilelist=os.listdir(psiblastResultPath)
        for each in PSSMfilelist:
            WholePath = psiblastResultPath+'//'+each
            pdbid = each.split('.')[0]
            print('get input')
            order=input()
            if order =='back':
                residuePosition = {"A":22,"R":23,"N":24,"D":25,"C":26,"Q":27,"E":28,"G":29,"H":30,"I":31,"L":32,"K":33,"M":34,"F":35,"P":36,"S":37,"T":38,"W":39,"Y":40,"V":41}
                pssmFileLines = self._loadFile(WholePath)
                outfile = pdbid + '.txt'
                writefile = open('/home/yangyn533/tool/features/'+outfile, 'w+')
                for line in pssmFileLines:
                    lines = line.split()                
                    if len(lines) == 44:
                        residue = lines[1] 
                        if residue == "X":
                            outline = residue + ' 1:0.00'
                        else:
                                position = residuePosition[residue]
                                ele = self._dealPssmfrequency(lines, position)                  
                                outline = residue + ' '+ele
                        writefile.write(outline +'\n')
                writefile.close()
    
    def _dealPssmfrequency(self,lines,position):
        '''Calculate the evolutionary conservation of an amino acid
            @return: the evolutionary conservation of an amino acid
            @param lines:the lines of pssmFile
            position: the residue position in pssmFile 
        '''   
        ele1 = str((round((int(lines[position])/100),2)))
        if len(ele1) == 4:
            ele =ele1
        elif len(ele1) == 1 :  
            ele = ele1 +'.00'
        else:
            ele = ele1 +'0'
        return ele 
    
def main():
    _DealPSSM = DealPSSM()
    _DealPSSM._dealPssmFile('/home/yangyn533/tool/psiblastResult/pssm')
if  __name__ == '__main__' :
    main()    
