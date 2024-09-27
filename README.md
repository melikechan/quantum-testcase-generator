**NOTE: This implementation is not practical for general usage, see [object-to-tc](https://github.com/melikechan/object-to-tc) to see something usable.**

# Testcase Generator using Qiskit

Generate test cases for your competitive programming problems with the randomness of the qubits!

## Features

- Generate pseudo-random numbers using IBM fake providers (local simulators) and IBM Quantum Platform (real quantum computers).
  - It works by mapping the random number to the desired range.
  - However, the range is works **as expected** if the number is between $-2^{(n-1)}$ and $2^{(n-1)} - 1$. (where $n$ is the number of qubits, one bit is used for the sign)

- Generate random **integer arrays** with the specified length, range, and sum.
- Generate random graphs with the number of nodes and edges.

**Important note:** In a 16GB RAM machine, the maximum number of qubits with $10^5$ generated random numbers is **14**.

## Upcoming Features

- Using the random number generator, generate test cases, from arrays to graphs.
- Easy to describe, why would you change the code for every problem?

## Contributing

Pull requests are very welcome, you can create a pull request from the corresponding GitHub section.
