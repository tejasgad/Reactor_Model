# Reduced-Order Reactor Thermal Model

A computational physics project investigating the coupling between
simplified reactor point kinetics and transient thermal behaviour.

## Current model

The model currently includes:

- Lumped fuel, cladding and coolant thermal nodes
- Numerical integration using SciPy `solve_ivp`
- One-group delayed neutron point kinetics
- Temperature-reactivity feedback
- Verification against simplified analytical solutions

