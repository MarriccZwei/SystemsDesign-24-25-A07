import numpy as np
import unittest
import matplotlib.pyplot as plt

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

        dl = length/self.accuracy #the length element for integrating the load

        #the distributed load
        intLoadDueToDistr = 0 #internal load due to distributed load
        for i in range(self.accuracy+1):
            #as mentioned in the class description, we count position from the root. 
            #Yet, we have to start internal force buil-up from the tip
            position = length - i/self.accuracy
            intLoadDueToDistr += distr(position)*dl #numerical integration of the distr load
            #due to it being cantilever, the integration constants for applied loads will be 0.

            #updating the corresponding field in loadVals
            loadVals[self.accuracy-i] += intLoadDueToDistr

        #the point loads
        for pointLoad in points:
            #we add the point load only to positions before where the point load is applied.
            #self.accuracy*pointLoad[0]/length gives the index at which the point load should end working, right?
            for i in range(int(np.round(self.accuracy*pointLoad[0]/length))):
                loadVals[i]+=pointLoad[1]

        return lenPts, loadVals

if __name__ == "__main__":
    class TestSBTdiagrams(unittest.TestCase):
        def test_generalDiagram(self):
            zeroIntLoad = lambda pos:0
            linearIntLoad = lambda pos:0.2
            length = 50 # to have sth easy to everse engineer, but affecting the result, in the right order of magnitude
            pointForces = [(0, 2), (21, 37), (13, 15)]
            maker = SBTdiagramMaker(accuracy = 50) #default settings, but low accuracy so that it is visible
            lenPts, loadVals = maker._general_diagram(zeroIntLoad, pointForces, length)
            plt.plot(lenPts, loadVals)
            plt.show()
            lenPts, loadVals = maker._general_diagram(linearIntLoad, [], length)
            plt.plot(lenPts, loadVals)
            plt.show()
            lenPts, loadVals = maker._general_diagram(linearIntLoad, pointForces, length)
            plt.plot(lenPts, loadVals)
            plt.show()

    unittest.main()