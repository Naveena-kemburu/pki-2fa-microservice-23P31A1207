from fastapi import FastAPI, HTTPException
import os, time
from crypto_utils import decrypt_seed, generate_totp_code, verify_totp_code, load_private_key_from_pem

app = FastAPI()
PRIVATE_KEY_PATH, SEED_FILE_PATH = "/app/student_private.pem", "/data/seed.txt"

def get_private_key():
    with open(PRIVATE_KEY_PATH, 'r') as f:
        return load_private_key_from_pem(f.read())

@app.post("/decrypt-seed")
async def decrypt_seed_endpoint(data: dict):
    try:
        encrypted_seed = data.get("encrypted_seed")
        if not encrypted_seed:
            raise HTTPException(status_code=400, detail="Missing encrypted_seed")
        private_key = get_private_key()
        hex_seed = decrypt_seed(encrypted_seed, private_key)
        os.makedirs("/data", exist_ok=True)
        with open(SEED_FILE_PATH, 'w') as f:
            f.write(hex_seed)
        return {"status": "ok"}
    except HTTPException:
        raise
    except:
        raise HTTPException(status_code=500, detail="Decryption failed")

@app.get("/generate-2fa")
async def generate_2fa():
    try:
        if not os.path.exists(SEED_FILE_PATH):
            raise HTTPException(status_code=500, detail="Seed not decrypted yet")
        with open(SEED_FILE_PATH, 'r') as f:
            hex_seed = f.read().strip()
        code = generate_totp_code(hex_seed)
        valid_for = 30 - (int(time.time()) % 30)
        return {"code": code, "valid_for": valid_for}
    except HTTPException:
        raise
    except:
        raise HTTPException(status_code=500, detail="Failed to generate 2FA code")

@app.post("/verify-2fa")
async def verify_2fa(data: dict):
    try:
        code = data.get("code")
        if not code:
            raise HTTPException(status_code=400, detail="Missing code")
        if not os.path.exists(SEED_FILE_PATH):
            raise HTTPException(status_code=500, detail="Seed not decrypted yet")
        with open(SEED_FILE_PATH, 'r') as f:
            hex_seed = f.read().strip()
        is_valid = verify_totp_code(hex_seed, code)
        return {"valid": is_valid}
    except HTTPException:
        raise
    except:
        raise HTTPException(status_code=500, detail="Verification failed")

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
