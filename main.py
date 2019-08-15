import voltage_response_simulation as sim
import matplotlib.pyplot as plt


def create_coordinates_for_tikz(potentials, radius, length, line_charge_density):
    fluo = sim.normalized_fluorescence(potentials, length, radius, line_charge_density)
    ip_index = sim.inflection_point(fluo)

    for pot, fl in fluo.items():
        print(str(pot) + " " + str(fl) + "\\\\")

    ip_x = list(fluo.keys())[ip_index]
    print("IP = " + str(list(fluo.keys())[ip_index]) + " " + str(list(fluo.values())[ip_index]) + "\\\\")
    print("IP slope = " + str(sim.inflection_point_slope(fluo)))

    print("------------------------ Inflection point corrected -----------------------")
    cntr = 0
    for pot, fl in fluo.items():
        if cntr % 10 == 0:
            print(str(pot - ip_x) + " " + str(fl) + "\\\\")
        cntr += 1

    return fluo


pot = [-3.9 + 0.001 * x for x in range(1, 5060, 1)]  # potential range

# fluo = create_coordinates_for_tikz(pot, sim.r_dna, sim.b*sim.bp, sim.rho_dna)
# fluo = create_coordinates_for_tikz(pot, sim.r_dna, sim.b*sim.bp*2, sim.rho_dna)
# fluo = create_coordinates_for_tikz(pot, sim.r_dna * 2.8, 50e-9, sim.rho_dna * 4)
fluo = create_coordinates_for_tikz(pot, sim.r_dna * 2.41, 50e-9, sim.rho_dna * 6)

fluo = sim.normalized_fluorescence(pot, 50e-9, sim.r_dna * 2.41, sim.rho_dna * 4)
plt.plot(list(fluo.keys()), list(fluo.values()))
fluo = sim.normalized_fluorescence(pot, 100e-9, sim.r_dna * 3, sim.rho_dna * 6)
plt.plot(list(fluo.keys()), list(fluo.values()))
fluo = sim.normalized_fluorescence(pot, 16e-9, sim.r_dna, sim.rho_dna)
plt.plot(list(fluo.keys()), list(fluo.values()))
fluo = sim.normalized_fluorescence(pot, 32e-9, sim.r_dna, sim.rho_dna)
plt.plot(list(fluo.keys()), list(fluo.values()))
plt.show()
