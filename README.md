# PKI-Based 2FA Microservice

A secure microservice implementing two-factor authentication using RSA encryption and TOTP codes, containerized with Docker.

## Features

- RSA 4096-bit encryption for secure seed transmission
- TOTP-based 2FA code generation and verification
- REST API endpoints for decryption, generation, and verification
- Persistent storage with Docker volumes
- Automated cron job for logging 2FA codes
- Multi-stage Docker build for optimization

## Setup

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

### Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Generate RSA keys
4. Download instructor public key
5. Request encrypted seed from API
6. Build Docker image: `docker-compose build`
7. Run container: `docker-compose up -d`

## API Endpoints

- `POST /decrypt-seed` - Decrypt encrypted seed
- `GET /generate-2fa` - Generate current TOTP code
- `POST /verify-2fa` - Verify TOTP code
- `GET /health` - Health check

## Student Information

- **Name**: Naveena Kemburu
- **Roll No**: 23P31A1207

## License

MIT
