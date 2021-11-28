#!/bin/sh
set -o xtrace
export VAULT_ADDR=https://vault.example.az:8200
export VAULT_TOKEN=root
export VAULT_SKIP_VERIFY=true

##create a new policy to create update revoke and list certificates
vault policy write pki_int pki_int.hcl
