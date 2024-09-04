flap_defl = float(input('Input Flap deflection '))
normal_e = float(input('Input the Oswald efficiency before flaps '))
Cd0 = float(input('Input Cd0 '))
change_e = 0.0026 * flap_defl
change_Cd0_flaps = 0.0013 * flap_defl
change_Cd0_lg = 0.025 # Choosing worst case scenario according to intro to ac design (page 151)

total_e = normal_e + change_e
total_Cd0 = change_Cd0_flaps + change_Cd0_lg + Cd0

print('Total Oswald is ', round(total_e, 2))
print('Total Cd0 ', round(total_Cd0, 2))

