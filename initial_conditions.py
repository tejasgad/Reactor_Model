def initial_conditions(params):


    P0 = params.P0
    Tw0 = params.T_in + P0 / (params.mdot * params.cp)
    Tc0 = Tw0 + P0 / params.K_cw
    Tf0 = Tc0 + P0 / params.K_fc
    C = params.beta * P0 / (params.Lambda * params.lambda_)

    return [Tf0, Tc0, Tw0, P0, C]

def initial_conditions_six_group(params):

    P0 = params.P0

    Tw0 = params.T_in + P0 / (params.mdot * params.cp)
    Tc0 = Tw0 + P0 / params.K_cw
    Tf0 = Tc0 + P0 / params.K_fc

    C0 = (
        params.beta_groups * P0
        / (params.Lambda * params.lambda_groups)
    )

    return [Tf0, Tc0, Tw0, P0, *C0]