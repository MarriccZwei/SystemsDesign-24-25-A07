if __name__ == "__main__":
    # ONLY FOR TESTING
    import sys
    import os
    sys.path.insert(1, os.getcwd())
    # ONLY FOR TESTING
    import matplotlib.pyplot
import CellAnaylysis.cellOperations as cop
import OOP.Planform as pf
import numpy as np
import General.Constants as c
import matplotlib.pyplot as plt
import OOP.Cell as cell
from typing import List

'''Planform Parameters from WP3'''
planform =pf.Planform(251.3429147793505, 9.872642920666417, 0.1, 28.503510117080133, 2.1496489882919865, False)
halfspan = planform.b/2
mWing = 22962.839350654576
mEngine = 3554.759960907367/2 #divide by two as we are looking at the half-span only
thrust = 91964.80101516769
wgboxArea = 123.969 #[m^2] measured in CATIA

'''Defining initial design parameters'''
plot = True #do we want to plot

"rib spacing"
#the rib stations required due to the subsystem presence - do not change!
#the 0.6 halfspan does not correspond to subsystem - it is there to model the point when skin buckling changes significance
#you can change 
ribStations = [0, 3.3, 3.9, 5.1, c.ENGINESPANWISEPOS*halfspan, 0.6*halfspan, 17.62, 17.92, 22.42, halfspan]

#change this, the columns left as zeros are there for a reason - the spacing between the enforced spars is just small.
ribBetweenCounts = [3, 0, 0, 1, 7, 3, 0, 6, 0] #amount of ribs between the ribs from ribStations

#generating rib positions
ribPoses = [0] #this is intentional to account for the rib at root
for i in range(len(ribBetweenCounts)):
    #+2 accounts for the first and the last rib, then the 1st rib is removed, so indeed you end up with 1 side rib plus the between rib count
    ribPoses+=np.linspace(ribStations[i], ribStations[i+1], ribBetweenCounts[i]+2).tolist()[1:]

midsCoffIdx = sum(ribBetweenCounts[:4])+5-1 #the selected and the enforced ribs up to the engine rib, -1 to account for indexing

"wingboxDesigns"
#design with index 0 is design option 1, etc.
stringerDesign = {'w':0.05, 'h':0.15, 't':0.007, 'sb':0.12, 'st':0.17}

print(f'Number of Ribs {2*len(ribPoses) - 1}')

#same indexing as stringerDesign
thicknesses = {'f':0.011, 'r':0.011, 'b':0.012, 't':0.012, 'm':0.01}

#mid spar persence and position
midSpar = None

'''Dividing the wing into the cells'''
cells = cop.cell_distr(planform, ribPoses
                        , stringerDesign, thicknesses, midsCoffIdx, midSpar)
margins_of_safety = cop.mofs(cells, plot=True)

