'''
Created on 2015-11-20

@author: Administrator
'''
import os
import sys

class Covariance():
    _covMatrix = {}
    _coor = {}
    _num = '0'
    def loadCovariance(self,fileName):
        '''functon for load Covariance file,if file exists, return True, else return False.
        @param filepath :string ,path of the file
        @return: If successfully loaded, return True,else return False.
        '''
        try :
            if os.path.exists(fileName) :
                for line in open(fileName,'r').readlines() :
                    if line.split()[0] != 'i' :
                        if line.split()[0] == self._num :
                            self._coor[line.split()[1]] = line.split()[2]
                            self._num = line.split()[0]
                        else :
                            self._covMatrix[self._num] = self._coor
                            self._num = line.split()[0]
                            self._coor={}
                            self._coor[line.split()[1]] = line.split()[2]
                self._covMatrix[self._num] = self._coor
                
                return True
            else :
                return False
        except :
            return False
                    
    def getCovariance(self,pos1,pos2):
        ''' function for get covariance value,
        @param pos1,pos2 :int,the coordination of residue,0 begin.
        @return: the value of the covariance between pos1 and pos2,if error,return -1.
        '''
        try :
            return self._covMatrix[str(pos1)][str(pos2)]
        except :
            return -1
        
class PSSM():
    _pssmMatrix = {}
    _coor = {}
    _residueorder = {     'L':10,
                          'V':19,
                          'I':9,
                          'F':13,
                          'M':12,
                          'W':17,
                          'C':4,
                          'A':0,
                          'G':7,
                          'T':16,
                          'Y':18,
                          'H':8,
                          'K':11,
                          'S':15,
                          'P':14,
                          'N':2,
                          'R':1,
                          'E':6,
                          'Q':5,
                          'D':3}
    def loadPSSM(self,fileName) :
        '''functon for load PSSM file,if file exists, return True, else return False.
        @param fileName :string ,path of the file
        @return: If successfully loaded, return True,else return False.
        '''
        linenum = 0
        try :
            if os.path.exists(fileName) :
                for line in open(fileName,'r').readlines() :
                    for i in range(0,len(line.split())) :
                        self._coor[str(i)] = line.split()[i]
                    self._pssmMatrix[str(linenum)] = self._coor
                    linenum += 1
                    self._coor = {}
                
                return True
            else :
                return False
        except :
            return False
                    
    def getFrequency(self,pos,residue):
        ''' function for get frequency value,
        @param pos:int,the coordination of residue,0 begin.
        @param rsidue:string,residue name,one letter residue.
        @return: the value of frequency.if error,return -1.
        '''
        try :
            if type(pos) == int and residue in self._residueorder.keys() :
                return self._pssmMatrix[str(pos)][str(self._residueorder[residue])]
            else :
                return -1
        except :
            return -1        
        
        
class Topology():
    _topology = ''
    def loadTopology(self,fileName):
        '''functon for load Topology file,if file exists, return True, else return False.
        @param filepath :string ,path of the file
        '''
        j = False
        if os.path.exists(fileName) :
            for line in open(fileName).readlines() :
                for i in range(0,len(line)-1) :
                    if line[i:i+1] != 'i' and line [i:i+1] != 'o' and line[i:i+1] != 'T' :
                        j = True
            if j :
                return False
            else :
                for line in open(fileName).readlines(): 
                    self._topology += line[0:len(line)-1]
                return True    
            
    def getTopologyType(self,pos):
        ''' function for get type of Topology,i,o--0,T--1.
        @param pos :int,the coordination of residue,0 begin
        '''
        sequence = self._topology
        if sequence == '' :
            return -1

        if type(pos) == int and pos in range(0,len(sequence)) :
            if sequence[pos:pos+1] == 'T' :
                return 1
            else :
                return 0
        else :
            return -1

    def getTopology(self):
        ''' function for get Topology sequence.
        '''
        if self._topology == '' :
            return -1
        return self._topology


class RelativeSeqPos():
    _topomatrix = {}
    _toposeq = ''
    _booltopo = True
    def LoadTopology(self,topoSeq): 
            '''functon for load Topology.
            @param topolSeq :string ,topology sequence of the protein file.
            '''
            for i in range(0,len(topoSeq)) :
                if topoSeq[i:i+1]  in ['i','o','T'] :
                    continue
                else :
                    self._booltopo = False

            if self._booltopo :
                self._toposeq = topoSeq
                j = 0
                h = 0
                for i in range(0,len(self._toposeq)) :
                    if self._toposeq[i:i+1] != 'T' :
                        self._topomatrix[str(i)] = 0
                    elif self._toposeq[i:i+1] == 'T' :
                        if self._toposeq[i+1:i+2] == 'T' :
                            j = j + 1
                        else :
                            j = j + 1
                            if h % 2 == 0 :
                                zero = 1
                                for l in range(i-j,i) :
                                    self._topomatrix[str(l+1)] = zero 
                                    zero += 1
                                h = h +1
                            else :
                                one = j
                                for l in range(i-j,i) :
                                    self._topomatrix[str(l+1)] = one
                                    one = one - 1
                                h = h + 1
                            j = 0
                return True
            else :
                return False
            
    def getReav(self,pos):
        ''' function for get relative position in topology sequence.
        @param pos : int,the relative position of the residue
        '''
        if str(pos) in self._topomatrix.keys() :
            return (self._topomatrix[str(pos)])
        else :
            return -1
        
        
