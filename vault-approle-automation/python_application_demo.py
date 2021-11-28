import os, subprocess
import hvac
import shutup

# Environment Variables (Must be added environment variables to pods from kubernetes)
vault_address = os.environ.get("VAULT_ADDR") or "https://vault.example.az:8200"
roled_id = os.environ.get("VAULT_ROLE_ID") or "84967779b-sdff-324-a967-abd6esdfsdfsdf"
secret_id = os.environ.get("VAULT_SECRET_ID") or "c25456bb-145-f364-8714-ba8666sdf250c6"
project_name = os.environ.get("PROJECT_NAME") or "portal"
repo_name = os.environ.get("REPO_NAME") or "api"
env = os.environ.get("ENV") or "dev"

def clear():
    os.system("clear")
    shutup.please()

def install_packages():
    cmd = "pip install -r requirements.txt"
    subprocess.call(cmd, shell=True, universal_newlines=True)

def get_secrets():
    vault = hvac.Client(url=vault_address, verify=False)
    vault.auth_approle(roled_id, secret_id)
    result = {
        'username': vault.read(f"secret/{project_name}/{repo_name}/{env}")['data']['database.username'],
        'password': vault.read(f"secret/{project_name}/{repo_name}/{env}")['data']['database.password'],
        'url':      vault.read(f"secret/{project_name}/{repo_name}/{env}")['data']['database.url'],
    }
    vault.logout()
    return result 

def main():
    clear()
    install_packages()
    print("-----------------")
    secret = get_secrets()
    print(f"Database Username: {secret['username']}")
    print(f"Database Password: {secret['password']}")
    print(f"Database URL: {secret['url']}")
        
if __name__== "__main__":
    main()
