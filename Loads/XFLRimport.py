import numpy as np
import scipy as sp
from scipy import interpolate
import matplotlib.pyplot as plt

# File path
txt_a0 = "Loads\MainWing_a=0.00_v=10.00ms.txt"
txt_a10 = "Loads\MainWing_a=10.00_v=10.00ms.txt"

def filetolist(txt):
    # Load data, skipping the header and footer lines to extract the table
    data = np.genfromtxt(
    txt,
    skip_header=40,  # Skip the first 40 
    max_rows=19,     # max rows
    usecols=(0, 3, 5, 6)  # Columns: y, Cl, Cd, Cm
    )
    ylst = data[:, 0].tolist()
    Cllst = data[:, 1].tolist()
    Cdlst = data[:, 2].tolist()
    Cmlst = data[:, 3].tolist()
    return(ylst,Cllst,Cdlst,Cmlst)


def interpolate(ylst,cnst):
    f = sp.interpolate.interp1d(ylst,cnst,kind='cubic',fill_value="extrapolate")
    return(f)


# TEST TO PLOTTT
# step = 0.1
# ytab=[]
# cltab=[]

# for i in range(24):
#     cl = interpolate((filetolist(txt_a10)[0]),(filetolist(txt_a10)[1]))(i)
#     i = i + step

#     ytab.append(i)
#     cltab.append(cl)

# # Plot the sine and cosine lines in a graph
# plt.plot(ytab, cltab)

# plt.title('test')
# plt.xlabel('y')
# plt.ylabel('cl')    

# plt.show()


