import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from reactor_parameters import ReactorParameters
from reactor_model import model
from initial_conditions import initial_conditions

base_params = ReactorParameters()
y0 = initial_conditions(base_params)

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

    T_minus = get_peak_fuel_temperature(params_minus, y0)

    # Upper value
    params_plus = ReactorParameters()
    setattr(params_plus, parameter_name, x0 + dx)

    T_plus = get_peak_fuel_temperature(params_plus, y0)

    # Central finite difference
    derivative = (T_plus - T_minus) / (2 * dx)

    # Baseline
    params_0 = ReactorParameters()
    setattr(params_0, parameter_name, x0)

    T0 = get_peak_fuel_temperature(params_0, y0)

    # Dimensionless sensitivity
    sensitivity = (x0 / T0) * derivative

    return T0, derivative, sensitivity

T0, derivative, S_mdot = calculate_sensitivity("mdot",10.0,0.25, y0)

print("Baseline peak fuel temperature:", T0, "K")
print("dTmax/dmdot:", derivative, "K/(kg/s)")
print("Dimensionless sensitivity:", S_mdot)

T0, derivative, S_rho = calculate_sensitivity(
    "rho0",
    0.001,
    0.000025,
    y0
)

print("Baseline peak fuel temperature:", T0, "K")
print("dTmax/drho0:", derivative, "K")
print("Dimensionless sensitivity:", S_rho)

T0, derivative, S_alpha = calculate_sensitivity(
    "alpha",
    -1e-5,
    5e-7,
    y0
)

print("Baseline peak fuel temperature:", T0, "K")
print("dTmax/dalpha:", derivative, "K^2")
print("Dimensionless sensitivity:", S_alpha)
