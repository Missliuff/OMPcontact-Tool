import os
import linecache
from fastaparser import fastaparsermethod


class Blast():
    
    _psiblastOutList = []
    _psiblastPssmList = []

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
    
    def _runBlast(self,fastaOriginalPath,fastapath):
        ''' Use psiblast tool to get multiple alignment results 
            @return: None
            @param fastaFilefile: The full path of the fastaFile, str
        '''
        Fastafilelist=os.listdir(fastaOriginalPath)
        for each in Fastafilelist:
            wholepath=fastapath+'//'+each
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
                cmd='psiblast -evalue 10 -num_iterations 3 -db /home/songjz671/blast/db/uniprot -query /home/yangyn533/tool/experiment.fasta -outfmt 0 -out /home/yangyn533/tool/psiblastResult/out/'+pdbid+'.fm0 -out_ascii_pssm /home/yangyn533/tool/psiblastResult/pssm/'+pdbid+'.pssm -num_alignments 1500 -num_threads 48'
                os.system(cmd)                        
                #self._psiblastOutList.append('/home/yangyn533/tool/psiblastResult/out/'+pdbid+'.fm0')
                #self._psiblastPssmList.append('/home/yangyn533/tool/psiblastResult/pssm/'+pdbid+'.pssm')
                i=i+2
                
def main():
    _Blast= Blast()
    _Blast._runBlast('//home//yangyn533//tool//fastaOriginal','//home//yangyn533//tool//fastaparsed')
if  __name__ == '__main__' :
    main()    