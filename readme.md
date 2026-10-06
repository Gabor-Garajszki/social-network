# Network Analysis & Agent-Based Modeling

A Python toolkit for simulating, analyzing, and visualizing complex network structures. This repository includes both classic random graph theory experiments (Erdős–Rényi) and an agent-based stochastic network dynamic model based on homophily and triadic closure.

---

## Overview

The repository consists of two core simulations:

1. **Erdős–Rényi Random Graph Analysis (`erdosrenyi.py`)**
   - Implements $G(n, p)$ random graph generation.
   - Evaluates degree distributions, connected components, and percolation/giant component emergence.
   - Executes Monte Carlo experiments across multiple realizations to aggregate empirical statistics.
   - Provides a comprehensive 6-panel analytical visualization dashboard.

2. **Agent-Based Stochastic Network Formation (`stochastic.py`)**
   - Simulates a dynamic social network of agents with multidimensional binary traits.
   - Models link formation driven by **trait homophily** and **triadic closure**.
   - Includes edge weight reinforcement, temporal tie decay, and weight-based tie pruning.
   - Generates and renders a localized **ego network** around the highest-degree agent.

---

## Installation

Ensure you have Python 3.8+ installed. Install the required dependencies using `pip`:

```bash
pip install networkx matplotlib numpy
```

---

## Usage

### 1. Erdős–Rényi Model
Run the script to execute the Monte Carlo runs and display the diagnostic dashboard:

```bash
python erdosrenyi.py
```

### 2. Stochastic Agent-Based Model
Run the simulation to generate agent interactions and inspect the ego network visualization:

```bash
python stochastic.py
```

---

## File Structure

```text
.
├── erdosrenyi.py    # Erdős–Rényi model, component analysis, and Monte Carlo engine
├── stochastic.py    # Trait homophily, triadic closure, and ego-network visualization
└── README.md        # Project documentation
```

---

## License

This project is licensed under the MIT License.