import OOP.Cell as cell
from typing import Iterable

def cell_distr(planform, ribposes, stringerDesign, wingBoxThicknesses, cutoffidx, midSpar):
    halfspan = planform.b/2
    cells = list()
    for i in range(1, len(ribposes)):
        if i > cutoffidx:
            midSpar = None
        cells.append(cell.Cell(planform, ribposes[i-1]*halfspan, ribposes[i]*halfspan, stringerDesign, wingBoxThicknesses, midSpar))
    return cells

