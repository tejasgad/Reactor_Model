import matplotlib.pyplot as plt

def plot_temperatures(solution):

  T_f = solution.y[0]
  T_c = solution.y[1]
  T_w = solution.y[2]
  P = solution.y[3]
  C = solution.y[4]

  # --------------------------------
  # Plot 1: Temperatures
  # --------------------------------

  fig, ax = plt.subplots()

  ax.plot(solution.t, T_f, label="Fuel")
  ax.plot(solution.t, T_c, label="Cladding")
  ax.plot(solution.t, T_w, label="Coolant")

  ax.set_xlabel("Time (s)")
  ax.set_ylabel("Temperature (K)")
  ax.set_title("Reactor Temperatures")
  ax.legend()
  ax.grid()
  plt.savefig('temperatures.svg',format='svg', bbox_inches='tight')
  plt.show()

  # --------------------------------
  # Plot 2: Power
  # --------------------------------

  fig, ax = plt.subplots()

  ax.plot(solution.t, P)

  ax.set_xlabel("Time (s)")
  ax.set_ylabel("Power (W)")
  ax.set_title("Reactor Power")
  ax.grid()

  plt.show()

  # --------------------------------
  # Plot 3: Power + Temperatures
  # --------------------------------

  fig, ax1 = plt.subplots()

  # Temperature - left axis
  ax1.plot(solution.t, T_f, label="Fuel")
  ax1.plot(solution.t, T_c, label="Cladding")
  ax1.plot(solution.t, T_w, label="Coolant")

  ax1.set_xlabel("Time (s)")
  ax1.set_ylabel("Temperature (K)")

  # Power - right axis
  ax2 = ax1.twinx()

  ax2.plot(solution.t, P, "--", label="Power")
  ax2.set_ylabel("Power (W)")

  # Combined legend
  lines1, labels1 = ax1.get_legend_handles_labels()
  lines2, labels2 = ax2.get_legend_handles_labels()

  ax1.legend(lines1 + lines2, labels1 + labels2)

  ax1.set_title("Reactor Power and Thermal Response")
  ax1.grid()
  plt.savefig('power_and_temperatures.svg', format='svg', bbox_inches='tight')
  plt.show()

