import math

g_0 = 9.80665
p_0 = 101325
R_0 = 287
T_0 = 288.15
h_0 = 0

def temp_height(startHeight, endHeight, a, startTemp):
    return startTemp + a*(endHeight - startHeight)

def gradient_pressure(startPressure, a, startTemp, endTemp):
    return (endTemp/startTemp)**((-g_0)/(a*R_0))*startPressure

def constant_pressure(startPressure, startHeight, endHeight, temp):
    return math.exp(((-g_0)/(temp*R_0))*(endHeight-startHeight))*startPressure

def pressure_tropoS(height):
    gradientCoeff = -0.0065
    T = temp_height(h_0, height, gradientCoeff, T_0)
    return gradient_pressure(p_0, gradientCoeff, T_0, T), T

def pressure_tropoP(height):
    prev = pressure_tropoS(11000)
    pP = prev[0]
    tP = prev[1] 
    return constant_pressure(pP, 11000, height, tP), tP

def pressure_strato1(height):
    prev = pressure_tropoP(20000)
    pP = prev[0]
    tP = prev[1]
    gradientCoeff = 0.0010
    T = temp_height(20000, height, gradientCoeff, tP)
    return gradient_pressure(pP, gradientCoeff, tP, T), T

def pressure_strato2(height):
    prev = pressure_strato1(32000)
    pP = prev[0]
    tP = prev[1]
    gradientCoeff = 0.0028
    T = temp_height(32000, height, gradientCoeff, tP)
    return gradient_pressure(pP, gradientCoeff, tP, T), T

def pressure_stratoP(height):
    prev = pressure_strato2(47000)
    pP = prev[0]
    tP = prev[1] 
    return constant_pressure(pP, 47000, height, tP), tP

def pressure_meso1(height):
    prev = pressure_stratoP(51000)
    pP = prev[0]
    tP = prev[1]
    gradientCoeff = -0.0028
    T = temp_height(51000, height, gradientCoeff, tP)
    return gradient_pressure(pP, gradientCoeff, tP, T), T

def pressure_meso2(height):
    prev = pressure_stratoP(71000)
    pP = prev[0]
    tP = prev[1]
    gradientCoeff = -0.0020
    T = temp_height(71000, height, gradientCoeff, tP)
    return gradient_pressure(pP, gradientCoeff, tP, T), T

def main_calc(height):
    inp = round(height)
    match inp:
        case inp if inp in range(0,11000): out = pressure_tropoS(inp)
        case inp if inp in range(11001, 20000): out = pressure_tropoP(inp)
        case inp if inp in range(20001, 32000): out = pressure_strato1(inp)
        case inp if inp in range(32001, 47000): out = pressure_strato2(inp)
        case inp if inp in range(47001, 51000): out = pressure_stratoP(inp)
        case inp if inp in range(51001, 71000): out = pressure_meso1(inp)
        case inp if inp in range(71001, 86000): out = pressure_meso2(inp)
    return out[0], out[1]

def pressure(altitude):
    data = main_calc(altitude)
    return data[0]

def temperature(altitude):
    data = main_calc(altitude)
    return data[1]

def density(altitude):
    data = main_calc(altitude)
    return (data[0])/(R_0*data[1])

def speedOfSound(altitude):
    temp = temperature(altitude)
    speed = math.sqrt(1.4*R_0*temp)
    return speed

if __name__ == '__main__':
    print(pressure(1000))
    print(temperature(1000))
    print(density(1000))