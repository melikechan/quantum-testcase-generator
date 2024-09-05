# Testcase Generator using Qiskit

Generate testcases for your competitive programming problems with the randomness of the qubits!

## Features

- Generate pseudo-random numbers using IBM fake providers (local simulators) and IBM Quantum Platform (real quantum computers).
  - It works through mapping the random number to the desired range.
  - However, the range is works **as expected** if the number is between $-2^{(n-1)}$ and $2^{(n-1)} - 1$. (where $n$ is the number of qubits, one bit is used for the sign)
- Generate random graphs with the number of nodes and edges.

**Important note:** In an 16GB RAM machine, maximum number of qubits with $10^5$ generated random numbers is **14**.

## Upcoming Features

- Using the random number generator, generate testcases, from arrays to graphs.
- Easy-to-describe, why would you change the code for every problem?

## Contributing

Pull requests are very welcome, you can create a pull request from the corresponding GitHub section.
