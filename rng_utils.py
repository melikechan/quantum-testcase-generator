import config
import qiskit
from qiskit_ibm_runtime import QiskitRuntimeService

num_qubits = 32


def init_runtime():
    global runtime
    global backend
    # Load the IBM Quantum Runtime service
    runtime = QiskitRuntimeService(
        channel="ibm_quantum", token=config.quantumPlatformToken)
    backend = runtime.backend("ibmq_qasm_simulator")

# Quantum circuit to generate random numbers, classical register to store the results


def init_circuit():
    global qreg, creg, circ
    qreg = qiskit.QuantumRegister(num_qubits)
    creg = qiskit.ClassicalRegister(num_qubits)
    circ = qiskit.QuantumCircuit(qreg, creg)


# Generate multiple random numbers in the range [l, r].
# The number of random numbers to generate is specified by num_numbers.
def get_random_number(l: int, r: int, num_numbers: int = 1) -> list:
    # Generate a 32 bit random number
    circ.h(qreg)
    circ.measure(qreg, creg)

    # Execute the circuit using the IBM Quantum Runtime
    job = backend.run(circ, shots=num_numbers)
    results = [k for k, v in job.result(
    ).results[0].data.counts.items() if v == 1]

    # Convert the results to integers and scale them to the desired range
    results = [l + int(result, 16) % (r - l + 1) for result in results]

    return results


if __name__ == "__main__":
    init_runtime()
    init_circuit()
    # print(get_random_number(0, 100, 10))
