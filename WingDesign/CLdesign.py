import json

maindata = json.load(open("Protocols/main.json"))

wingLoading = maindata["W/S"]
wFuel = maindata["MFUEL"]*9.81
surface = maindata["S"]
rho = 0.3163
vCruise = 242
q = 0.5*rho*vCruise**2
w = (wingLoading*surface)-wFuel
averageWS = 0.5*(2*w/surface+1.05*wFuel/surface)
cL = 1.1*averageWS*1/q
print(cL)