import numpy as np
from kinetics_six_groups import six_group_kinetics


def model_six_group(t, y, params):

    T_f, T_c, T_w, P = y[:4]
    C = y[4:]

    P0 = params.P0
    Tw0 = params.T_in + P0 / (params.mdot * params.cp)
    Tc0 = Tw0 + P0 / params.K_cw
    Tf0 = Tc0 + P0 / params.K_fc

    # Temperature feedback
    rho = (
        params.rho0
        + params.alpha * (T_f - Tf0)
    )

    # Thermal equations
    dTf_dt = (
        P - params.K_fc * (T_f - T_c)
    ) / params.C_f

    dTc_dt = (
        params.K_fc * (T_f - T_c)
        - params.K_cw * (T_c - T_w)
    ) / params.C_c

    dTw_dt = (
        params.K_cw * (T_c - T_w)
        - params.mdot * params.cp * (T_w - params.T_in)
    ) / params.C_w

    # Six-group kinetics
    dP_dt, dC_dt = six_group_kinetics(
        P,
        C,
        rho,
        params.beta_groups,
        params.Lambda,
        params.lambda_groups
    )

    return np.concatenate((
        [dTf_dt, dTc_dt, dTw_dt, dP_dt],
        dC_dt
    ))
