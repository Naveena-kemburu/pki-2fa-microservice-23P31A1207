# Complete Setup Guide for PKI-Based 2FA Microservice

## Student Information
- **Name**: Naveena Kemburu
- **Roll No**: 23P31A1207
- **Repository**: https://github.com/Naveena-kemburu/pki-2fa-microservice-23P31A1207

## Quick Setup (Run These Commands)

```bash
# 1. Clone the repository
git clone https://github.com/Naveena-kemburu/pki-2fa-microservice-23P31A1207.git
cd pki-2fa-microservice-23P31A1207

# 2. Create directories
mkdir -p scripts cron

# 3. Generate RSA Keys (4096-bit)
python3 << 'EOF'
from crypto_utils import generate_rsa_keypair, serialize_private_key, serialize_public_key

priv, pub = generate_rsa_keypair()

with open('student_private.pem', 'w') as f:
    f.write(serialize_private_key(priv))

with open('student_public.pem', 'w') as f:
    f.write(serialize_public_key(pub))

print("Keys generated successfully!")
EOF

# 4. Download instructor public key
curl https://partnr-public.s3.us-east-1.amazonaws.com/gpp-resources/instructor_public.pem -o instructor_public.pem

# 5. Commit keys to Git
git add student_private.pem student_public.pem instructor_public.pem
git commit -m "Add RSA keypair and instructor public key"
git push origin main
```

## Step-by-Step Instructions

### 1. Generate Encrypted Seed
Update the instructor API call with your student ID and GitHub URL, then run:

```python
import requests
import json

student_id = "23P31A1207"
github_repo = "https://github.com/Naveena-kemburu/pki-2fa-microservice-23P31A1207"

# Read your public key
with open('student_public.pem', 'r') as f:
    public_key = f.read()

payload = {
    "student_id": student_id,
    "github_repo_url": github_repo,
    "public_key": public_key
}

response = requests.post(
    "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws",
    json=payload
)

data = response.json()
with open('encrypted_seed.txt', 'w') as f:
    f.write(data['encrypted_seed'])

print("Encrypted seed saved!")
```

### 2. Create Remaining Files

Create app.py, Dockerfile, docker-compose.yml, and other files (see instructions below)

### 3. Build and Run

```bash
# Build Docker image
docker-compose build --no-cache

# Run container
docker-compose up -d

# Test endpoints
curl -X POST http://localhost:8080/decrypt-seed \
  -H "Content-Type: application/json" \
  -d "{\"encrypted_seed\":\"$(cat encrypted_seed.txt)\"}"

curl http://localhost:8080/generate-2fa

# Wait 70+ seconds for cron to execute
sleep 70
docker exec pki-2fa-app cat /cron/last_code.txt
```

## Important Files to Create

1. **app.py** - FastAPI application
2. **Dockerfile** - Multi-stage build
3. **docker-compose.yml** - Container configuration
4. **scripts/log_2fa_cron.py** - Cron job script
5. **.gitattributes** - Ensure LF line endings
6. **.gitignore** - Exclude encrypted_seed.txt

## Notes

- Never commit encrypted_seed.txt
- Always use the EXACT same GitHub URL for API and submission
- Ensure cron file has LF (Unix) line endings
- Test all endpoints before submission
- Generate commit proof with signature before submitting
