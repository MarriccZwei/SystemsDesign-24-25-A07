if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
from Deflections.wingbox import wingbox

chord = 8.14
upperCoords, lowerCoords = wingbox(chord, plot=True)
points = list(zip(upperCoords[0],upperCoords[1]))
print(points)


