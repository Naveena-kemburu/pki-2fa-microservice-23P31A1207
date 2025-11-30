import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend
import pyotp

def generate_rsa_keypair(key_size=4096):
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size, backend=default_backend())
    return private_key, private_key.public_key()

def serialize_private_key(private_key):
    pem = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.PKCS8, encryption_algorithm=serialization.NoEncryption())
    return pem.decode('utf-8')

def serialize_public_key(public_key):
    pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    return pem.decode('utf-8')

def load_private_key_from_pem(pem_data):
    if isinstance(pem_data, str):
        pem_data = pem_data.encode('utf-8')
    return serialization.load_pem_private_key(pem_data, password=None, backend=default_backend())

def load_public_key_from_pem(pem_data):
    if isinstance(pem_data, str):
        pem_data = pem_data.encode('utf-8')
    return serialization.load_pem_public_key(pem_data, backend=default_backend())

def decrypt_seed(encrypted_seed_b64, private_key):
    encrypted_seed = base64.b64decode(encrypted_seed_b64)
    decrypted_seed = private_key.decrypt(encrypted_seed, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    hex_seed = decrypted_seed.decode('utf-8')
    if len(hex_seed) != 64 or not all(c in '0123456789abcdef' for c in hex_seed):
        raise ValueError("Invalid seed")
    return hex_seed

def generate_totp_code(hex_seed):
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(base32_seed, digest=hashes.SHA1)
    return totp.now()

def verify_totp_code(hex_seed, code, valid_window=1):
    try:
        seed_bytes = bytes.fromhex(hex_seed)
        base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
        totp = pyotp.TOTP(base32_seed, digest=hashes.SHA1)
        return totp.verify(code, valid_window=valid_window)
    except:
        return False

def sign_message(message, private_key):
    message_bytes = message.encode('utf-8')
    signature = private_key.sign(message_bytes, padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
    return signature

def encrypt_with_public_key(data, public_key):
    ciphertext = public_key.encrypt(data, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    return ciphertext
