import pandas as pd
import os
#TODO create a file with this python code in the computer and put there the aircraft data and then write it below to import from excel

aircraftDataExcelPath = os.path.join(os.getcwd(), 'aircraftReferenceData.xlsx')
aircraftDataFrame = pd.read_excel(aircraftDataExcelPath)

if __name__ == "__main__":
    print(aircraftDataFrame)