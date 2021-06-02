from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
import matplotlib.pyplot as plt


def entangle_qubits(circuit, qubits_ids):
    # create entangle pair of qubits (bell pair)
    circuit.h(qubits_ids[0])  # Put first qubit into a \+> state
    circuit.cx(qubits_ids[0], qubits_ids[1])  # Apply CNOT gate with first qubit as control and second qubit as target


def sender_gate(circuit, psi_qubit_id, sender_qubit_id):
    circuit.cx(psi_qubit_id, sender_qubit_id)
    circuit.h(psi_qubit_id)


def meansure_and_send(circuit, psi_qubit_id, sender_qubit_id):
    circuit.measure(psi_qubit_id, 0)  # measure and assign to first classical bit
    circuit.measure(sender_qubit_id, 1)  # measure and assign to second classical bit


def receiver_gate(circuit, receiver_qubit_id, classical_registerz, classical_registerx):
    circuit.x(receiver_qubit_id).c_if(classical_registerx, 1)
    circuit.z(receiver_qubit_id).c_if(classical_registerz, 1)


def create_teleportation_circuit():
    # setup qubits and classical bits for quantum teleportation
    quantum_register = QuantumRegister(3, name="q")
    classical_registerz = ClassicalRegister(1, name="crz")
    classical_registerx = ClassicalRegister(1, name="crx")
    teleportation_circuit = QuantumCircuit(quantum_register, classical_registerx, classical_registerz)

    # sender owns q0 and receiver owns q1
    sender_qubit_id = 1
    receiver_qubit_id = 2
    third_party_qubit_id = 0

    entangle_qubits(teleportation_circuit, [sender_qubit_id, receiver_qubit_id])  # entangle qubits q0 and q1

    teleportation_circuit.barrier()
    sender_gate(teleportation_circuit, third_party_qubit_id, sender_qubit_id)
    teleportation_circuit.barrier()
    meansure_and_send(teleportation_circuit, third_party_qubit_id, sender_qubit_id)
    teleportation_circuit.barrier()
    receiver_gate(teleportation_circuit, receiver_qubit_id, classical_registerz, classical_registerx)

    teleportation_circuit.draw(output="mpl")
    plt.show()


if __name__ == "__main__":
    create_teleportation_circuit()
