import os
import pandas as pd
from math import tan
from OOP.Planform import Planform
from scipy.interpolate import interp1d

# When given fileName of excel returns pandas dataframe of given file
def readExcelFile(fileName):
    absolutePath = os.path.join(os.getcwd(), fileName)
    dataFrame = pd.read_excel(absolutePath)
    return dataFrame

def partialSurface(a, planform: Planform):
    area = (a*tan(planform.sweep_at_c_fraction(1))+planform.cr)*a-0.5*a**2*tan(planform.sweep_at_c_fraction(1))-0.5*a**2*tan(planform.sweepLE)
    return area

def sparHeight(upperCoords, lowerCoords, sparLoc) -> list:
    interpUpper = interp1d(upperCoords[0], upperCoords[1], bounds_error=False, fill_value="extrapolate")
    interpLower = interp1d(lowerCoords[0], lowerCoords[1], bounds_error=False, fill_value="extrapolate")
    coords = [[sparLoc, sparLoc], [float(interpUpper(sparLoc)), float(interpLower(sparLoc))]]
    return coords

def length(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5