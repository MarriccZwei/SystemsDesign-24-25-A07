if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
import EvalWgbox.iterationFuns as iterfuns
import OOP.Wingbox as wb
import OOP.Planform as pf
import numpy as np

#sizing the mid spar less wingbox
planform =pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
halfspan = planform.b/2
mWing = 22962.839350654576
mEngine = 3554.759960907367/2 #divide by two as we are looking at the half-span only
thrust = 91964.80101516769
wgboxArea = 123.969 #[m^2] measured in CATIA

#no reinforcement spar wingbox
# wgBoxInitial = wb.Wingbox(0.001, 0.001, 0.01, 0.002, planform)
# wgBoxFinal = iterfuns.size_rectbox(wgBoxInitial, 0.15*planform.b, np.radians(10), 0.01, planform, mWing, mEngine, wgboxArea, thrust)
# print(f"No reinf. Spars wingbox, stiffener area: {wgBoxFinal.stiffArea}, spar thickness: {wgBoxFinal.tSpar}, skin thickness: {wgBoxFinal.tSkin}")

#reinforcement wingspar-variable cutoff
# wgBoxInitial = wb.Wingbox(0.001, 0.001*2/3, 0.001*2/3, 0.002, planform, midSpar=True, midSparPos=0.4, cutMidSpar=1)
# wgBoxFinal = iterfuns.size_constbox(wgBoxInitial, 0.15*planform.b, np.radians(10), 0.01, planform, mWing, mEngine, wgboxArea, thrust)
# print(f"No reinf. Spars wingbox, stiffener area: {wgBoxFinal.stiffArea}, spar thickness: {wgBoxFinal.tSpar}, skin thickness: {wgBoxFinal.tSkin}, cutoff pos: {wgBoxFinal.cutoff}")

#reinforcement wingspar - no cutoff
# wgBoxInitial = wb.Wingbox(0.001, 0.001, 0.001, 0.002, planform, midSpar=True, midSparPos=0.4, cutMidSpar=0.3*planform.b/2)
# wgBoxFinal = iterfuns.size_complexbox(wgBoxInitial, 0.15*planform.b, np.radians(10), 0.01, planform, mWing, mEngine, wgboxArea, thrust)
# print(f"No reinf. Spars wingbox, stiffener area: {wgBoxFinal.stiffArea}, spar thickness: {wgBoxFinal.tSpar}, skin thickness: {wgBoxFinal.tSkin}, cutoff pos: {wgBoxFinal.cutoff}")

#no reinforcement spar wingbox
wgBoxInitial = wb.Wingbox(0.001, 0.001, 0.01, 0.001, planform)
wgBoxFinal = iterfuns.size_rectbox(wgBoxInitial, 0.15*planform.b, np.radians(10), 0.001, planform, mWing, mEngine, wgboxArea, thrust)
print(f"No reinf. Spars wingbox, stiffener area: {wgBoxFinal.stiffArea}, spar thickness: {wgBoxFinal.tSpar}, skin thickness: {wgBoxFinal.tSkin}")