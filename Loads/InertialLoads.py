
def wingskin_mass(total_ribs_mass, wing_mass, root_chord, tip_chord, span):
    L = span/2
    k = (wing_mass - total_ribs_mass)/((tip_chord-root_chord)*(2- L))
    wingskin_shear_linear = -2*k*(tip_chord-root_chord)/L
    wingskin_shear_consant = 2*k*(tip_chord-root_chord)/L
    return  wingskin_shear_linear , wingskin_shear_consant

def engine_zpos(span):
    L = span/2
    engine_zpos = 0.3*L
    return engine_zpos

def engine_xpos(root_chord):
    engine_xpos = (1/2)*root_chord
    return engine_xpos  


def engine_shear(engine_mass, engine_zpos)