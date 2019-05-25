import voltage_response_simulation as sim
import matplotlib.pyplot as plt


potentials = [-0.2 + 0.01 * x for x in range(1, 56, 1)]               # potential range
radius = sim.r_dna * 3
length = 100e-9
line_charge_density = sim.rho_dna * 6

fluo = sim.normalized_fluorescence(potentials, length, radius, line_charge_density)
ip_index = sim.inflection_point(fluo)

for pot, fl in fluo.items():
    print(str(pot) + " " + str(fl)+"\\\\")

print("IP = "+str(list(fluo.keys())[ip_index]) + " " + str(list(fluo.values())[ip_index])+"\\\\")


plt.plot(list(fluo.keys()), list(fluo.values()), list(fluo.keys())[ip_index], list(fluo.values())[ip_index], 'o')
plt.show()