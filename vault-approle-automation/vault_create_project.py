import os, sys, subprocess, shutil, base64
from tempfile import TemporaryDirectory

# Environment Variables
os.environ["VAULT_ADDR"] = "https://vault.example.az:8200"
os.environ["VAULT_TOKEN"] = "root"
os.environ["VAULT_SKIP_VERIFY"] = "true"

# Necessary Variables
vault_address = os.environ.get("VAULT_ADDR")
packages = ["vault"]
env_list = ["dev", 'uat', 'prod']
vault_secrets_folder = "./secrets_vault"
policy_folder = "./policies_vault"
kubernetes_secrets_folder = "./secrets_kubernetes"
kubernetes_secret_template = f"{kubernetes_secrets_folder}/secret.yaml"
repo_name_list = []

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

def replace_word(infile,old_word,new_word):
    if not os.path.isfile(infile):
        print ("Error on replace_word, not a regular file: " + infile)
        sys.exit(1)

    f1=open(infile,'r').read()
    f2=open(infile,'w')
    m=f1.replace(old_word,new_word)
    f2.write(m)

def put_secrets(vault_secrets_folder, project_name):
    if os.path.exists(vault_secrets_folder):
        for dirpath, dirnames, filenames in os.walk(vault_secrets_folder):
            for each_file in filenames:
                repo_name = dirpath.split("/", 2)[2]
                env = os.path.splitext(each_file)[0]
                cmd = f"vault kv put secret/{project_name}/{repo_name}/{env} @secrets_vault/{repo_name}/{env}.json"
                subprocess.call(cmd, shell=True, universal_newlines=True)
                repo_name_list.append(repo_name)
    else:
        print("secrets_vault directory is empty")

def approle_operation(project_name):
    with TemporaryDirectory() as tmp:
        for env in env_list:
            print("{} Enviroment".format(env))
            print("--- Policy file generating ..")

            policy_template = f"{policy_folder}/{env}.hcl"
            policy_file = f"{tmp}/{env}_policy"
    
            for repo_name in repo_name_list:
                shutil.copyfile(policy_template, policy_file)
                replace_word(policy_file, 'env_name', env)
                replace_word(policy_file, 'repo_name', repo_name)
                replace_word(policy_file, 'project_name', project_name)

            print("--- Policy creating ..")
            cmd = f"vault policy write {project_name}_{env} {policy_file}"
            subprocess.call(cmd, shell=True, universal_newlines=True)

            print("--- Approle auth method binding to policy..")
            cmd = f"vault write auth/approle/role/{project_name}_{env} bind_secret_id='true' policies={project_name}_{env}"
            subprocess.call(cmd, shell=True, universal_newlines=True)

            print("--- Approle Auth secrets generating:")
            cmd = f"vault read -format=yaml auth/approle/role/{project_name}_{env}/role-id"
            out_output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]

            print("--- Kubernetess secrets generating:")
            role_id = ""
            for line in out_output.split('\n'):
                if "role_id:" in line:
                    role_id = line.split(": ")[1]

            cmd = f"vault write -f -format=yaml auth/approle/role/{project_name}_{env}/secret-id"
            out_output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]

            secret_id = ""
            for line in out_output.split('\n'):
                if "secret_id:" in line:
                    secret_id = line.split(": ")[1]

            print(f"ROLE ID: {role_id} \nSECRET ID: {secret_id}")
            role_id_base64 = base64.b64encode(role_id.encode())
            secret_id_base64 = base64.b64encode(secret_id.encode())

            kubernetes_secret = kubernetes_secrets_folder + "/" + project_name + "_" + env + "_secret.yaml"

            shutil.copyfile(kubernetes_secret_template, kubernetes_secret)
            replace_word(kubernetes_secret, 'role_id', str(role_id_base64).split("'")[1])
            replace_word(kubernetes_secret, 'secret_id', str(secret_id_base64).split("'")[1])
            replace_word(kubernetes_secret, 'project_name', project_name)
            print(f"export kubernetes environment: \nkubectl apply -f ./{kubernetes_secrets_folder}/{project_name}_{env}_secret.yaml")

            print("--- Get temporary token for checking vault secret access from Vault UI:")
            cmd = f"vault write -f -format=yaml auth/approle/login role_id={role_id} secret_id={secret_id}"
            out_output = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True).communicate()[0]

            client_token = ""
            for line in out_output.split('\n'):
                if "client_token:" in line:
                    client_token = line.split(": ")[1]
            print(f"CLIENT TOKEN: {client_token}")

def main():
    clear()
    print("---------------------")
    check_package()
    print("---------------------")
    while True:
        choice = input("Do you want to create new project (y/n) : ")
        if 'y' in choice.lower():
            project_name = input("Please write the name of the project: ")
            put_secrets(vault_secrets_folder, project_name)
            approle_operation(project_name)
        elif 'n' in choice.lower():
            print("Exiting...")
            sys.exit(1)
        else:
            print("Invalid input... Please try again.")
        
if __name__== "__main__":
    main()