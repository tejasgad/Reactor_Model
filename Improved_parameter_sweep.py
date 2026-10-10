import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from reactor_parameters import ReactorParameters
from reactor_model import model
from initial_conditions import initial_conditions


def parameter_scan(parameter_name, values):

    # Create baseline reactor
    base_params = ReactorParameters()

    # Calculate ONE common initial state
    y0 = initial_conditions(base_params)

    peak_temperatures = []
    peak_powers = []

    for value in values:

        # Start with baseline parameters
        params = ReactorParameters()

        # Perturb only the parameter being studied
        setattr(params, parameter_name, value)

        # Run simulation from COMMON initial state
        solution = solve_ivp(
            model,
            (0, 1000),
            y0,
            args=(params,)
        )

        # Extract results
        T_f = solution.y[0]
        P = solution.y[3]

        peak_temperatures.append(np.max(T_f))
        peak_powers.append(np.max(P))

    return peak_temperatures, peak_powers

# flow_rates = [5, 7.5, 10, 12.5, 15]
#
# peak_temperatures, peak_powers = parameter_scan(
#     "mdot",
#     flow_rates
# )
#
# plt.plot(flow_rates, peak_temperatures, "o-")
#
# plt.xlabel("Coolant mass flow rate (kg/s)")
# plt.ylabel("Peak fuel temperature (K)")
# plt.title("Sensitivity to Coolant Flow")
# plt.grid()
#
# plt.show()
#
# reactivities = [0.0002, 0.0005, 0.001, 0.0015, 0.002]
#
# peak_temperatures, peak_powers = parameter_scan(
#     "rho0",
#     reactivities
# )
#
# plt.plot(reactivities, peak_temperatures, "o-")
#
# plt.xlabel("Initial reactivity")
# plt.ylabel("Peak fuel temperature (K)")
# plt.title("Sensitivity to Reactivity")
# plt.grid()
#
# plt.show()
#
# feedback_coefficients = [-2e-5, -1.5e-5, -1e-5, -5e-6, -2.5e-6]
#
# peak_temperatures, peak_powers = parameter_scan(
#     "alpha",
#     feedback_coefficients
# )
# plt.plot(feedback_coefficients, peak_temperatures, "o-")
#
# plt.xlabel("Temperature feedback coefficient (1/K)")
# plt.ylabel("Peak fuel temperature (K)")
# plt.title("Sensitivity to Temperature Feedback")
# plt.grid()
#
# plt.show()

def get_peak_fuel_temperature(params, y0):

    solution = solve_ivp(
        model,
        (0, 1000),
        y0,
        args=(params,)
    )

    Tf = solution.y[0]

    return np.max(Tf)

def calculate_sensitivity(parameter_name, x0, dx, y0):

    # Lower value
    params_minus = ReactorParameters()
    setattr(params_minus, parameter_name, x0 - dx)

    T_minus = get_peak_fuel_temperature(
        params_minus,
        y0
    )

    # Upper value
    params_plus = ReactorParameters()
    setattr(params_plus, parameter_name, x0 + dx)

    T_plus = get_peak_fuel_temperature(
        params_plus,
        y0
    )

    # Central finite difference
    derivative = (T_plus - T_minus) / (2 * dx)

    # Baseline
    params_0 = ReactorParameters()
    setattr(params_0, parameter_name, x0)

    T0 = get_peak_fuel_temperature(
        params_0,
        y0
    )

    # Dimensionless sensitivity
    sensitivity = (x0 / T0) * derivative

    return T0, derivative, sensitivity