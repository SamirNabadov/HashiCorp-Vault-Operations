__Hashicorp Vault Operation__
================================

Vault operations based on Python and Bash scripts


__Configured__
------------
* Vault PKI
* Implementation of Vault PKI, Certmanager, Ingress in Kubernetes Cluster Environment
* Vault AppRole Automation
* Dynamic secrets database


__Basic settings__
------------
* Configuring Vault PKI,  generating Root Certificate Authority within Vault. All detailed steps were defined in bash script files as comment
* Nginx Ingress, Cert-Manager, Cert-Manager ClusterIssuer/Certificate and sample app which enabled ingress https endpoint are installed based on bash script
* Creating policies, secrets for each environment and implementing the AppRole mechanism with python script
* Implementation of Dynamic secrets database mechanism for PostgreSQL based on python script



Vault PKI
------------
`$ cd  vault-pki/`

`$ ./01_pki_root_ca_generate.sh`

`$ ./02_pki_intermediate_ca_generate.sh`

`$ ./03_pki_int_create_role.sh`

`$ ./04_pki_int_policy.sh`

`$ ./05_approle.sh`

`$ ./06_custom_certificate_generate.sh`

Implementation of Vault PKI, Certmanager, Ingress in Kubernetes Cluster Environment
------------
`$ cd  k8s-ingress-certmanager-vault-pki/`

`$ ./deploy.sh`

Vault AppRole Automation
------------
`$ cd  vault-approle-automation/`

`$ python3 vault_create_project.py`

`$ python3 python_application_demo.py`

Dynamic secrets database
------------
`$ cd  dynamic-secrets-database/`

`$ python3 python_app_demo_dynamic_secrets.py`



__Requirements__
------------
* Python 3.8
* Vault client
* Kubernetes Cluster Environment
* PostgreSQL database


__Author Information__
------------------

Samir Nabadov
