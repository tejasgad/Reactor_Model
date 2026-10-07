import numpy as np
from scipy.integrate import solve_ivp
from reactor_parameters import ReactorParameters
from reactor_model import model
from initial_conditions import initial_conditions
import plots


# Instantiate the parameters object
params = ReactorParameters()

# Print the initial values
print("Initial fuel temperature:", Tf0, "K")
print("Initial cladding temperature:", Tc0, "K")
print("Initial coolant temperature:", Tw0, "K")
print("Initial precursor concentration (C):", C)

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