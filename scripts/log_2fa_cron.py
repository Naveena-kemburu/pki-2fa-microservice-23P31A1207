#!/usr/bin/env python3
import os
import sys
from datetime import datetime, timezone

# Add parent directory to path to import crypto_utils
sys.path.insert(0, '/app')

try:
    from crypto_utils import generate_totp_code
    
    # Read the stored seed
    seed_file = '/data/seed.txt'
    if not os.path.exists(seed_file):
        print(f"Error: Seed file not found at {seed_file}", file=sys.stderr)
        sys.exit(1)
    
    with open(seed_file, 'r') as f:
        hex_seed = f.read().strip()
    
    # Generate TOTP code
    code = generate_totp_code(hex_seed)
    
    # Get current UTC timestamp
    utc_time = datetime.now(timezone.utc)
    timestamp = utc_time.strftime('%Y-%m-%d %H:%M:%S')
    
    # Log to file
    log_file = '/cron/last_code.txt'
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    with open(log_file, 'a') as f:
        f.write(f"{timestamp} - 2FA Code: {code}\n")
    
    print(f"{timestamp} - 2FA Code: {code}")

except Exception as e:
    print(f"Error in cron job: {str(e)}", file=sys.stderr)
    sys.exit(1)
