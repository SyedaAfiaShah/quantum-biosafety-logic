# 🧬 Quantum Logic Simulation of a Biosafety Decision System in a “Pollutant-Eating” Biospray

## 🧠 Project Overview

This project demonstrates how biological decision-making logic, originally designed for a synthetic biology biospray, can be represented through **quantum logic circuits** using **Qiskit**.

The concept is inspired by the **Pollutant-Eating Biospray Project**, where harmless engineered bacteria are programmed to detect and degrade toxic airborne pollutants (like soot-borne polycyclic aromatic hydrocarbons, *PAHs*).  
These bacteria act as microscopic cleaners that activate when pollutants are present and deactivate or self-destruct when safety rules are violated.

This repository explores how the **biosafety control logic** used in such a biological system can be modeled and simulated on a quantum computer.

## ⚙️ Biological Inspiration

In the biospray design, each bacterial cell follows a simple decision-making process:

- ✅ **Survive** if pollutants are detected (normal condition).  
- 🔁 **Replicate** only in controlled conditions.  
- 💀 **Self-destruct (kill signal)** if:
  - **T (Timer):** The bacterium has not detected pollutants for too long.  
  - **M (Mutation):** Genetic damage or mutation is detected.  
  - **G (Geosensing):** The bacterium drifts outside a predefined safe geography.

The biosafety rule can be summarized as:


K = T + M + G


where **K** is the kill signal (**1 = terminate**, **0 = survive**).

This rule is implemented as a **quantum circuit** that models the same logical relationships in a reversible, computational way.


## 💻 Quantum Logic Model

In this project, we map each biological input to a **quantum bit (qubit)** and use **quantum gates** to reproduce the logic of the biosafety kill-switch.

| Biological Signal        | Symbol | Qubit | Description                              |
|---------------------------|:------:|:------:|------------------------------------------|
| Mutation detected         | M      | q₀     | Triggers kill signal if true             |
| Timer expired (pollutant absent) | T | q₁     | Triggers kill signal after delay         |
| Geosensing out of range   | G      | q₂     | Detects unsafe environment               |
| Kill output               | K      | q₄     | Activated when any trigger = 1           |

## 🔬 Implementation Details

The simulation is implemented in **Python** using the **Qiskit** quantum computing framework.

### Core Features
- Construction of a reversible quantum circuit for the biosafety rule.  
- Classical vs Quantum truth table comparison.  
- Quantum superposition simulation to explore all input states simultaneously.  
- Noisy backend simulation to test performance under real hardware-like errors.  
- Histogram visualizations for probability outcomes.

## 🧩 Circuit Logic

The quantum circuit uses:
- **CNOT (CX)** gates to propagate single-input signals.  
- **Toffoli (CCX)** gates to handle multi-input logic combinations.  
- **Hadamard (H)** gates to introduce quantum superposition across input states.

These gates work together to compute:

K = T + M + G

The circuit remains **reversible**, meaning that no information is destroyed, just like in biological regulation, where signals can be reversed or overridden under controlled feedback.


## 📊 Simulations

The notebook runs three key simulations:

1. **Classical vs Quantum Truth Table**  
   Compares deterministic (classical) logic output with probabilistic quantum results for all input combinations of M, T, and G.

2. **Quantum Superposition Simulation**  
   Places all input qubits in superposition using Hadamard gates to visualize the full outcome distribution of possible environmental conditions.

3. **Noisy Quantum Simulation**  
   Adds realistic hardware noise using Qiskit’s Aer noise model.  
   This mirrors biological uncertainty, just as bacteria experience imperfect sensing or environmental fluctuations.

## 🧠 Insights

- **Ideal Circuit:** Produces perfect results where the kill signal activates for any safety violation.  
- **Noisy Simulation:** Demonstrates probabilistic deviations, similar to biological “noise” or imperfect gene regulation.  

**Takeaway:** Biological safety circuits and quantum logic both rely on conditional decision-making and redundancy for robustness.

## 🔗 Related Project

This quantum simulation was inspired by the larger **Synthetic Biology Biospray Project**, where engineered *Pseudomonas putida* bacteria detect and degrade air pollutants while maintaining biosafety through built-in regulation logic.

👉 **View the full project:** [Biospray Project on Notion](https://awake-pot-132.notion.site/SynBio-Project-Engineering-a-PAH-Detecting-and-Degrading-Biospray-Using-Pseudomonas-putida-275d15e7a8e480c58c18f95504988d2e?source=copy_link&authuser=0)

---

## 🧰 Requirements

- Python 3.9+  
- Qiskit  
- Matplotlib  
- Pandas  
- NumPy  

Install dependencies using:

```bash
pip install qiskit qiskit-aer matplotlib pylatexenc pandas numpy
