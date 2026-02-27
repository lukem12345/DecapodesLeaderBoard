# Decapodes.jl Physics Examples Not Yet in the Leaderboard

Searched the Decapodes.jl documentation and GitHub repository
(https://github.com/AlgebraicJulia/Decapodes.jl) and identified the following
documented physics examples not yet recorded in the Decapodes Leaderboard.

The authoritative source of all doc pages is `docs/make.jl` in the repo.

---

## Examples with Full Documentation Pages (Model Zoo / Examples)

### 1. Pipe Flow (Poiseuille)
- **Doc page:** `docs/src/poiseuille/poiseuille.md`
- **URL:** https://algebraicjulia.github.io/Decapodes.jl/dev/poiseuille/poiseuille/
- **Description:** Viscous fluid flow through pipe networks using the Poiseuille model.
  Covers single-pipe segments, multi-segment linear pipes, and binary-tree branching
  pipe networks. Also demonstrates a multiphysics extension coupling density, pressure,
  and advection. μ̃ represents negative viscosity per unit area; R is pipe boundary drag.
- **First committed:** June 6, 2024 (GeorgeR227, Documentation Overhaul #231)

### 2. Grigoriev Ice Cap
- **Doc page:** `docs/src/grigoriev/grigoriev.md`
- **URL:** https://algebraicjulia.github.io/Decapodes.jl/dev/grigoriev/grigoriev/
- **Description:** Halfar's shallow ice model applied to real-world data from the
  Grigoriev ice cap in Kyrgyzstan (from a 2023 survey GeoTIFF). Demonstrates running
  an existing Decapode on observational data rather than synthetic geometry.
- **First committed:** June 6, 2024 (GeorgeR227, Documentation Overhaul #231)

### 3. Budyko-Sellers-Halfar (BSH)
- **Doc page:** `docs/src/bsh/budyko_sellers_halfar.md`
- **URL:** https://algebraicjulia.github.io/Decapodes.jl/dev/bsh/budyko_sellers_halfar/
- **Description:** Operadic composition of the Budyko-Sellers 1D energy balance model
  with the Halfar model of glacial dynamics. Temperature drives ice deformability via
  Glen's law, creating a feedback loop between warming and glacier flow over 1 million
  simulated years. Distinct from the standalone Budyko-Sellers leaderboard entry.
- **First committed:** June 6, 2024 (GeorgeR227, Documentation Overhaul #231)

### 4. Halfar-EBM-Water
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
  Navier-Stokes equations (Mohamed et al. formulation) on a spherical Earth-radius mesh.
  A sigmoid blocking function prevents water flow through ice-covered regions.
  "HALMO" = HALfar + MOhamed.
- **First committed:** June 6, 2024 (GeorgeR227, Documentation Overhaul #231)

### 6. Fokker-Planck
- **Doc page:** `docs/src/fokker_planck/fokker_planck.md`
- **URL:** https://algebraicjulia.github.io/Decapodes.jl/dev/fokker_planck/fokker_planck/
- **Description:** Evolution of a probability density function (ρ) on a spherical
  icosphere mesh. Combines an advection term driven by a potential Ψ and a diffusion
  term weighted by inverse temperature β⁻¹:
    ∂ₜ(ρ) == ∘(⋆,d,⋆)(d(Ψ)∧ρ) + β⁻¹*Δ(ρ)
  Initial conditions use eigenfunctions of the Laplacian; probability is conserved.
- **First committed:** January 30, 2025 (quffaro / Matt Cuffaro, Balancing Docs #296)

### 7. Magnetohydrodynamics (MHD)
- **Doc page:** `docs/src/examples/mhd.md`
- **URL:** https://algebraicjulia.github.io/Decapodes.jl/dev/examples/mhd/
- **Description:** Two variants of MHD simulation using the stream function-vorticity
  formulation on spherical meshes, based on Gillespie's "MHD via Discrete Exterior
  Calculus":
  - **Out-of-plane:** magnetic field β perpendicular to the fluid plane; vorticity
    dynamics driven by velocity-magnetic interactions.
  - **In-plane:** magnetic field lies within the fluid plane; 1-form magnetic
    transport advected by the flow.
  Extends the NS vorticity Decapode already in the leaderboard with a magnetic field.
- **First committed:** January 30, 2025 (quffaro, Balancing Docs #296; updated June 8,
  2025 by lukem12345)

### 8. Tumor Proliferation-Invasion (Oncology)
- **Doc page:** `docs/src/examples/oncology/tumor_proliferation_invasion.md`
- **URL:** https://algebraicjulia.github.io/Decapodes.jl/dev/examples/oncology/tumor_proliferation_invasion/
- **Description:** Full composition of a tumor growth model (Gompertz or logistic) with
  a tumor invasion/diffusion model. The leaderboard plots/diagrams currently reference
  only the Gompertz growth component; the documented example covers the complete
  proliferation-invasion composition.
- **Note:** The Gompertz growth diagram and plot are already in the leaderboard's
  plots/diagrams section. This full composition is not yet a leaderboard record.

---

## GitHub Examples Without Dedicated Doc Pages (Yet)

These scripts exist in the `examples/` directory but are not yet promoted to full
documentation pages in the Model Zoo:

### 9. Shallow Water Equations
- **File:** `examples/sw/sw.jl`, `examples/sw/sw_with_advection.jl`
- **URL:** https://github.com/AlgebraicJulia/Decapodes.jl/tree/main/examples/sw
- **Description:** Advection-diffusion dynamics on an icosphere mesh representing
  Earth's surface (radius 6371 + 90 km). The `sw_with_advection.jl` variant adds
  advective flux via a velocity field V on top of Fick's law diffusion.

### 10. Conjugate Heat Transfer
- **File:** `examples/diff_adv/cht.jl` (+ CUDA variant `cht_cuda.jl`)
- **URL:** https://github.com/AlgebraicJulia/Decapodes.jl/tree/main/examples/diff_adv
- **Description:** Coupled heat transfer simulation. GPU-accelerated variant available.

### 11. Heat Equation
- **File:** `examples/diff_adv/heat.jl` (+ CUDA variant `heat_cuda.jl`)
- **URL:** https://github.com/AlgebraicJulia/Decapodes.jl/tree/main/examples/diff_adv
- **Description:** Heat diffusion equation, including a GPU-accelerated variant.

### 12. Coupled Navier-Stokes / Cahn-Hilliard (Multi-Phase Flow)
- **File:** `examples/climate/mpf.jl`
- **URL:** https://github.com/AlgebraicJulia/Decapodes.jl/blob/main/examples/climate/mpf.jl
- **Description:** Coupled system of NS vorticity dynamics and the Cahn-Hilliard
  phase-field equation, with composition-dependent viscosity via a sigmoid function.
  Distinct from the individual NS and Cahn-Hilliard leaderboard entries.

---

## Already in Leaderboard

For reference, these doc pages are already represented in the leaderboard records:

| Leaderboard Entry | Doc/Source |
|---|---|
| Cahn-Hilliard | `ch/cahn-hilliard.md` |
| Brusselator (all variants) | `brussel/brussel.md` |
| Gray-Scott | `examples/chemistry/gray_scott.md` |
| Halfar / CISM v2.1 | `cism/cism.md` |
| Budyko-Sellers | `examples/climate/budyko_sellers.jl` |
| Navier-Stokes Vorticity | `navier_stokes/ns.md` |
| Nonhydrostatic Buoyant Seawater | `nhs/nhs_lite.md` |
| Porous Convection | `pconv/porous_convection.md` |
| Klausmeier | `klausmeier/klausmeier.md` (in plots) |
| Gompertz oncology | `examples/oncology/...` (in plots/diagrams) |

## Borderline Cases

- **Harmonics** (`harmonics/harmonics.md`): Demonstrates spectral analysis
  (eigenvalues/eigenvectors of the Laplacian on a sphere). Mathematical tooling
  tutorial rather than a physics simulation proper.
- **Halfar Calibration** (`calibrate/calibration.md`): Calibrates Halfar model
  parameters via SciML optimization. Methodology tutorial, not a new physics model.
- **Ice Dynamics** (`ice_dynamics/ice_dynamics.md`): Reference documentation for the
  Halfar model; covered by the existing CISM v2.1 leaderboard entry.
