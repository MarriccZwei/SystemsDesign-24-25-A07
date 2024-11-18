# SystemsDesign-24-25-A07
code for the project estimations

# Work Package 4 code:
Loads/:
    SBTdiagrams.py - a class that can generate said diagrams both as numpy arrays and in a graphical way
    XFLRimport.py - a file imoprting data from XFLR 5
    InertialLoads.py - a file allowing for estimating inertial loads such as wing mass and bending relief
    CriticalLoads.py - a file finding the critical loads, using the other modules
Deflections/
    MoI.py - a file with moment of inertia estimations
    TorsionalStiffness.py - a file with torsional stiffness estimations
    Bending.py - a file analysing the bending deflection given MoI
    Twist.py - a file analasying the twisting given Torsional Constant
VnDiagram/
    graph.py - the file when the graph will actually get plotted