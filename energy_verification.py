import numpy as np
import matplotlib.pyplot as plt
from reactor_parameters import ReactorParameters
from reactor_model import model
from initial_conditions import initial_conditions
from scipy.integrate import solve_ivp

params = ReactorParameters()
y0 = initial_conditions(params)

solution = solve_ivp(
    model,
    (0, 1000),
    y0,
    args=(params,),
    rtol=1e-9,
    atol=1e-11
)

t = solution.t

T_f, T_c, T_w, P, C = solution.y

# Calculate derivatives directly from the model
derivatives = np.array([
    model(ti, solution.y[:, i], params)
    for i, ti in enumerate(t)
])

dTf_dt = derivatives[:, 0]
dTc_dt = derivatives[:, 1]
dTw_dt = derivatives[:, 2]

# Rate of change of stored thermal energy
dE_dt = (
    params.C_f * dTf_dt
    + params.C_c * dTc_dt
    + params.C_w * dTw_dt
)

# Net thermal power entering the system
Q_out = params.mdot * params.cp * (T_w - params.T_in)

net_power = P - Q_out

# Energy balance residual
residual = dE_dt - net_power

print("Maximum residual:", np.max(np.abs(residual)), "W")

plt.figure(figsize=(9, 5))

plt.plot(t, residual)

plt.xlabel("Time (s)")
plt.ylabel("Energy balance residual (W)")
plt.title("Verification of Thermal Energy Conservation")
plt.grid(True)

plt.show()

plt.figure(figsize=(9, 5))

plt.plot(t, dE_dt, label="Rate of stored energy change")
plt.plot(t, net_power, "--", label="Net input power")

plt.xlabel("Time (s)")
plt.ylabel("Power (W)")
plt.title("Thermal Energy Balance")
plt.legend()
plt.grid(True)

plt.show()