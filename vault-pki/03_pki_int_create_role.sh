#!/bin/sh
set -o xtrace
export VAULT_ADDR=https://vault.example.az:8200
export VAULT_TOKEN=root
export VAULT_SKIP_VERIFY=true

#create a role to generate new certificates
vault write pki_int/roles/example-dot-az \
        allowed_domains="example.az" \
        allow_subdomains=true \
        max_ttl="720h"

#delete a role to generate new certificates
#vault delete pki_int/roles/example-dot-az