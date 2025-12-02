import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
import subprocess

# 1. Get latest commit hash
commit_hash = subprocess.check_output(
    ["git", "log", "-1", "--format=%H"],
    text=True
).strip()

# 2. Load student private key (for signing)
with open("student_private.pem", "rb") as f:
    student_priv = serialization.load_pem_private_key(
        f.read(),
        password=None,
        backend=default_backend()
    )

# 3. Load instructor public key (for encrypting the signature)
with open("instructor_public.pem", "rb") as f:
    instructor_pub = serialization.load_pem_public_key(
        f.read(),
        backend=default_backend()
    )

# 4. Sign the commit hash with RSA-PSS-SHA256
signature = student_priv.sign(
    commit_hash.encode("utf-8"),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# 5. Encrypt the signature with instructor public key using RSA-OAEP-SHA256
ciphertext = instructor_pub.encrypt(
    signature,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# 6. Base64 encode and print single line
b64_cipher = base64.b64encode(ciphertext).decode("ascii")
print(b64_cipher)
