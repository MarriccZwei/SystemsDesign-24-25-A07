if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING

import OOP.Cell as cell
from typing import List
'''Here will be the function that will call the functions analysing the cell structure 
for different stresses and create the margin factor analysis in every block'''

def loadsInCells(cells:List[cell.Cell], plot=False):
    '''returns a list of margin factors for every load type for every cell, starting spanwise, syntax:
    [{"stress1": margin factor, "stress2": mf, etc.}, {"stress1": margin factor, "stress2": mf, etc.}]'''
    pass