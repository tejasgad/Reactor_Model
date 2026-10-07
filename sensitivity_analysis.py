import numpy as np
from scipy.integrate import solve_ivp
from reactor_parameters import ReactorParameters
from reactor_model import model
from initial_conditions import initial_conditions
import matplotlib.pyplot as plt


# Instantiate the parameters object
params = ReactorParameters()

# Print the initial values
print("Initial fuel temperature:", Tf0, "K")
print("Initial cladding temperature:", Tc0, "K")
print("Initial coolant temperature:", Tw0, "K")
print("Initial precursor concentration (C):", C)

#Running m dot Parameter sweep
flow_rates = [5, 7.5, 10, 12.5, 15]  # kg/s
peak_fuel_temps = []
peak_powers = []
for flow_rate in flow_rates:

    # Change only the coolant flow rate
    params.mdot = flow_rate

    # Run simulation
    solution = solve_ivp(
        model,
        t_span=(0, 1000),
        y0=initial_conditions(params),
        args=(params,),
        dense_output=True
    )

    # Extract results
    T_f = solution.y[0]
    P = solution.y[3]

    # Store maximum values
    peak_fuel_temps.append(np.max(T_f))
    peak_powers.append(np.max(P))

for flow, temp, power in zip(
    flow_rates,
    peak_fuel_temps,
    peak_powers
):
    print(
        f"Flow = {flow:5.1f} kg/s | "
        f"Peak T_f = {temp:8.2f} K | "
        f"Peak P = {power:8.3f} W"
    )
  # --------------------------------
  # Plot Sensitivity
  # --------------------------------

fig, ax = plt.subplots()

ax.plot(flow_rates, peak_fuel_temps, 'o-')

ax.set_xlabel("Coolant Mass Flow Rate (kg/s)")
ax.set_ylabel("Peak Fuel Temperature (K)")
ax.set_title("Peak Fuel Temperature vs Coolant Flow Rate")
ax.grid()

plt.show()