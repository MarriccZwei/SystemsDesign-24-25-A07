# SystemsDesign-24-25-A07
code for the project estimations

# Work Package 4 code:
Loads/:
    SBTdiagrams.py - a class that can generate said diagrams both as numpy arrays and in a graphical way
    XFLRimport.py - a file imoprting data from XFLR 5
    InertialLoads.py - a file allowing for estimating inertial loads such as wing mass and bending relief
    CriticalLoads.py - a file finding the critical loads, using the other modules
    WingSBT.py - a file containing functions that combine the loads applied to the wing for the urpose of creating the SBT diagram.
Deflections/
    MoI.py - a file with moment of inertia estimations
        - centroid function returns centroid coordinates w.r.t the left upper corner of the wingbox
        - MOI function return the moments of inertia about the centroid of the wingbox
    wingbox.py - a file with the definition of the wingbox
        - wingbox function returns latice points of the wingbox in wrong coordinate system
    TorsionalStiffness.py - a file with torsional stiffness estimations
    MoISpnawise.py - a file producing the moments of inertia graph
    Twist.py - a file analasying the twisting given Torsional Constant
VnDiagram/
    graph.py - the file when the graph will actually get plotted