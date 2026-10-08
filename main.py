import numpy as np
from scipy.integrate import solve_ivp
from reactor_parameters import ReactorParameters
from reactor_model import model
from initial_conditions import initial_conditions
import plots


# Instantiate the parameters object
params = ReactorParameters()

y0 = initial_conditions(params)

# Print the initial values
print("Initial fuel temperature:", y0[0], "K")
print("Initial cladding temperature:", y0[1], "K")
print("Initial coolant temperature:", y0[2], "K")
print("Initial precursor concentration (C):", y0[3])

# Solve the system
solution = solve_ivp(
    model,
    t_span=(0, 1000),
    y0=initial_conditions(params),
    args=(params,),
    method='RK45',
    rtol=1e-12,
    atol=1e-14,
    dense_output=True
)
plots.plot_temperatures(solution)