#plotting mofs
if plot:
    ZposCell1 = margins_of_safety[0]  # cell start positions
    ZposCell = ZposCell1.copy()  # copy for adding last point
    ZposCell.append(halfspan)  # the last point tip

    # Wing geometry parameters
    root_chord = planform.cr
    tip_chord = planform.ct  # Tip chord length
    half_span = halfspan  # Half span of the wing
    sweep_angle_rad = planform.sweepLE  # Sweep angle in rads at leading
    TR = planform.TR

    # rip positions spanwise from code above
    rib_positions_spanwise = ribPoses

    #get chord at a given spanwise position
    def chord_at_span(span_pos):
        return root_chord - root_chord * (span_pos/halfspan) * (1-TR)

    quarter_chord_offset = 0.25 * root_chord

    #  get leading and trailing edge x-coordinates at a given spanwise position
    def leading_edge_x(span_pos):
        return np.tan(sweep_angle_rad) * span_pos - quarter_chord_offset #is good now

    def trailing_edge_x(span_pos):
        return leading_edge_x(span_pos) + chord_at_span(span_pos)


    # Plot wing outline
    span_positions = np.linspace(0, half_span, 100)
    leading_edge = [leading_edge_x(span) for span in span_positions]
    trailing_edge = [trailing_edge_x(span) for span in span_positions]

    plt.subplot(231)
    # Leading edge
    plt.plot(span_positions, leading_edge, 'g-', label="Leading Edge")
    # Trailing edge
    plt.plot(span_positions, trailing_edge, 'c-', label="Trailing Edge")

    # Plot ribs
    for rib_pos in rib_positions_spanwise:
        rib_leading = leading_edge_x(rib_pos)  # Leading edge x at rib position
        rib_trailing = trailing_edge_x(rib_pos)  # Trailing edge x at rib position
        plt.plot([rib_pos, rib_pos], [rib_leading, rib_trailing], 'b-', label="Rib" if rib_pos == rib_positions_spanwise[0] else "")

    #Cells printing
    def CellCoords(cells:List[cell.Cell]):
        ncells = len(cells)
        fcoor = list()
        rcoor = list()
        mcoor = list()

        for i in range(ncells):
            offset = (leading_edge_x(ZposCell[i]) + chord_at_span(ZposCell[i])/4) #offset due to coordinate system at quarter chord
            fcoor.append(float(cells[i].vertices['itf'][0]) + offset)
            rcoor.append(float(cells[i].vertices['itr'][0]) + offset)
            if cells[i].midSpar != None:
                #mcoor.append(midSpar * chord_at_span(ZposCell[i]) + leading_edge_x(ZposCell[i]))
                mcoor.append(float(cells[i].vertices['itm'][0])+ offset)
            else:
                mcoor.append(None)
        # tip coords
        fcoor.append(float(cells[ncells-1].vertices['otf'][0])+ (leading_edge_x(halfspan) + chord_at_span(halfspan)/4))
        rcoor.append(float(cells[ncells-1].vertices['otr'][0])+ (leading_edge_x(halfspan) + chord_at_span(halfspan)/4))
        if cells[1].midSpar != None:
            mcoor.append(None)
        return fcoor, rcoor, mcoor


    plt.scatter(ZposCell, CellCoords(cells)[0], s=10)
    plt.scatter(ZposCell, CellCoords(cells)[1], s=10)
    plt.plot(ZposCell, CellCoords(cells)[0], label="Front Spar")
    plt.plot(ZposCell, CellCoords(cells)[1], label="Rear Spar")
    if cells[0].midSpar != None:
        plt.scatter(ZposCell, CellCoords(cells)[2], s=10)
        plt.plot(ZposCell, CellCoords(cells)[2], label="Mid Spar")



    # Formatting
    plt.xlabel("Spanwise Position (m)")
    plt.ylabel("Chordwise Position from c/4 at Root (m)")
    plt.title("Wing Top view with Ribs and Cells")
    plt.axis("equal")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()




    plt.subplot(232)
    plt.plot(margins_of_safety[0], margins_of_safety[1], label = "computed margin of safety")
    plt.plot([0, 25], [1, 1], label = "margin of safety of 1 for reference")
    plt.title("Tensile strength failure margin of Safety")
    plt.axis([0, 25, 0, 10])
    plt.xlabel("Spanwise Position (m)")
    plt.grid(True)
    plt.legend()

    plt.subplot(233)
    plt.plot(margins_of_safety[0], margins_of_safety[2], label = "computed margin of safety")
    plt.plot([0, 25], [1, 1], label = "margin of safety of 1 for reference")
    plt.title("Compressive strength failure margin of safety")
    plt.axis([0, 25, 0, 10])
    plt.xlabel("Spanwise Position (m)")
    plt.grid(True)
    plt.legend()

    plt.subplot(234)
    plt.plot(margins_of_safety[0], margins_of_safety[3], label = "computed margin of safety")
    plt.plot([0, 25], [1, 1], label = "margin of safety of 1 for reference")
    plt.title("Stringer column buckling margin of safety")
    plt.axis([0, 25, 0, 10])
    plt.xlabel("Spanwise Position (m)")
    plt.grid(True)
    plt.legend()

    plt.subplot(235)
    plt.plot(margins_of_safety[0], margins_of_safety[4], label = "computed margin of safety")
    plt.plot([0, 25], [1, 1], label = "margin of safety of 1 for reference")
    plt.title("Spar shear buckling margin of safety")
    plt.axis([0, 25, 0, 10])
    plt.xlabel("Spanwise Position (m)")
    plt.grid(True)
    plt.legend()
    
    plt.subplot(236)
    plt.plot(margins_of_safety[0], margins_of_safety[5], label = "computed margin of safety")
    plt.plot([0, 25], [1, 1], label = "margin of safety of 1 for reference")
    plt.title("Skin buckling margin of safety")
    plt.axis([0, 25, 0, 10])
    plt.xlabel("Spanwise Position (m)")
    plt.grid(True)
    plt.legend()

    plt.show()
    #print(margins_of_safety)
print(sum(ribBetweenCounts)+len(ribStations))
print(margins_of_safety[4])

'''Add a code that computes the mass of the design!'''
def final_wing_mass(cells:List[cell.Cell], ribThickness: float) -> float:
    mass = cells[0].wingbox(0).ribMass(ribThickness) #counting the root rib
    for ce in cells: #adding outboard rib mass and cell mass
        mass += 2*(ce.mass + ce.wingbox(1).ribMass(ribThickness))

    return mass

wbMass = final_wing_mass(cells, c.rib_thickness) #assigning the final wingbox mass

#from wp2
def intersparVolume( b, cr, tr, A2c2=0.038):
    return A2c2*b*cr*cr/3*(1+tr+tr*tr)

'''re-obtaining the fuel volume'''
#wbVol = wbMass/c.DENSITY #reverse-obtaining the total structural volume by dividing by material density
#the volume not occupied by the wingbox structure
fuelVolume = intersparVolume(planform.b, planform.cr, planform.TR)*0.85
#fuelVolume = freeIntersparVolume/1.1 #dividing by a safety factor for piping and fuel tank walls

print(f"The mass of the wing structure is: {wbMass}, the fuel volume is: {fuelVolume}")
print(f"The number of stringers in the root cell: top: {cells[0].stringerNumTop}, bottom: {cells[0].stringerNumBot}")