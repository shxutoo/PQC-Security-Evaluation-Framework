SECURITY_INFO = {

    "RSA": {
        "family": "Classical public-key cryptography",
        "security_basis": "Integer factorization problem",
        "quantum_resistant": False,
        "nist_status": "Not post-quantum standard"
    },

    "ECDSA": {
        "family": "Elliptic curve cryptography",
        "security_basis": "Elliptic Curve Discrete Logarithm Problem",
        "quantum_resistant": False,
        "nist_status": "Not post-quantum standard"
    },

    "MLDSA": {
        "family": "Lattice-based cryptography",
        "security_basis": "Module lattice problem",
        "quantum_resistant": True,
        "nist_status": "NIST standardized post-quantum signature"
    }

}


def get_security_info(algorithm):

    return SECURITY_INFO.get(
        algorithm,
        {
            "family": "Unknown",
            "security_basis": "Unknown",
            "quantum_resistant": False,
            "nist_status": "Unknown"
        }
    )
