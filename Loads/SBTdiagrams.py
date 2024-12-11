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
    def axial_diagram(self, distrLoad, pointLoads, length):
        '''Generates the internal axial force diagram, as two numpy arrays, 
        one with the steps along the length of the element, 
        the other with the internal axial force value at those steps'''
        lenPts, loadVals = self._general_diagram(distrLoad, pointLoads, length)
        self._general_plot(lenPts, loadVals, "Internal axial force (in the sweep direction)", "A_z [N]")
        return lenPts, loadVals
    
    #distrLoads is a function of position, pointLoads are stored in a list of tuples (position, magnitude)
    def shear_diagram(self, distrLoad, pointLoads, length):
        '''Generates the internal shear force diagram, as two numpy arrays, 
        one with the steps along the length of the element, 
        the other with the internal shear force value at those steps'''
        lenPts, loadVals = self._general_diagram(distrLoad, pointLoads, length)
        self._general_plot(lenPts, loadVals, "Internal Shear Force (Upward Positive)", "V_y [N]")
        return lenPts, loadVals

    #distrLoads is a function of position, pointLoads are stored in a list of tuples (position, magnitude)
    #distrMoment is a function of position, pointMoments are a stored in a list of tuples (position, magnitude) 
    def bending_diagram(self, distrLoad, pointLoads, distrMoment, pointMoments, length):
        '''Generates the internal bending moment diagram, as two numpy arrays,
        one with the steps along the length of the element, 
        the other with the internal bending moment value at those steps'''
        #internal bending due to pure bending
        lenPts, loadVals = self._general_diagram(distrMoment, pointMoments, length)

        #shear diagram
        lenPts, shearVals = self._general_diagram(distrLoad, pointLoads, length)

        #integrating the shear diagram
        dl = length/self.accuracy #the length element for integrating the load
        intBdueToDistrS = 0 #internal bending due to internal shear
        #as mentioned in the class description, we count position from the root. 
        #Here dM/dx = V, so we do shouldn't invert the positions
        #yet we do it, because then our bending will start from zero and end at non-zero 
        #(and be zeroed by the cantilever reaction force)
        for i in reversed(range(self.accuracy+1)):
            intBdueToDistrS -= shearVals[i]*dl #numerical integration of the distr load
            #due to it being cantilever, the integration constants for applied loads will be 0.

            #updating the corresponding field in loadVals
            loadVals[i] += intBdueToDistrS

        #auto_plotting afterwards
        self._general_plot(lenPts, loadVals, "Internal Bending Moment (Positive in Flight Direction)", "M_x [Nm]")
        return lenPts, loadVals

    #distrLoads is a function of position, pointLoads are stored in a list of tuples (position, magnitude)
    def torque_diagram(self, distrTorque, pointTorques, length):
        '''Generates the internal torque diagram, as two numpy arrays,
        one with the steps along the length of the element, 
        the other with the internal torque value at those steps'''
        lenPts, loadVals = self._general_diagram(distrTorque, pointTorques, length)
        self._general_plot(lenPts, loadVals, "Internal Torque (Pitch down positive)", "T_z [Nm]")
        return lenPts, loadVals

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
            position = length*(1 - i/self.accuracy)
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
    
    #intForceTitle, stating the internal force with the relevant assumption (e.g. which of the two shear forces)
    #intforceLabel, axis label following a format of: "<internal force symbol> [<unit>]"
    def _general_plot(self, lenPts, loadVals, intForceTitle, intForceLabel):
        '''A plotting subfunctioon that allows to visualize the diagram when the settings indicate that'''
        if self.plot:
            plt.plot(lenPts, loadVals)
            plt.xlabel("Spanwise Position [m] (0 at the wing root)")
            plt.ylabel(intForceLabel)
            plt.title(intForceTitle)
            plt.show()

if __name__ == "__main__":
    class TestSBTdiagrams(unittest.TestCase):
        def test_shearBendingDiagram(self):
            zeroIntLoad = lambda pos:0
            linearIntLoad = lambda pos:0.2

            def appl_load(pos): #constant applied load of 2N/m from 5m to 10m
                if 5<pos and pos<10:
                    return 2
                else:
                    return 0
                
            def appl_moment(pos): #constant applied load of 2N/m from 15m to 20m
                if 15<pos and pos<20:
                    return 4
                else:
                    return 0

            length = 20 # to have sth easy to everse engineer, but affecting the result, in the right order of magnitude
            pointForces = [(15, 10)]
            maker = SBTdiagramMaker(accuracy = 50, plot=False) #we want to plot
            lenPts, loadVals = maker.shear_diagram(appl_load, pointForces, length)

            #to see if there is no information distortion
            plt.plot(lenPts, loadVals)
            plt.show()

            lenPts, loadVals = maker.bending_diagram(appl_load, pointForces, appl_moment, [(10, -50)], length)

        def test_torque_diagrams(self):
            maker = SBTdiagramMaker(accuracy = 50, plot=True) #we want to plot
            lenPts, loadVals = maker.torque_diagram(lambda x:0, [(.3, -15), (.5, 10)], 0.5)

    unittest.main()