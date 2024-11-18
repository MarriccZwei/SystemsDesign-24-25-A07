import numpy as np

'''A class that provides the internal shear, normal, bending and torsion diagrams, 
the __init__ attributes are assumptions and settings, the method arguments are the loads'''
'''Contrary to the name, due to simplifications from Manual Appendix A.3, it also generates axial force,
because the engines are angled to account for removing speed'''

'''How To use: In general the class assumes a CANTILEVER element the position is zero at the fixed end, maximum at the free end'''

class SBTdiagramMaker(object):
    def __init__(self, accuracy=100, plot=False):
        self.accuracy = accuracy #into how many control points the length of the element is divided
        self.plot = plot #will the diagram actually be plotted or will only the wing loadings be provided

    #distrLoads is a function of position, pointLoads are stored in a list of tuples (position, magnitude)
    def axial_diagram(self, distrLoad, pointLoad, length):
        '''Generates the internal axial force diagram, as two numpy arrays, 
        one with the steps along the length of the element, 
        the other with the internal axial force value at those steps'''
    
    #distrLoads is a function of position, pointLoads are stored in a list of tuples (position, magnitude)
    def shear_diagram(self, distrLoad, pointLoads, length):
        '''Generates the internal shear force diagram, as two numpy arrays, 
        one with the steps along the length of the element, 
        the other with the internal shear force value at those steps'''

    #distrLoads is a function of position, pointLoads are stored in a list of tuples (position, magnitude)
    #distrMoment is a function of position, pointMoments are a stored in a list of tuples (position, magnitude) 
    def bending_diagram(self, distrLoad, pointLoad, distrMoment, pointMoments, length):
        '''Generates the internal bending moment diagram, as two numpy arrays,
        one with the steps along the length of the element, 
        the other with the internal bending moment value at those steps'''

    #distrLoads is a function of position, pointLoads are stored in a list of tuples (position, magnitude)
    def torque_diagram(self, distrTorque, pointTorques, length):
        '''Generates the internal torque diagram, as two numpy arrays,
        one with the steps along the length of the element, 
        the other with the internal torque value at those steps'''

    #distr is a function of position, points are stored in a list of tuples (position, magnitude)
    #!The input is assumed to follow a sign convention for the right type of load!
    def _general_diagram(self, distr, points, length):
        '''Generates a diagram of any "distribution plus point oad load"
        by the method of superposition, as two numpy arrays,
        one with the steps along the length of the element, 
        the other with the internal torque value at those steps'''

        #points along the length for which the internal load will be evaluated
        lenPts = np.linspace(0, length, self.accuracy+1)

        #the array that will contain the internal loads at the point from lenPts
        loadVals = np.zeros(self.accuracy+1)

        #the distributed load
        for i in range(self.accuracy+2):
            position = length - i #as mentioned in the class

        return lenPts, loadVals

