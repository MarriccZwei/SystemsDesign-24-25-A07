import sys
import os
import pandas as pd
sys.path.insert(1, os.getcwd())



# When given fileName of excel returns pandas dataframe of given file
def readExcelFile(fileName):
    absolutePath = os.path.join(os.getcwd(), fileName)
    dataFrame = pd.read_excel(absolutePath)
    return dataFrame