def model(t, y, params):
  T_f, T_c, T_w, P, C = y # Unpack the state variables

  P0 = params.P0
  Tw0 = params.T_in + P0 / (params.mdot * params.cp)
  Tc0 = Tw0 + P0 / params.K_cw
  Tf0 = Tc0 + P0 / params.K_fc
    # Adding temperature feedback to the value of rho
  rho = ( params.rho0 + params.alpha * (T_f - Tf0))
  # Calculate the rates of change of temperature
  dT_f_dt = (P - params.K_fc * (T_f - T_c)) / params.C_f
  dT_c_dt = (params.K_fc * (T_f - T_c) - params.K_cw * (T_c - T_w)) / params.C_c
  dT_w_dt = (params.K_cw * (T_c - T_w) - params.mdot * params.cp * (T_w - params.T_in)) / params.C_w

  # Point Kinetics Equations in terms of normalised power 'p'
  dP_dt = (rho - params.beta) * P / params.Lambda + C * params.lambda_
  dC_dt = params.beta * P / params.Lambda - C * params.lambda_

  return [dT_f_dt, dT_c_dt, dT_w_dt, dP_dt, dC_dt]