# Decapodes.jl Physics Examples Not Yet in the Leaderboard

Searched the Decapodes.jl documentation (https://github.com/AlgebraicJulia/Decapodes.jl)
and identified the following documented physics examples that are not yet recorded in the
Decapodes Leaderboard.

## New Physics Examples

### 1. Pipe Flow (Poiseuille)
- **Doc page:** `docs/src/poiseuille/poiseuille.md`
- **URL:** https://algebraicjulia.github.io/Decapodes.jl/dev/poiseuille/poiseuille/
- **Description:** Viscous fluid flow through pipe networks using the Poiseuille model.
  Covers single-pipe segments, multi-segment linear pipes, and binary-tree branching
  pipe networks. Also demonstrates a multiphysics extension coupling density, pressure,
  and advection.
- **First committed:** June 6, 2024 (GeorgeR227, Documentation Overhaul #231)

### 2. Grigoriev Ice Cap
- **Doc page:** `docs/src/grigoriev/grigoriev.md`
- **URL:** https://algebraicjulia.github.io/Decapodes.jl/dev/grigoriev/grigoriev/
- **Description:** Halfar's shallow ice model applied to real-world data from the
  Grigoriev ice cap in Kyrgyzstan (from a 2023 survey). Demonstrates running an
  existing Decapode on observational GeoTIFF data rather than synthetic geometry.
- **First committed:** June 6, 2024 (GeorgeR227, Documentation Overhaul #231)

### 3. Budyko-Sellers-Halfar (BSH)
- **Doc page:** `docs/src/bsh/budyko_sellers_halfar.md`
- **URL:** https://algebraicjulia.github.io/Decapodes.jl/dev/bsh/budyko_sellers_halfar/
- **Description:** Operadic composition of the Budyko-Sellers 1D energy balance model
  with the Halfar model of glacial dynamics. Temperature drives ice deformability via
  Glen's law, creating a feedback loop between warming and glacier flow over 1 million
  simulated years.
- **First committed:** June 6, 2024 (GeorgeR227, Documentation Overhaul #231)

### 4. Halfar-EBM-Water (EBM Melt)
- **Doc page:** `docs/src/ebm_melt/ebm_melt.md`
- **URL:** https://algebraicjulia.github.io/Decapodes.jl/dev/ebm_melt/ebm_melt/
- **Description:** Three-way composition of Halfar ice dynamics, the Budyko-Sellers
  energy balance model, and a meltwater transport equation. Surface temperature drives
  ice melt; meltwater diffuses across the domain. Runs on real PIOMAS sea ice thickness
  data on a spherical mesh over 100-year periods.
- **First committed:** December 4, 2024 (lukem12345, Halfar-Melting-EBM simulation #283)

### 5. Halfar-NS (HALMO)
- **Doc page:** `docs/src/halmo/halmo.md`
- **URL:** https://algebraicjulia.github.io/Decapodes.jl/dev/halmo/halmo/
- **Description:** Coupled simulation of Halfar glacier dynamics and the incompressible
  Navier-Stokes equations (Mohamed et al. formulation) on a spherical Earth-radius
  mesh. A sigmoid blocking function prevents water flow through ice-covered regions.
  "HALMO" = HALfar + MOhamed.
- **First committed:** June 6, 2024 (GeorgeR227, Documentation Overhaul #231)

### 6. Fokker-Planck
- **Doc page:** `docs/src/fokker_planck/fokker_planck.md`
- **URL:** https://algebraicjulia.github.io/Decapodes.jl/dev/fokker_planck/fokker_planck/
- **Description:** Evolution of a probability density function (ρ) on a spherical
  icosphere mesh. Combines an advection term driven by a potential Ψ and a diffusion
  term weighted by inverse temperature β⁻¹. Equation:
    ∂ₜ(ρ) == ∘(⋆,d,⋆)(d(Ψ)∧ρ) + β⁻¹*Δ(ρ)
  Initial conditions use eigenfunctions of the Laplacian; probability is conserved.
- **First committed:** January 30, 2025 (quffaro, Balancing Docs #296)

### 7. Magnetohydrodynamics (MHD)
- **Doc page:** `docs/src/examples/mhd.md`
- **URL:** https://algebraicjulia.github.io/Decapodes.jl/dev/examples/mhd/
- **Description:** Two variants of MHD simulation using the stream function-vorticity
  formulation on spherical meshes, based on Gillespie's "MHD via Discrete Exterior
  Calculus":
  - **Out-of-plane:** magnetic field β perpendicular to the fluid plane; vorticity
    dynamics driven by velocity-magnetic interactions.
  - **In-plane:** magnetic field lies within the fluid plane; 1-form magnetic transport
    advected by the flow.
- **First committed:** January 30, 2025 (quffaro, Balancing Docs #296)

---

## Already in Leaderboard

For reference, these doc pages are already represented in the leaderboard:

| Leaderboard Entry | Doc page |
|---|---|
| Cahn-Hilliard | ch/cahn-hilliard.md |
| Brusselator (all variants) | brussel/brussel.md |
| Gray-Scott | examples/chemistry/gray_scott.md |
| Halfar / CISM | cism/cism.md |
| Budyko-Sellers | examples/climate/budyko_sellers.jl |
| Navier-Stokes Vorticity | navier_stokes/ns.md |
| Nonhydrostatic Buoyant Seawater | nhs/nhs_lite.md |
| Porous Convection | pconv/porous_convection.md |
| Klausmeier | klausmeier/klausmeier.md (in plots) |
| Gompertz oncology | examples/oncology/tumor_proliferation_invasion.md (in plots) |

## Notes on Borderline Cases

- **Harmonics** (`harmonics/harmonics.md`): Demonstrates spectral analysis of the
  Laplacian operator on meshes. Mathematical tooling tutorial rather than a physics
  simulation per se.
- **Halfar Calibration** (`calibrate/calibration.md`): Calibrates Halfar model
  parameters via optimization. Methodology tutorial rather than a new physics model.
- **Ice Dynamics** (`ice_dynamics/ice_dynamics.md`): Reference page for the Halfar
  model; covered by existing CISM leaderboard entry.
