import os
import linecache


class fastaparsermethod():
    
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
            print('File error:'+err)    
        
    def _parser(self,fastaOriginalpath,parsedpath):
        ''' Open the file with the path
            @return: The true fasta format which can be used for ThirdPartTools
            @param file: The full path of the file, str
        ''' 
        Fastafilelist=os.listdir(fastaOriginalpath)
        for each in Fastafilelist:
            wholepath = fastaOriginalpath+'/'+each
            fastaID = wholepath.split('/')[-1]
            fastaFileLines = self._loadFile(wholepath)
            fastaFilecount = len(fastaFileLines)
            lines = linecache.getlines(wholepath)
            parsedFile = open(parsedpath+fastaID,'w')
            i = 0
            while i <= fastaFilecount-1:
                if i == fastaFilecount-1:
                    parsedFile.write(lines[i])
                    i = i+1
                elif lines[i][0] == '>' or lines[i+1][0] == '>':
                    parsedFile.write(lines[i])
                    i = i+1
                else:
                    newline = lines[i].replace('\n','').replace(' ','')
                    lines[i] = newline
                    parsedFile.write(lines[i])
                    i = i+1
            parsedFile.close()

def main():
    fastaparser=fastaparsermethod()
    fastaparser._parser('/home/yangyn533/tool/fastaOriginal','/home/yangyn533/tool/fastaparsed/')    
if __name__=="__main__":
    main()

        