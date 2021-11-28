import os, sys, subprocess

# Environment Variables
os.environ["VAULT_ADDR"] = "https://vault.example.az:8200"
os.environ["VAULT_TOKEN"] = "root"
os.environ["VAULT_SKIP_VERIFY"] = "true"

packages = ["vault"]

def clear():
    os.system("clear")

def check_package():
    for package in packages:
        rc = subprocess.call(['which', package])
        if rc == 0:
            print(f'{package} installed!')
        else:
            print(f'{package} missing in path!')
            sys.exit(1)

def main():

    clear()
    # Check vault package is exists
    check_package()

    # enable database secrets
    cmd = f"vault secrets enable database"
    subprocess.call(cmd, shell=True, stderr=subprocess.PIPE, universal_newlines=True)

    # configure the database secrets engine with the connection credentials for the Postgres database
    cmd = "vault write database/config/postgresql plugin_name=postgresql-database-plugin connection_url='postgresql://{{username}}:{{password}}@192.168.200.200:5432/postgres?sslmode=disable' allowed_roles=readonly username='postgres' password='postgres'"
    subprocess.call(cmd, shell=True, universal_newlines=True)

    # create the role named readonly that creates credentials with the readonly.sql
    cmd = "vault write database/roles/readonly db_name=postgresql creation_statements=@readonly.sql default_ttl=1h max_ttl=24h"
    subprocess.call(cmd, shell=True, universal_newlines=True)

    # read credentials from the readonly database role
    cmd = "vault read database/creds/readonly"
    subprocess.call(cmd, shell=True, universal_newlines=True)
    print("---------------------------------------------------------")

    # create a Vault password policy named database with the password policy rules defined in password_policy.hcl
    cmd = "vault write sys/policies/password/database policy=@password_policy.hcl"
    subprocess.call(cmd, shell=True, universal_newlines=True)
    print("---------------------------------------------------------")

    # force delete all db connections and disable database secret
    #cmd = "vault lease revoke -f -prefix database/creds/"
    #subprocess.call(cmd, shell=True, universal_newlines=True)
    #cmd = "vault secrets disable database"
    #subprocess.call(cmd, shell=True, universal_newlines=True)

if __name__== "__main__":
    main()