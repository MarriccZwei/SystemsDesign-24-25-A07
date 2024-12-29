def MaxAxialStress(MomentX:float, MOIxx:float, MOIyy:float, MOIxy:float, FrontSparLen:float, CentroidX:float, Chord:float): 
    Y = FrontSparLen/2 #location of maximum axial stress will likely be at the front spar
    X = CentroidX*Chord
    Denominator = MOIxx*MOIyy - MOIxy**2
    MaxStress = MomentX*((MOIyy*Y - MOIxy*X)/(Denominator))

#