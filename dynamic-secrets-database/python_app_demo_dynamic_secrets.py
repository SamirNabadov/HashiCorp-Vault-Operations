import os, subprocess
import requests
import json
import shutup
import psycopg2

# Environment Variables
vault_address = os.getenv("VAULT_ADDR") or "https://vault.example.az:8200"
vault_token = os.getenv("VAULT_TOKEN") or "root"
vault_api = f'{vault_address}/v1/database/creds/readonly'
POSTGRES_HOST = "192.168.200.200"
POSTGRES_PORT = "5432"

def install_packages():
    cmd = "pip install -r requirements.txt"
    subprocess.call(cmd, shell=True, universal_newlines=True)

def disable_warings():
    shutup.please()

def get_secrets_from_vault():
    response_API = requests.get(vault_api, headers={'X-Vault-Token': vault_token}, verify=False).text
    reponse = json.loads(response_API)
    
    secrets = {
            'username': reponse['data']['username'],
            'password': reponse['data']['password']
        }
    return secrets

def main():

    disable_warings()
    install_packages()

    secret = get_secrets_from_vault()
    print(f"Database Username: {secret['username']}")
    print(f"Database Password: {secret['password']}")

    conn = psycopg2.connect(
        database="postgres", user=secret['username'], password=secret['password'], host=POSTGRES_HOST, port= POSTGRES_PORT
    )
    cursor = conn.cursor()
    cursor.execute("select version()")

    data = cursor.fetchone()
    print("Connection established to: ", data)
    conn.close()

if __name__== "__main__":
    main()

