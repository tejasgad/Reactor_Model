import importlib
from scipy.integrate import solve_ivp
from reactor_parameters import ReactorParameters
from reactor_model import model
import plots

# Force reload the modified plots module to apply changes
importlib.reload(plots)

# Instantiate the parameters object
params = ReactorParameters()

P0 = params.P0
Tw0 = params.T_in + P0 / (params.mdot * params.cp)
Tc0 = Tw0 + P0 / params.K_cw
Tf0 = Tc0 + P0 / params.K_fc

# Calculate exact analytical eta0 to avoid floating point truncation mismatch
C = round(params.beta * P0 / (params.Lambda * params.lambda_)) * params.lambda_

# Print the initial values
print("Initial fuel temperature:", Tf0, "K")
print("Initial cladding temperature:", Tc0, "K")
print("Initial coolant temperature:", Tw0, "K")
print("Initial precursor concentration (C):", C)

# Solve the system
solution = solve_ivp(
    model,
    t_span=(0, 1000),
    y0=[Tf0, Tc0, Tw0, P0, C],
    args=(params,),
    method='RK45',
    rtol=1e-12,
    atol=1e-14,
    dense_output=True
)
plots.plot_temperatures(solution)