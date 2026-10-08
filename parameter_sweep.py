import numpy as np
from scipy.integrate import solve_ivp
from reactor_parameters import ReactorParameters
from reactor_model import model
from initial_conditions import initial_conditions
import matplotlib.pyplot as plt


# Instantiate the parameters object
params = ReactorParameters()

y0 = initial_conditions(params)
# Print the initial values
print("Initial fuel temperature:", y0[0], "K")
print("Initial cladding temperature:", y0[1], "K")
print("Initial coolant temperature:", y0[2], "K")
print("Initial precursor concentration (C):", y0[3])

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
        y0=y0,
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

#Running rho0 Parameter sweep
reactivities = [0.0002,0.0005, 0.001, 0.0015, 0.002]  # kg/s
peak_fuel_temps = []
peak_powers = []
for reactivity in reactivities:

    # Change only the coolant flow rate
    params.rho0 = reactivity

    # Run simulation
    solution = solve_ivp(
        model,
        t_span=(0, 1000),
        y0=y0,
        args=(params,),
        dense_output=True
    )

    # Extract results
    T_f = solution.y[0]
    P = solution.y[3]

    # Store maximum values
    peak_fuel_temps.append(np.max(T_f))
    peak_powers.append(np.max(P))

for reactivity, temp, power in zip(
    reactivities,
    peak_fuel_temps,
    peak_powers
):
    print(
        f"Initial Reactivity = {reactivity:5.5f} | "
        f"Peak T_f = {temp:8.2f} K | "
        f"Peak P = {power:8.3f} W"
    )
  # --------------------------------
  # Plot Reactivity
  # --------------------------------

fig, ax = plt.subplots()

ax.plot(reactivities, peak_fuel_temps, 'o-')

ax.set_xlabel("Reactivity")
ax.set_ylabel("Peak Fuel Temperature (K)")
ax.set_title("Peak Fuel Temperature vs Reactivity")
ax.grid()

plt.show()

#Running alpha   Parameter sweep
feedback_coefficients = [-2e-5, -1.5e-5, -1e-5, -5e-6, -2.5e-6]
peak_fuel_temps = []
peak_powers = []
for feedback_coefficient in feedback_coefficients:

    # Change only the feedback coefficient value
    params.alpha = feedback_coefficient

    # Run simulation
    solution = solve_ivp(
        model,
        t_span=(0, 1000),
        y0=y0,
        args=(params,),
        dense_output=True
    )

    # Extract results
    T_f = solution.y[0]
    P = solution.y[3]

    # Store maximum values
    peak_fuel_temps.append(np.max(T_f))
    peak_powers.append(np.max(P))

for feedback_coefficient, temp, power in zip(
    feedback_coefficients,
    peak_fuel_temps,
    peak_powers
):
    print(
        f"Feedback Coefficient = {feedback_coefficient:5.9f} | "
        f"Peak T_f = {temp:8.2f} K | "
        f"Peak P = {power:8.3f} W"
    )
  # --------------------------------
  # Plot Coefficient
  # --------------------------------

fig, ax = plt.subplots()

ax.plot(feedback_coefficients, peak_fuel_temps, 'o-')

ax.set_xlabel("Feedback Coefficient")
ax.set_ylabel("Peak Fuel Temperature (K)")
ax.set_title("Peak Fuel Temperature vs Coefficient")
ax.grid()

plt.show()