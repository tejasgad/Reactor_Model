import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from time import perf_counter

from reactor_parameters import ReactorParameters
from reactor_model import model
from reactor_model_six_groups import model_six_group
from initial_conditions import (
    initial_conditions,
    initial_conditions_six_group
)

params = ReactorParameters()
lambda_eff = (
    np.sum(params.beta_groups)
    / np.sum(params.beta_groups / params.lambda_groups)
)

# Same time points
t = np.linspace(0, 1000, 2000)

# One-group simulation
start = perf_counter()

sol_1 = solve_ivp(
    model,
    (0, 1000),
    initial_conditions(params),
    args=(params,),
    t_eval=t,
    method="BDF",
    rtol=1e-8,
    atol=1e-10
)

time_1 = perf_counter() - start

# Six-group simulation
start = perf_counter()

sol_6 = solve_ivp(
    model_six_group,
    (0, 1000),
    initial_conditions_six_group(params),
    args=(params,),
    t_eval=t,
    method="BDF",
    rtol=1e-8,
    atol=1e-10
)

time_6 = perf_counter() - start

if not sol_1.success or not sol_6.success:
    raise RuntimeError("One of the simulations failed")

plt.figure(figsize=(9, 5))

plt.plot(t, sol_1.y[3] / 1e6, label="One-group")
plt.plot(t, sol_6.y[3] / 1e6, "--", label="Six-group")

plt.xlabel("Time (s)")
plt.ylabel("Power (MW)")
plt.title("Comparison of Reactor Power")
plt.legend()
plt.grid()
plt.savefig('Comparison_of_power.svg', format='svg', bbox_inches='tight')
plt.show()

plt.figure(figsize=(9, 5))

plt.plot(t, sol_1.y[0], label="One-group")
plt.plot(t, sol_6.y[0], "--", label="Six-group")

plt.xlabel("Time (s)")
plt.ylabel("Fuel Temperature (K)")
plt.title("Comparison of Fuel Temperature")
plt.legend()
plt.grid()
plt.savefig('comparison_of_temp.svg', format='svg', bbox_inches='tight')
plt.show()
print("One-group peak fuel temperature:",
      np.max(sol_1.y[0]))

print("Six-group peak fuel temperature:",
      np.max(sol_6.y[0]))

print("One-group peak power:",
      np.max(sol_1.y[3]))

print("Six-group peak power:",
      np.max(sol_6.y[3]))

print("One-group runtime:", time_1, "s")
print("Six-group runtime:", time_6, "s")
