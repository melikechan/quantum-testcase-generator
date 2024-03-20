import config
import qiskit
from qiskit_ibm_runtime import QiskitRuntimeService


class RandomNumberGenerator:
    num_qubits = 32
    def __init__(self):
        self.init_runtime()
        self.init_circuit()

    def init_runtime(self):
        # Load the IBM Quantum Runtime service
        self.runtime = QiskitRuntimeService(
            channel="ibm_quantum", token=config.quantumPlatformToken)
        self.backend = self.runtime.backend("ibmq_qasm_simulator")

    # Quantum circuit to generate random numbers, classical register to store the results
    def init_circuit(self):
        self.qreg = qiskit.QuantumRegister(self.num_qubits)
        self.creg = qiskit.ClassicalRegister(self.num_qubits)
        self.circ = qiskit.QuantumCircuit(self.qreg, self.creg)

    # Generate multiple random numbers in the range [l, r].
    # The number of random numbers to generate is specified by num_numbers.
    def get_random_number(self, l: int, r: int, num_numbers: int = 1) -> list:
        # Generate a 32 bit random number
        self.circ.h(self.qreg)
        self.circ.measure(self.qreg, self.creg)

        # Execute the circuit using the IBM Quantum Runtime
        job = self.backend.run(self.circ, shots=num_numbers)
        results = [k for k, v in job.result(
        ).results[0].data.counts.items() if v == 1]

        # Convert the results to integers and scale them to the desired range
        results = [l + int(result, 16) % (r - l + 1) for result in results]

        return results


if __name__ == "__main__":
    rng = RandomNumberGenerator()
    print(rng.get_random_number(0, 100, 10))    
    # print(get_random_number(0, 100, 10))
