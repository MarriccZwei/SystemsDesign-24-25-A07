import json
import os
import pandas as pd
import math 

maindata = json.load(open("Protocols/main.json"))

def readExcelFile():
    cpDataExcelPath = os.path.join(os.getcwd(), 'cpAirfoil.xlsx')
    cpDataFrame = pd.read_excel(cpDataExcelPath)
    return cpDataFrame

#minCp = -1.5
sweepLE = maindata["sweepLE"]
mCr = maindata['Mcruise'] + 0.03

reynolds = '9e+06'
alpha = '4.80'
df = readExcelFile()
print(df)

column = f'NACA 64A210-Re=   {reynolds}-Alpha= {alpha}-NCrit=  9.0-XTrTop=0.007-XtrBot=0.751'
cpList = df[column].tolist()
cpList.sort()
cpMin = cpList[0]

print(cpMin)
cpR = 1-(1/(mCr*math.cos(sweepLE)))**2
crM = 1/(math.sqrt(1-cpMin)*math.cos(sweepLE))
print(crM)
