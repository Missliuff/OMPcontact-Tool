import linecache
import os
import pickle
import xlwt

picklefile = open('/home/songjz671/covariancesurfaceout/surface.pickle','rb')
surface = pickle.load(picklefile)
#print(surface)
#print(surface['1ACB_E'])
elscsurface = {}
filelist=[]
for root,dirs,files in os.walk('/home/songjz671/covarianceout/elsc'):
    for file in files:
        filelist.append(os.path.join(root,file))
for each in filelist:
    w=xlwt.Workbook()
    ws = w.add_sheet('covariance')    
    filename=each.split('/')[-1]
    proteinid = filename.split('.')[0]
    a=linecache.getlines(each)
    pointresult={}
    surfaceresult={}
    for i in range(1,len(a)):
        part1 = a[i].split()[0]
        part2 = a[i].split()[1]
        if part1 not in pointresult.keys():
            pointresult[part1] = 0
        if part2 not in pointresult.keys():
            pointresult[part2] = 0    
    num = len(pointresult.keys()) - 1
    for each_item in pointresult.keys():
        for each_one in range(1,len(a)):
            partone = a[each_one].split()[0]
            parttwo = a[each_one].split()[1]
            if each_item == partone or each_item == parttwo:
                pointresult[each_item] = pointresult[each_item] + float(a[each_one].split()[2])
        pointresult[each_item] = pointresult[each_item] / num
        #if each_item not in surface[proteinid]:
            #del pointresult[each_item]
    try:
        for eachsurface in surface[proteinid]:
            try:
                surfaceresult[eachsurface] = pointresult[eachsurface]
            except:
                print('no this site:'+proteinid+' '+eachsurface)
    except:
        print('no this file:'+proteinid)
    elscsurface[proteinid] = surfaceresult
    '''
    result=sorted(surfaceresult.items(), key=lambda d:d[1], reverse = True)
    row = 0
    for key,value in result:
        ws.write(row,0,key)
        ws.write(row,1,value)
        row = row + 1
    w.save('/home/songjz671/covariancesurfaceout/elsc/'+proteinid+'.xls')    
    #print(pointresult)
    '''
#print(elscsurface)
outfile=open('/home/songjz671/covariancesurfaceout/elscsurface.pickle','wb')
pickle.dump(elscsurface,outfile)

