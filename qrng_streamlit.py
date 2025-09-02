import streamlit as st
from qiskit import QuantumCircuit, Aer, execute
import matplotlib.pyplot as plt
import math
import random
import base64

# Function to generate quantum bits using Hadamard gate
def generate_quantum_bits(num_bits=128):
    qc = QuantumCircuit(1, 1)
    backend = Aer.get_backend('qasm_simulator')
    qc.h(0)
    qc.measure(0, 0)
    job = execute(qc, backend, shots=num_bits)
    result = job.result()
    counts = result.get_counts()
    bitstream = ''.join(random.choices(['0', '1'], weights=[counts.get('0', 0), counts.get('1', 0)], k=num_bits))
    return bitstream

# Von Neumann extractor
def von_neumann_extractor(raw_bits):
    extracted = ''
    for i in range(0, len(raw_bits)-1, 2):
        pair = raw_bits[i:i+2]
        if pair == '01':
            extracted += '1'
        elif pair == '10':
            extracted += '0'
    return extracted

# Shannon entropy calculation
def calculate_entropy(bits):
    if not bits:
        return 0.0
    p0 = bits.count('0') / len(bits)
    p1 = bits.count('1') / len(bits)
    entropy = 0
    if p0 > 0:
        entropy -= p0 * math.log2(p0)
    if p1 > 0:
        entropy -= p1 * math.log2(p1)
    return entropy

# Generate random OTP
def generate_otp(bits, digits=6):
    if len(bits) < digits * 4:
        return "Not enough bits"
    decimal_value = int(bits[:digits*4], 2)
    return str(decimal_value % (10**digits)).zfill(digits)

# Generate 128-bit encryption key (hex)
def generate_encryption_key(bits):
    if len(bits) < 128:
        return "Not enough bits"
    key = bits[:128]
    hex_key = hex(int(key, 2))[2:].zfill(32)
    return hex_key

# Generate password salt (base64)
def generate_salt(bits, length=16):
    if len(bits) < length * 8:
        return "Not enough bits"
    byte_array = int(bits[:length*8], 2).to_bytes(length, byteorder='big')
    return base64.b64encode(byte_array).decode('utf-8')

# Streamlit app layout
st.title("🔐 Quantum Random Number Generator (QRNG) - Prototype")
st.markdown("Built using Qiskit, Streamlit | Showcasing applications in Cybersecurity")

if st.button("⚛ Generate Quantum Random Bits"):
    raw = generate_quantum_bits(256)
    extracted = von_neumann_extractor(raw)
    entropy_score = calculate_entropy(extracted)

    st.subheader("🧪 Random Bitstream (Extracted)")
    st.code(extracted[:128] + "..." if len(extracted) > 128 else extracted)

    st.subheader("📊 Entropy Score")
    st.metric(label="Shannon Entropy", value=f"{entropy_score:.4f}", delta="Max = 1.0")

    st.subheader("🔐 Cybersecurity Simulations")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.caption("AES Key (128-bit)")
        st.code(generate_encryption_key(extracted))
    with col2:
        st.caption("6-digit OTP")
        st.code(generate_otp(extracted))
    with col3:
        st.caption("Password Salt")
        st.code(generate_salt(extracted))
