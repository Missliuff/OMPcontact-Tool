import xlrd
import pickle

data=xlrd.open_workbook('C:\\Users\\Administrator\\Desktop\\data.xls')
table=data.sheets()[0]
num_rows = table.nrows
interface = {}
for curr in range(1,num_rows):
    row=table.row_values(curr)
    partone = row[1].split('_')[0]
    parttwo = row[2]
    proteinid = partone + '_' + parttwo
    if proteinid not in interface.keys():
        interface[proteinid] = {}
    #if row[4] == 1.0:
    #print(row[3])
    resid = int(row[3])-1
    interface[proteinid][str(resid).split('.')[0]] = {'surface':str(row[4]).split('.')[0],'interface':str(row[5]).split('.')[0]}
#print(interface)
picklefile = open('C:\\Users\\Administrator\\Desktop\\data.pickle','wb')
pickle.dump(interface,picklefile)