class predict_data_generate():
    
    def __init__(self,primaryseqfile,topofile,covariancefile,pssmfile,predictfileout):
        '''@attention: generate a file used in svm-predict to predict
        @param primaryseqfile: str,The path of primary sequence file.
        @param topofile: str,The path of topology file.
        @param covariancefile: str,The covariance file path.
        @param pssmfile:str, The path of PSSM file.
        @param predictfileout:str,Out put file,used in svm-predict to predict.   
        '''
        try :
            self.primarysequences = open(primaryseqfile).readlines()
            self.topo = Topology()
            self.topo.loadTopology(topofile)

            self.covar = Covariance()
            self.covar.loadCovariance(covariancefile)

            self.pssm = PSSM()
            self.pssm.loadPSSM(pssmfile)
            self.predictfileout = predictfileout
            if self.topo.loadTopology(topofile) == 1 and self.covar.loadCovariance(covariancefile) ==1 and self.pssm.loadPSSM(pssmfile) ==1 :
                print ('Load file succeed')
            else :
                print ('Load file error')
                sys.exit(1)
        except Exception as ex :
            print (ex)
        
    def __getprimarysequence(self):
        f1 = self.primarysequences
        primaryseq = ''
        for line in f1 :
            if line[0:1] != '>' :
                if line[-1] == '\n':
                    primaryseq += line[:-1]
                else :
                    primaryseq += line    
        return primaryseq
        
    def __getposandresidue(self,pos1,pos2):
        f1 = self.primarysequences
        primaryseq = ''
        posone = []
        postwo = []
        for line in f1 :
            if line[0:1] != '>' :
                if line[-1] == '\n':
                    primaryseq += line[:-1]
                else :
                    primaryseq += line
        if int(pos1) == 0 and int(pos2) != len(primaryseq)-1 :
            posone.append({'0':primaryseq[0:1]})
            posone.append({'1':primaryseq[1:2]})
            posone.append({'2':primaryseq[2:3]})
            postwo.append({str(int(pos2)-1):primaryseq[int(pos2)-1:int(pos2)]})
            postwo.append({str(int(pos2)):primaryseq[int(pos2):int(pos2)+1]})
            postwo.append({str(int(pos2)+1):primaryseq[int(pos2)+1:int(pos2)+2]})
        elif int(pos2) == len(primaryseq)-1 and int(pos1) != 0:
            postwo.append({str(int(pos2)-2):primaryseq[int(pos2)-2:int(pos2)-1]})
            postwo.append({str(int(pos2)-1):primaryseq[int(pos2)-1:int(pos2)]})
            postwo.append({str(int(pos2)):primaryseq[-1]})
            posone.append({str(int(pos1)-1):primaryseq[int(pos1)-1:int(pos1)]})
            posone.append({str(int(pos1)):primaryseq[int(pos1):int(pos1)+1]})
            posone.append({str(int(pos1)+1):primaryseq[int(pos1)+1:int(pos1)+2]})
        elif int(pos2) == len(primaryseq)-1 and int(pos1) == 0:
            posone.append({'0':primaryseq[0:1]})
            posone.append({'1':primaryseq[1:2]})
            posone.append({'2':primaryseq[2:3]})
            postwo.append({str(int(pos2)-2):primaryseq[int(pos2)-2:int(pos2)-1]})
            postwo.append({str(int(pos2)-1):primaryseq[int(pos2)-1:int(pos2)]})
            postwo.append({str(int(pos2)):primaryseq[-1]})
        else :
            posone.append({str(int(pos1)-1):primaryseq[int(pos1)-1:int(pos1)]})
            posone.append({str(int(pos1)):primaryseq[int(pos1):int(pos1)+1]})
            posone.append({str(int(pos1)+1):primaryseq[int(pos1)+1:int(pos1)+2]})
            postwo.append({str(int(pos2)-1):primaryseq[int(pos2)-1:int(pos2)]})
            postwo.append({str(int(pos2)):primaryseq[int(pos2):int(pos2)+1]})
            postwo.append({str(int(pos2)+1):primaryseq[int(pos2)+1:int(pos2)+2]})
        return posone,postwo
        
    def __getCov(self,pos1,pos2):
        covnum = self.covar.getCovariance(pos1,pos2)
        return covnum
    
    def __getPSSM(self,residueList):
        feq = []
        for i in residueList :
            for key in i :
                feq.append(self.pssm.getFrequency(int(key), i[key]))
        return feq[0],feq[1],feq[2]
    
    def __getReSeqPos(self,pos):
        toposeq = self.topo.getTopology()
        reseqpos = RelativeSeqPos()
        reseqpos.LoadTopology(toposeq)
        relaseq = reseqpos.getReav(pos)
        return relaseq
    
    def __intopo(self,pos1,pos2):
        ''' function for judge whether two residue both in topology area.
            @param pos1,pos2 :the coordination of residue
        '''
        posone = self.topo.getTopologyType(pos1)
        postwo = self.topo.getTopologyType(pos2)
        if posone == 1 and postwo == 1 :
            return True
        else :
            return False
        
    
    def generate_predict_file(self):
        '''

        '''
        predictout = open(self.predictfileout,'wt')
        primaryseq = self.__getprimarysequence()
        for i in range(0,len(primaryseq)) :
            for j in range(0,len(primaryseq)) :
                if i < j :
                    if self.__intopo(i, j) :
                        
                        info = ''
                        aa,bb = self.__getposandresidue(i,j)
                        covnum = self.__getCov(i,j)
                        
                        
                        a0,a1,a2 = self.__getPSSM(aa)
                        b0,b1,b2 = self.__getPSSM(bb)
                        relativeseqa = self.__getReSeqPos(i)
                        relativeseqb = self.__getReSeqPos(j)
                        resseq = str(i)+str(j)+str(len(str(i)))
                        info += resseq+' 1:'+str(covnum)+' 2:'+str(a0)+' 3:'+str(a1)+' 4:'+str(a2)+' 5:'+str(b0)+' 6:'+str(b1)+' 7:'+str(b2)+' 8:'+str(relativeseqa)+' 9:'+str(relativeseqb) + '\n' 
                        predictout.write(info)
                    else :
                        pass
                    
        predictout.close()
        
        
