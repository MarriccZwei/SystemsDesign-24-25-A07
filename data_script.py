import pandas as pd
import os

g = 9.81

def readExcelFile():
    aircraftDataExcelPath = os.path.join(os.getcwd(), 'aircraftReferenceData.xlsx')
    aircraftDataFrame = pd.read_excel(aircraftDataExcelPath)
    return aircraftDataFrame

def generateLoadingPoints():
    pointList = []
    df = readExcelFile()
    MTOWList = df['MTOW(kg)'].tolist()
    trustList = df['Thrust (kN)'].tolist()
    wingAreaList = df['Wing Area'].to_list()
    aircraftList = df['Aircraft'].to_list()
    for idx, aircraft in enumerate(aircraftList):
        wingLoading = (MTOWList[idx] * g)/wingAreaList[idx]
        trustRatio = (trustList[idx]*1000)/(MTOWList[idx] * g)
        dataPoint = [wingLoading, trustRatio, aircraft]
        pointList.append(dataPoint)
    return(pointList)

if __name__ == "__main__":
    print(generateLoadingPoints())