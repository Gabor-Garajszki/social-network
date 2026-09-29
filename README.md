# Stochastic Network Analysis & Evolution Simulations

A Python-based framework implementing stochastic graph analysis, percolation phase transitions, and agent-based social network dynamics using `networkx`, `numpy`, and `matplotlib`.

## Overview

The repository contains two modular simulation modules:

### 1. Social Network Evolution (`stochastic.py`)
An agent-based stochastic simulation tracking the evolution of social ties across multidimensional attribute spaces:
- **Homophily-Driven Edge Formation:** Dynamic interaction probability weighted by agent trait similarity.
- **Triadic Closure Dynamics:** Transitive closure mechanics strengthening secondary social triangles.
- **Decay & Pruning:** Continuous exponential link weight decay with automated threshold pruning.
- **Ego-Network Visualization:** Focused spring-layout rendering centered on maximum weighted-degree agents.

### 2. Erdős–Rényi Phase Transition (`erdosrenyi.py`)
Empirical study of random graph percolation near the critical regime ($p \sim 1/N$):
- **Percolation Analysis:** Tracking giant component emergence across subcritical and supercritical regimes ($p = 1.5/N$).
- **Degree & Component Distribution:** Single-run visualization contrasted against aggregated Monte Carlo experiments (400 realizations).
- **Statistical Dashboard:** Automated calculation of median, mode, average degree, and component metrics.

## Requirements

- Python 3.9+
- `networkx`
- `numpy`
- `matplotlib`

Install dependencies via pip:
```bash
pip install networkx numpy matplotlib

## Usage Example
```bash
python stochastic.py
python erdosrenyi.py