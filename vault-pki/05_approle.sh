#!/usr/bin/env bash
set -o xtrace
export VAULT_ADDR=https://vault.example.az:8200
export VAULT_SKIP_VERIFY=true
export VAULT_TOKEN=root

# enable approle method
vault auth enable approle

# create cert-manager-role approle
 vault write auth/approle/role/cert-manager-role \
    secret_id_ttl=10m \
    token_num_uses=10 \
    token_ttl=20m \
    token_max_ttl=30m \
    secret_id_num_uses=40

# get role-id from cert-manager-role approle
vault read auth/approle/role/cert-manager-role/role-id | grep role_id | awk '{print $2}' > role_id

# get secret-id for cert-manager-role approle
vault write -f auth/approle/role/cert-manager-role/secret-id | grep secret_id | awk '{print $2}' > secret_id

