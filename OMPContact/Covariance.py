import os
import sys
import linecache
import numpy as np

class Get_Covariance():
    
    _mviewoutOriginal = []
    _mviewoutFormat = []
    _covarianceInputFormat = []
    _covarianceResult = []
    _zscoreList = []    
    
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
            
    def _runMView(self,MViewInputPath):
        ''' Use MView tool to deal multiple alignment results
            @return: None
        '''                 
        MViewInputlist=os.listdir(MViewInputPath)
        for each in MViewInputlist:
            WholePath = MViewInputPath + '/'+each
            pdbid = each.split('.')[0]
            cmd = '/home/ThirdPartTools/mview-1.61/bin/mview -in blast -out fasta '+ WholePath +' > /home/yangyn533/tool/mviewout/original/'+pdbid+'.aln.fasta'
            os.system(cmd) 
            self._mviewoutOriginal.append('/home/yangyn533/tool/mviewout/original/'+pdbid+'.aln.fasta')
            
    def _convertMViewFormat(self):
    
        for each_item in self._mviewoutOriginal:
            mviewoutFileLines = self._loadFile(each_item)
            mviewoutCount=len(mviewoutFileLines)            
            i=0
            pdbid = each_item[-16:-10]
            mviewoutformatFile = open('//home//yangyn533//tool//mviewout//format//'+pdbid+'.aln.fasta','w')
            while i < mviewoutCount:
                if i==mviewoutCount-1:
                    mviewoutformatFile.write(mviewoutFileLines[i])
                else:
                    if mviewoutFileLines[i][0]!='>' and mviewoutFileLines[i+1][0]!='>':
                        newline = mviewoutFileLines[i].replace('\n','')
                        mviewoutFileLines[i] = newline 
                    mviewoutformatFile.write(mviewoutFileLines[i])
                i=i+1
            mviewoutformatFile.close()
            self._mviewoutFormat.append('/home/yangyn533/tool/mviewout/format/'+pdbid+'.aln.fasta')            
            
    def _convertCovarianceInputFormat(self):
        ''' Convert MView tool output format for the next covariance predict
             @return: None
         '''              
        for each_item in self._mviewoutFormat:
            newfilename = '/home/yangyn533/tool/covariance/input/' + each_item[-16:-10]  + '.txt'
            filelines = self._loadFile(each_item)
            count = 0
            outline = ''
            try:
                outfile = open(newfilename,'w+')
                for line in filelines:
                    count = count + 1
                    if count >2:
                        if line[0] == '>':
                            outline = line[1:].split()[0]
                        else:
                            outline = outline + '        ' + line          
                            outfile.write(outline)
                outfile.close()
                self._covarianceInputFormat.append(newfilename)
            except:
                print(each_item)   
                
    def _runCovariance(self,methodFlag):
        ''' Use Covariance tool to predict 
            @return: None
            @param methodFlag: one Covariance method's name 
        '''          
        for each_item in self._covarianceInputFormat:  
            outfile = '//home//yangyn533//tool//covariance//' +methodFlag+"//"+each_item[-10:-4] + '.txt'
            cmd='java covariance.algorithms.'+methodFlag+'Covariance ' + each_item  + ' ' + outfile
            os.system(cmd)        
            self._covarianceResult.append(outfile)   
                       
    def _zscore(self,methodFlag):
        ''' For output standard 
            @return: None
            @param methodFlag: one Covariance method's name 
        '''         
        for each_item in self._covarianceResult:
            meannum,stdnum = self._getCalculationParameters(each_item)
            outfile = '//home//yangyn533//tool//covariance//zscore//'+methodFlag+"//" + each_item[-10:-4] +'_zscore.txt' 
            writefile = open(outfile,'w+')
            covariancelines = self._loadFile(each_item)
            for linenum in range(len(covariancelines)):
                if linenum==0:
                    outline = covariancelines[0].replace('\n','')
                else:
                    zscore = str((float(covariancelines[linenum].split()[2]) - meannum )/ stdnum)
                    outline = str(covariancelines[linenum].split()[0])+ ' ' + str(covariancelines[linenum].split()[1]) + ' ' +zscore
                writefile.write(outline +'\n')
            writefile.close()
            self._zscoreList.append(outfile)

    def _getCalculationParameters(self,covarianceFile):
        ''' Auxiliary calculation for zscore
            @return: None
            @param covarianceFile: the file which need to standard 
        '''         
        covariancescore = []
        covarianceLines = self._loadFile(covarianceFile)
        for linenum in range(1,len(covarianceLines)):
            covariancescore.append(float(covarianceLines[linenum].split()[2]))
        numarray = np.array(covariancescore)
        meannum = np.mean(numarray)
        stdnum = np.std(numarray)
        return meannum,stdnum

def main():
    _Get_Covariance = Get_Covariance()
    _Get_Covariance._runMView('/home/yangyn533/tool/psiblastResult/out')
    _Get_Covariance._convertMViewFormat()
    _Get_Covariance._convertCovarianceInputFormat()
    _Get_Covariance._runCovariance('MI')
    _Get_Covariance._zscore('MI')
if  __name__ == '__main__' :
    main()    
    
        