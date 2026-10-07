from dataclasses import dataclass

@dataclass
class ReactorParameters:
    # Thermal Paarmeters
    P0: float = 1e6       # Reference Reactor thermal power [W]
    K_fc: float = 1e4     # Fuel-cladding conductance [W/K]
    K_cw: float = 2e4     # Cladding-coolant conductance [W/K]

    C_f: float = 5e5      # Fuel heat capacity [J/K]
    C_c: float = 1e5      # Cladding heat capacity [J/K]
    C_w: float = 2e5      # Coolant heat capacity [J/K]

    mdot: float = 10.0    # Coolant mass flow rate [kg/s]
    cp: float = 4200.0    # Coolant specific heat capacity [J/(kg K)]
    T_in: float = 300.0   # Coolant inlet temperature [K]

    #Kinetics Parameters
    beta: float = 0.0065     # Effective delayed neutron fraction [-]
    Lambda: float = 1e-4     # Neutron generation time [s]
    lambda_: float = 0.08    # Precursor decay constant [1/s]

    rho0: float = 0.001
    alpha: float = -1e-5