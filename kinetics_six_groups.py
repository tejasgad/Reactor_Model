import numpy as np

def six_group_kinetics(P, C, rho, beta, Lambda, lambdas):

    # Total delayed neutron fraction
    beta_total = np.sum(beta)

    # Delayed neutron contribution
    delayed_source = np.sum(lambdas * C)

    # Rate of change of power
    dP_dt = (
        ((rho - beta_total) / Lambda) * P
        + delayed_source
    )

    # Rate of change of each precursor group
    dC_dt = (
        (beta / Lambda) * P
        - lambdas * C
    )

    return dP_dt, dC_dt

