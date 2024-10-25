import os
import hvac
import json

try:
    vault_addr = os.getenv('VAULT_ADDR')
    role_id = os.getenv('VAULT_ROLE_ID')
    secret_id = os.getenv('VAULT_SECRET_ID')
    previous_secrets_file = 'previous_secrets.json'

    # Initialize Vault client
    client = hvac.Client(url=vault_addr)
    client.auth.approle.login(role_id=role_id, secret_id=secret_id)

    # Fetch secrets
    secrets = client.secrets.kv.v2.read_secret_version(path='secret/azure')['data']['data']

    # Load previous secrets
    if os.path.exists(previous_secrets_file):
        with open(previous_secrets_file, 'r') as f:
            previous_secrets = json.load(f)
    else:
        previous_secrets = {}

    # Compare secrets
    if secrets != previous_secrets:
        # Save the new secrets
        with open(previous_secrets_file, 'w') as f:
            json.dump(secrets, f)
        print('Secrets have changed.')
        with open(os.environ['GITHUB_OUTPUT'], 'a') as gh_out:
            gh_out.write('trigger=true\n')
    else:
        print('No changes detected in secrets.')
        with open(os.environ['GITHUB_OUTPUT'], 'a') as gh_out:
            gh_out.write('trigger=false\n')
except Exception as e:
    print(f"Error occurred: {e}")
    exit(1)
