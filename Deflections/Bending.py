if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
import numpy as np
import matplotlib.pyplot as plt
from Deflections.wingbox import wingbox

#Function to calculate the chord at an arbitrary spanwise location z
'z - spanwise location'
'c_r - root chord'
'tr - taper ratio'
'b - wingspan'
def chord(z, c_r, tr, b):
    c = c_r - c_r * (1 - tr) * (z / (b/2))
    return c 