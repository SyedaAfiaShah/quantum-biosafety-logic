from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.visualization import plot_histogram
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error, ReadoutError
from itertools import product
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

# --------------------------- Setup ---------------------------
plt.rcParams["figure.dpi"] = 120
# ---------- Classical kill rule ----------
def kill_rule_classical(mutation, timer, geosense):
    """
    Classical kill rule for biospray safety logic.
    K = T OR M OR G
    """
    return int(mutation or timer or geosense)

# ---------- Build reversible quantum circuit ----------
def build_reversible_kill_circuit():
    """
    Build a reversible quantum circuit implementing:
        K = T OR M OR G
    using basic quantum logic gates.
    Qubit mapping:
        q0 = M (Mutation)
        q1 = T (Timer)
        q2 = G (Geosensing)
        q3 = Ancilla
        q4 = K (Kill output)
    """
    qr = QuantumRegister(5, "q")
    cr = ClassicalRegister(1, "c")  # measure kill outpu
    qc = QuantumCircuit(qr, cr)

    # Step 1: Initialize kill bit to 0
    qc.reset(qr[4])

    # Step 2: XOR inputs into output (sets kill=1 when odd number of inputs 1)
    qc.cx(qr[0], qr[4])
    qc.cx(qr[1], qr[4])
    qc.cx(qr[2], qr[4])

    # Step 3: Toffoli gates correct parity to form proper OR (1 if any input = 1)
    qc.ccx(qr[0], qr[1], qr[4])
    qc.ccx(qr[0], qr[2], qr[4])
    qc.ccx(qr[1], qr[2], qr[4])

    return qc, qr, cr

# ---------- Quantum truth table ----------
def evaluate_truth_table_quantum():
    backend = AerSimulator()
    qc_base, qr, cr = build_reversible_kill_circuit()
    rows = []

    for mutation, timer, geosense in product([0, 1], repeat=3):
        qc = qc_base.copy()
        prep = QuantumCircuit(qr, cr)
        if mutation:
            prep.x(qr[0])
        if timer:
            prep.x(qr[1])
        if geosense:
            prep.x(qr[2])

        full = prep.compose(qc)
        full.measure(qr[4], cr[0])

        compiled = transpile(full, backend)
        res = backend.run(compiled, shots=1024).result()
        counts = res.get_counts()

        total_shots = sum(counts.values())
        prob_kill = sum(
            cnt for bitstring, cnt in counts.items() if bitstring[0] == "1"
        ) / total_shots

        rows.append(
            {
                "Mutation": mutation,
                "Timer": timer,
                "Geosensing": geosense,
                "Quantum_Prob_Kill": prob_kill,
                "Classical_Kill": kill_rule_classical(mutation, timer, geosense),
            }
        )

    df = pd.DataFrame(rows)
    return df

# ---------- Quantum Superposition Simulation ----------
def superposition_counts(noisy=False, noise_model=None):
    qc_base, qr, _ = build_reversible_kill_circuit()
    cr = ClassicalRegister(5, "c")  # ✅ FIX: create 5 classical bits
    prep = QuantumCircuit(qr, cr)
    prep.h([qr[0], qr[1], qr[2]])  # put all inputs in superposition
    full = prep.compose(qc_base)
    full.measure([qr[4], qr[3], qr[2], qr[1], qr[0]], range(5))  # ✅ now valid

    backend = AerSimulator()
    compiled = transpile(full, backend)
    job = backend.run(compiled, shots=4096, noise_model=noise_model if noisy else None)
    return job.result().get_counts()

# ---------- Noise Model ----------
def build_simple_noise_model(p1=0.002, p2=0.02, readout_err=0.03):
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(
        depolarizing_error(p1, 1), ["u1", "u2", "u3", "x", "h"]
    )
    noise_model.add_all_qubit_quantum_error(depolarizing_error(p2, 2), ["cx"])
    noise_model.add_all_qubit_quantum_error(depolarizing_error(p2 * 1.5, 3), ["ccx"])
    readout = ReadoutError(
        [[1 - readout_err, readout_err], [readout_err, 1 - readout_err]]
    )
    noise_model.add_all_qubit_readout_error(readout)
    return noise_model

# ---------- Helper: Plotting Function ----------
def plot_counts(counts_dict, title, save=False):
    if not counts_dict:
        print("No data to plot for", title)
        return
    labels = list(counts_dict.keys())
    values = list(counts_dict.values())

    plt.figure(figsize=(8, 4))
    plt.bar(range(len(labels)), values, tick_label=labels)
    plt.xticks(rotation=45, ha="right")
    plt.title(title)
    plt.xlabel("Output state (bitstring)")
    plt.ylabel("Counts")
    plt.tight_layout()
    plt.show()

    if save:
        os.makedirs("plots", exist_ok=True)
        plt.savefig(f"plots/{title.replace(' ', '_')}.png", dpi=300, bbox_inches="tight")
        print(f"Saved: plots/{title.replace(' ', '_')}.png")


# --------------------------- MAIN ---------------------------
if __name__ == "__main__":
    print("1️⃣ Classical vs Quantum truth table (ideal simulator):")
    df = evaluate_truth_table_quantum()
    print(df.to_string(index=False))

    print("\n2️⃣ Quantum superposition counts (ideal):")
    counts = superposition_counts(noisy=False)
    print("Sample:", list(counts.items())[:5])
    plot_counts(counts, "Quantum Superposition (Ideal)")

    print("\n3️⃣ Quantum superposition counts (noisy):")
    noise = build_simple_noise_model()
    noisy_counts = superposition_counts(noisy=True, noise_model=noise)
    print("Sample:", list(noisy_counts.items())[:5])
    plot_counts(noisy_counts, "Quantum Superposition (Noisy)")

    print("\n✅ All simulations completed successfully.")

