import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from reactor_parameters import ReactorParameters
from initial_conditions import initial_conditions_six_group
from reactor_model_six_groups import model_six_group

params = ReactorParameters()

y0 = initial_conditions_six_group(params)

t = np.linspace(0, 1000, 2000)

solution = solve_ivp(
    model_six_group,
    (0, 1000),
    y0,
    args=(params,),
    t_eval=t,
    method="BDF",
    rtol=1e-8,
    atol=1e-10
)


T_f, T_c, T_w, P = solution.y[:4]

plt.plot(solution.t, T_f, label="Fuel")
plt.plot(solution.t, T_c, label="Cladding")
plt.plot(solution.t, T_w, label="Coolant")

plt.xlabel("Time (s)")
plt.ylabel("Temperature (K)")
plt.title("Six-Group Thermal Response")
plt.legend()
plt.grid()
plt.savefig('temperatures.svg',format='svg', bbox_inches='tight')
plt.show()

plt.plot(solution.t, P, label="P")
plt.xlabel("Time (s)")
plt.ylabel("Power (W)")
plt.title("Six-Group Power Response")
plt.legend()
plt.grid()
plt.show()