import OOP.Planform as pf
from typing import Dict

class Cell:
    '''The representation of the wingbox between 2 ribs'''
    #startPos, endPos - spanwise location [m] from root, stringerDesign: the design decisions of the stringers, as a dict
    #wgboxThicknesses: the 'f', 'm', 'r', ... dict for 
    def __init__(planform:pf.Planform, startPos:float, endPos:float, stringerDesign:Dict[str:float], wgboxThicknesses:Dict[str:float]):
        pass
