import os
import pandas as pd
from math import tan
from OOP.Planform import Planform

# When given fileName of excel returns pandas dataframe of given file
def readExcelFile(fileName):
    absolutePath = os.path.join(os.getcwd(), fileName)
    dataFrame = pd.read_excel(absolutePath)
    return dataFrame

def partialSurface(a, planform: Planform):
    area = (a*tan(planform.sweep_at_c_fraction(1))+planform.cr)*a-0.5*a**2*tan(planform.sweep_at_c_fraction(1))-0.5*a**2*tan(planform.sweepLE)
    return area