def svmpredict(svmpredict_exe_path,modelpath,predictfile,svmpredictout,covariance_kind):
    '''@attention: Run svm-predict with OMPcantact.model to predict file
    @param svmpredict_exe_path: str,The all path of svm-predict in the system
    @param predictfile:str,Be predicted in svm-predict,generated by class predict_data_generate
    @param svmpredictout:str,svm-predict output file path.
    @param covariance_kind:Four kind of Covariance :EVFOLD,MI,ELSC,OMES '''
    try :
        #modelpath = os.getcwd()
        #modelfile = modelpath + '//OMPcontact'+covariance_kind+'.model'
        cmd = svmpredict_exe_path+' -b 1 '+predictfile+' '+modelpath +' '+svmpredictout
        os.system(cmd)
    except Exception as ex :
        print (ex)


'''
if  __name__ == '__main__' :
    def exit_with_help():
        print('Usage: OMPcontact.py [Primary sequence file] [Topology file] [PSSM file] [covariance file] [predict_exe file path] [svm-train file path] [svm-predict output file] [kind of covariance of Model file,MI,EVFOLD,ELSC,OMES]')
        sys.exit(1)

    if len(sys.argv) < 8:
        exit_with_help()
    primaryfile = sys.argv[1]
    topologyfile = sys.argv[2]
    covariancefile = sys.argv[3]
    pssmfile = sys.argv[4]
    predict_exefile = sys.argv[5]
    svmpath = sys.argv[6]
    outfile = sys.argv[7]
    covariance_kind = sys.argv[8]
    
    filegenerate = predict_data_generate(primaryfile,topologyfile,covariancefile,pssmfile,predict_exefile)
    filegenerate.generate_predict_file()
    
    svmpredict(svmpath,predict_exefile,outfile,covariance_kind)

#python OMPcontact.py //home//developer//OMPs//FASTA//2YNK.fasta //home//developer//OMPs//TOPOLOGY_BETAWARE//2YNK.txt //home//developer//OMPs//BLAST//PROF//2YNK.prof //home//developer//OMPs//COVARIANCE//ELSC//2YNK_zscore.txt //home//yl//OMPcontact//2YNK //home//ThirdPartTools//libsvm-3.20//svm-predict //home//yl//OMPcontact//2YNK.out
'''
if  __name__ == '__main__' :
    filegenerate = predict_data_generate('/home/yangyn533/tool/fastaparsed/1qj8.fasta','/home/yangyn533/tool/betaware/betawareSVMInput/1QJ8_A.parsed.out','/home/yangyn533/tool/covariance/MI/1QJ8_A.txt','/home/yangyn533/tool/profile/1QJ8_A.prof','/home/yangyn533/OMPContact/1qj8')
    filegenerate.generate_predict_file()
    svmpredict('svm-predict','/home/yangyn533/OMPContact/OMPcontactMI.model','/home/yangyn533/OMPContact/1qj8','/home/yangyn533/tool/1qj8.out','MI')
    

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        