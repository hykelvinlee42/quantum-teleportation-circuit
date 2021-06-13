from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.extensions import Initialize
from qiskit import IBMQ, Aer, transpile, assemble
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import matplotlib.pyplot as plt

# Create 1-qubit state
psi = [0.45936609+0.56725257j, 0.40025413+0.55407937j] #set qubit state
#psi = [0.60275+0.62458j, 0.39451+0.30158j] #set qubit state

# Show the qubit on a Bloch sphere
plot_bloch_multivector(psi)
#plt.show()
init_gate = Initialize(psi)

init_gate.label = "init"

inverse_init_gate = init_gate.gates_to_uncompute()

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
    teleportation_circuit = QuantumCircuit(quantum_register, classical_registerz, classical_registerx)

    # sender owns q0 and receiver owns q1
    sender_qubit_id = 1
    receiver_qubit_id = 2
    third_party_qubit_id = 0

    
    teleportation_circuit.append(init_gate, [0])
    teleportation_circuit.barrier()

    entangle_qubits(teleportation_circuit, [sender_qubit_id, receiver_qubit_id])  # entangle qubits q0 and q1
    teleportation_circuit.barrier()

    sender_gate(teleportation_circuit, third_party_qubit_id, sender_qubit_id)
    teleportation_circuit.barrier()
    meansure_and_send(teleportation_circuit, third_party_qubit_id, sender_qubit_id)
    teleportation_circuit.barrier()
    receiver_gate(teleportation_circuit, receiver_qubit_id, classical_registerz, classical_registerx)

    #teleportation_circuit.append(inverse_init_gate, [2])
    #cr_result = ClassicalRegister(1)
    #teleportation_circuit.add_register(cr_result)
    #teleportation_circuit.measure(2,2)

    #teleportation_circuit.draw(output="mpl")
    #teleportation_circuit.draw()
    #plt.show()

    #Statevector Simulator
    sv_sim = Aer.get_backend('statevector_simulator')
    qobj = assemble(teleportation_circuit)
    out_vector = sv_sim.run(qobj).result().get_statevector()
    plot_bloch_multivector(out_vector)

    teleportation_circuit.draw(output="mpl")
    plt.show()

if __name__ == "__main__":
    create_teleportation_circuit()
