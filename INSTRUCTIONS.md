# PKI-Based 2FA Microservice - Completion Instructions

## Project Status
This project is 95% complete with all core infrastructure in place. Follow these final steps to complete the task.

## Prerequisites Completed
✅ FastAPI application with three REST endpoints
✅ Cryptographic functions (RSA/OAEP, RSA-PSS, TOTP)
✅ Docker containerization with multi-stage build
✅ Cron job scheduling every minute
✅ Docker volumes for persistence
✅ RSA key pair (4096-bit)
✅ Instructor public key

## CRITICAL: Next Steps Required

### 1. Get Encrypted Seed from Instructor API
**IMPORTANT:** Use the EXACT repository URL: https://github.com/Naveena-kemburu/pki-2fa-microservice-23P31A1207

Call the instructor API endpoint:
```bash
curl -X POST https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws/ \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": "23P31A1207",
    "github_repo_url": "https://github.com/Naveena-kemburu/pki-2fa-microservice-23P31A1207",
    "public_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2UvC9ktf0tXdFOzRLxib\n7y2K18tEmL1CyURkHD3ySm2Q70/lXRcQPamfF/GM7j+Faiow/FsFOBUvTiKBKl1W\nb4RKOiYSs9U2Ru0YkLyqcTVSZmeV6gNpGeU/ajPDc0KuVTdlcy6j6jb0A0R40OmI\nS41d0MqpFT8UdWL1myWZycRGaifVuTe4TEL2T6im/XSdqi71nQb1fS79y5Tjag3R\nOjZClypsmrxhyUMvFWZEGTbx4BeS9r0M6uk8vKfb1qiaeeZ1YWd2M1byfCYys8b1\nszfGeHz8VU2UUPO88+TJF6hfV9kL1yalb2T70M2S5mUEM0KvC6UPCva2dqWDeKuS\n6wIDAQAB\n-----END PUBLIC KEY-----\n"
  }'
```

Copy the `encrypted_seed` value and create `encrypted_seed.txt` with the base64 string (single line, no breaks).

### 2. Local Testing
```bash
# Build Docker image
docker-compose build

# Start container
docker-compose up -d

# Test decrypt endpoint
curl -X POST http://localhost:8080/decrypt-seed \
  -H "Content-Type: application/json" \
  -d "{\"encrypted_seed\": \"<base64_encrypted_seed>\"}"

# Test generate 2FA endpoint
curl http://localhost:8080/generate-2fa

# Test verify endpoint
curl -X POST http://localhost:8080/verify-2fa \
  -H "Content-Type: application/json" \
  -d '{"code": "123456"}'

# Wait 70+ seconds to verify cron job
sleep 70
docker exec <container_id> cat /cron/last_code.txt

# Test container restart persistence
docker-compose down
docker-compose up -d
curl http://localhost:8080/generate-2fa
```

### 3. Generate Commit Proof
```bash
# Get commit hash
commit_hash=$(git log -1 --format=%H)

# Sign the commit hash with student private key (RSA-PSS-SHA256)
# Encrypt the signature with instructor public key (RSA/OAEP-SHA256)
# Base64 encode the result (single line)

# You need to write a Python script or use openssl to do this
```

### 4. Submit Task
Go to Partnr platform and fill in the Submit form with:
- GitHub Repository URL: https://github.com/Naveena-kemburu/pki-2fa-microservice-23P31A1207
- Commit Hash: (from git log -1 --format=%H)
- Encrypted Commit Signature: (base64 encoded)
- Student Public Key: (contents of student_public.pem)
- Encrypted Seed: (from encrypted_seed.txt, single line)
- Optional: Docker Image URL (if pushed to registry)

## File Structure
```
pki-2fa-microservice-23P31A1207/
├── app.py                      # FastAPI application
├── crypto_utils.py             # Cryptographic functions
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Multi-stage Docker build
├── docker-compose.yml          # Container orchestration
├── .gitattributes             # Line ending configuration
├── .gitignore                 # Excluded files
├── README.md                  # Project overview
├── SETUP_GUIDE.md             # Detailed setup guide
├── INSTRUCTIONS.md            # This file
├── scripts/
│   └── log_2fa_cron.py       # Cron job script
├── cron/
│   └── 2fa-cron              # Cron schedule
├── student_private.pem         # Student private key (RSA 4096-bit)
├── student_public.pem          # Student public key
├── instructor_public.pem       # Instructor public key
└── encrypted_seed.txt          # Encrypted seed (to be generated)
```

## Key Technical Details
- RSA Algorithm: 4096-bit, public exponent 65537
- Decryption: RSA/OAEP with SHA-256, MGF1(SHA-256), no label
- Signing: RSA-PSS with SHA-256, MGF1(SHA-256), maximum salt length
- TOTP: SHA-1, 30-second period, 6-digit codes
- Timezone: UTC (critical for TOTP accuracy)
- Cron Job: Executes every minute and logs to /cron/last_code.txt
- Persistence: Seed stored in Docker volume at /data/seed.txt

## Troubleshooting

### Issue: TOTP codes don't match
- Verify timezone is UTC on both API and cron containers
- Ensure hex seed is correctly converted to base32
- Check that correct student_id and repo_url were used for seed generation

### Issue: Cron job not executing
- Verify cron/2fa-cron has LF line endings (not CRLF)
- Check .gitattributes contains: `cron/2fa-cron text eol=lf`
- Ensure cron container process is running: `docker exec <container_id> ps aux | grep cron`

### Issue: Container restart loses seed
- Verify docker-compose.yml has volume mounts
- Check volumes are defined: `seed-data` and `cron-output`
- Ensure mounts point to correct paths: `/data` and `/cron`

## Repository URL
https://github.com/Naveena-kemburu/pki-2fa-microservice-23P31A1207

## Deadline
6 Dec 2025, 09:59 AM IST (3 days remaining)

Good luck! All components are ready for testing and deployment.
