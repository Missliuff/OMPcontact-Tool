import os
import xlrd
import xlwt
import pickle

picklefile = open('/home/songjz671/covariancesurfaceout/interface.pickle','rb')
interface = pickle.load(picklefile)
elscpicklefile = open('/home/songjz671/covariancesurfaceout/elscsurface.pickle','rb')
elscsurface = pickle.load(elscpicklefile)
mcbascpicklefile = open('/home/songjz671/covariancesurfaceout/mcbascsurface.pickle','rb')
mcbascsurface = pickle.load(mcbascpicklefile)
mipicklefile = open('/home/songjz671/covariancesurfaceout/misurface.pickle','rb')
misurface = pickle.load(mipicklefile)
omespicklefile = open('/home/songjz671/covariancesurfaceout/omessurface.pickle','rb')
omessurface = pickle.load(omespicklefile)
for eachprotein in elscsurface.keys():
    w=xlwt.Workbook()
    ws = w.add_sheet('Covariance')    
    row = 0
    for eachsurface in elscsurface[eachprotein].keys():
        try:
            ws.write(row,0,elscsurface[eachprotein][eachsurface])
            ws.write(row,1,mcbascsurface[eachprotein][eachsurface])
            ws.write(row,2,misurface[eachprotein][eachsurface])
            ws.write(row,3,omessurface[eachprotein][eachsurface])
            ws.write(row,4,interface[eachprotein][eachsurface]['interface'])
            row = row + 1
        except:
            print(eachprotein+'  '+eachsurface)
            continue
    w.save('/home/songjz671/covariancesurfaceout/covariancematrix/'+eachprotein+'.xls')

    