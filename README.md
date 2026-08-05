# PQC Security Evaluation Framework

A research-oriented framework for evaluating classical and post-quantum cryptographic algorithms through performance benchmarking, security classification, and comparative analysis.

## Overview

The development of quantum computers introduces a potential threat to widely deployed public-key cryptographic systems.

This project focuses on analyzing the impact of quantum computing on classical cryptographic algorithms and evaluating post-quantum cryptographic alternatives by comparing their performance characteristics, key sizes, signature sizes, and security properties.

The framework provides an automated evaluation pipeline that performs cryptographic benchmarks, analyzes security properties, and generates comparative reports.

## Objectives

- Analyze the vulnerability of classical public-key cryptographic algorithms against quantum attacks.
- Evaluate post-quantum cryptographic signature schemes.
- Compare performance characteristics through experimental benchmarking.
- Measure key generation, signing, and verification performance.
- Analyze key and signature size overhead.
- Generate automated comparative reports.

## Evaluated Algorithms

## Classical Algorithms

### RSA

- Cryptographic family: Classical public-key cryptography
- Security basis: Integer factorization problem
- Quantum resistant: No

### ECDSA

- Cryptographic family: Elliptic curve cryptography
- Security basis: Elliptic Curve Discrete Logarithm Problem
- Quantum resistant: No


## Post-Quantum Algorithms

### ML-DSA (Dilithium)

- Cryptographic family: Lattice-based cryptography
- Security basis: Module lattice problem
- Quantum resistant: Yes
- NIST standardized post-quantum signature scheme


### SPHINCS+

- Cryptographic family: Hash-based cryptography
- Security basis: Hash function security
- Quantum resistant: Yes
- NIST standardized post-quantum signature scheme


## Framework Architecture


Cryptographic Algorithms
|
v
Benchmark Engine
|
v
Performance Metrics Collection
|
+----------------------+
| |
v v
Security Analysis Comparative Analysis
|
v
Automated Report Generation



## Benchmark Metrics

The framework evaluates each algorithm based on:

### Performance Metrics

- Key generation time
- Signing time
- Verification time
- Standard deviation across multiple benchmark runs


### Size Metrics

- Public key size
- Private key size
- Signature size


### Security Metrics

- Cryptographic family classification
- Security foundation
- Quantum resistance status
- NIST standardization status


## Generated Reports

The framework automatically generates:


results/

├── benchmark_results.json
├── comparative_summary.json
└── comparative_summary.txt


Generated reports include:

- Complete benchmark measurements
- Classical algorithm comparison
- Post-quantum algorithm comparison
- Security classification
- Signature size analysis


## Project Structure


src/

├── algorithms/
├── benchmarks/
├── analysis/
└── visualization/

results/

├── benchmark_results.json
├── comparative_summary.json
├── comparative_summary.txt
└── generated plots



## Installation

Install project dependencies:

```bash
pip install -r requirements.txt

Activate the virtual environment:

source .venv/bin/activate
Usage

Run the complete evaluation pipeline:

python -m src.main

The framework will automatically:

Execute cryptographic benchmarks.
Store experimental results.
Perform security analysis.
Generate comparative reports.
Research Context

This framework was developed as part of a thesis project focusing on post-quantum cryptography and the transition from classical cryptographic systems to quantum-resistant alternatives.
