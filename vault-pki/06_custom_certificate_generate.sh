#!/usr/bin/env bash
set -o xtrace
export VAULT_ADDR=https://vault.example.az:8200
export VAULT_SKIP_VERIFY=true
export VAULT_TOKEN=root

#set roleid and secretid as env variables from the previous step
role_id=$(cat role_id)
secret_id=$(cat secret_id)

curl -s  --request POST --data '{"role_id": "'"$role_id"'", "secret_id":"'"$secret_id"'"}'  ${VAULT_ADDR}/v1/auth/approle/login |  jq -r ".auth.client_token"  > user.token

#store the token as env variable, now this token can be used to authenticate against Vault
export VAULT_TOKEN=`cat user.token`

#Use the new token to generate a new certificate and store it in a file
vault write -format=json pki_int/issue/example-dot-az common_name=test.example.com > test.example.az.crt

#extract the certificate, issuing ca(intermediate) in the pem file and private key in the key file seperately
cat test.example.az.crt | jq -r .data.certificate > test.example.az.pem
cat test.example.az.crt | jq -r .data.issuing_ca >> test.example.az.pem
cat test.example.az.crt | jq -r .data.private_key > test.example.az.key

#list all certificates created by the intermediate CA
vault list pki_int/certs
vault list pki_int/certs > cert_key_list

#call the tidy API to clen up revoked certs
#vault write pki_int/tidy \
#   safety_buffer=5s \
#    tidy_cert_store=true \
#    tidy_revocation_list=true