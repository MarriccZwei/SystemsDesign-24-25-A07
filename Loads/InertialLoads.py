
def wingskin_mass(total_ribs_mass, wing_mass, root_chord, tip_chord, length):
    wingskin_mass = wing_mass - total_ribs_mass
    k = (wing_mass - total_ribs_mass)/((tip_chord-root_chord)*(2- length))
    wingskin_shear_linear = -2*k*(tip_chord-root_chord)/length
    wingskin_shear_consant = 2*k*(tip_chord-root_chord)/length
    return  wingskin_shear_linear , wingskin_shear_consant
