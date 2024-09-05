import config
import qiskit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2
from qiskit_ibm_runtime.fake_provider import FakeAuckland


class RandomNumberGenerator:
    num_qubits = 14  # For the sake of randomness, we can increase the number of qubits
    cloud_mode = False  # Use it at your own risk, it may cost you money.

    def __init__(self):
        self.init_runtime()
        self.init_circuit()

    def init_runtime(self):
        # Load the IBM Quantum Runtime service
        if self.cloud_mode:
            self.runtime = QiskitRuntimeService(
                channel="ibm_quantum", token=config.quantumPlatformToken
            )
            backends = self.runtime.backends(min_num_qubits=self.num_qubits)

            if len(backends) == 0:
                raise Exception("No backends available")

            self.backend = backends[0]
        else:
            self.backend = FakeAuckland()

    # Quantum circuit to generate random numbers, classical register to store the results
    def init_circuit(self):
        self.qreg = qiskit.QuantumRegister(self.num_qubits)
        self.creg = qiskit.ClassicalRegister(self.num_qubits)
        self.circ = qiskit.QuantumCircuit(self.qreg, self.creg)

    # Generate multiple random numbers in the range [l, r].
    # The number of random numbers to generate is specified by num_numbers.
    def get_random_number(self, l: int, r: int, num_numbers: int = 1) -> list:
        if l > r:
            raise Exception("Invalid range")

        if l < -(2 ** (self.num_qubits - 1)) or r > 2 ** (self.num_qubits - 1) - 1:
            raise Exception("Out of bounds")

        self.circ.h(self.qreg)
        self.circ.measure(self.qreg, self.creg)

        transpiled_circ = qiskit.transpile(self.circ, backend=self.backend)

        # Execute the circuit
        sampler = SamplerV2(self.backend)
        job = sampler.run([transpiled_circ], shots=num_numbers)
        if self.cloud_mode:
            result = job.result(timeout=60)
        else:
            result = job.result()[0].data.c0

        # Convert the results to integers and scale them to the desired range
        results = [
            (int(key[1:], 2) * (1 if key[0] == "0" else -1)) % (r - l + 1) + l
            for key in result.get_counts().keys()
        ]

        return results


if __name__ == "__main__":
    # Sample usage
    """
    rng = RandomNumberGenerator()
    a = rng.get_random_number(-(2**13), 2**13 - 1, 10)
    print(a)
    """
