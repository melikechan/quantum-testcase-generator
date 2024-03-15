import config
import qiskit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

def init_runtime():
    global runtime
    global backend
    # Load the IBM Quantum Runtime service
    runtime = QiskitRuntimeService(channel="ibm_quantum", token=config.quantumPlatformToken)
    backend = runtime.backend("ibmq_qasm_simulator")


def get_random_number(l: int, r: int) -> int:
    # Generate a 32 bit random number
    num_qubits = 32

    qreg = qiskit.QuantumRegister(num_qubits)
    creg = qiskit.ClassicalRegister(num_qubits)
    circ = qiskit.QuantumCircuit(qreg, creg)

    circ.h(qreg)
    circ.measure(qreg, creg)

    # Execute the circuit using the IBM Quantum Runtime
    job = backend.run(circ, shots=1)
    result = [k for k, v in job.result().results[0].data.counts.items() if v == 1][0]

    # Convert the result to an integer
    result = int(result, 16)

    # Scale the result to the desired range
    result = l + result % (r - l + 1)
    
    return result


if __name__ == "__main__":
    init_runtime()
