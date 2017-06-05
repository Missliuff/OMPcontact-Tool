import linecache
import os
filelist=[]
for root,dirs,files in os.walk('/home/songjz671/covarianceout/mcbasc'):
    for file in files:
        filelist.append(os.path.join(root,file))
for each in filelist:
    filename=each.split('/')[-1]
    a=linecache.getlines(each)
    pointresult={}
    for i in range(1,len(a)):
        part1 = a[i].split()[0]
        part2 = a[i].split()[1]
        if part1 not in pointresult.keys():
            pointresult[part1] = 0
        if part2 not in pointresult.keys():
            pointresult[part2] = 0    
    num = len(pointresult.keys()) - 1
    for each_itme in pointresult.keys():
        for each_one in range(1,len(a)):
            partone = a[each_one].split()[0]
            parttwo = a[each_one].split()[1]
            if each_itme == partone or each_itme == parttwo:
                pointresult[each_itme] = pointresult[each_itme] + float(a[each_one].split()[2])
        pointresult[each_itme] = pointresult[each_itme] / num
    print(pointresult)
    result=sorted(pointresult.items(), key=lambda d:d[1], reverse = True)
    f=open('/home/songjz671/covarianceparser/mcbasc/'+filename,'w')
    for key,value in result:
        f.write(key)
        f.write('\n')
        f.write(str(value))
        f.write('\n')
    f.close