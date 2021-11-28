#!/bin/sh
set -o xtrace
export KUBECONFIG=$(pwd)/.kube/config.yml

# approle secretid
secret_id="l25256bb-1f2y-f464-6724-ca86d05250h7"

# installing cert-manager on kubernetes environment
kubectl apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v0.15.2/cert-manager.crds.yaml
helm upgrade --install cert-manager cert-manager --repo https://charts.jetstack.io --kubeconfig $KUBECONFIG --namespace cert-manager --create-namespace

# waiting for the cert-manager deployment to finish
kubectl rollout status deployment -n cert-manager cert-manager
kubectl rollout status deployment -n cert-manager cert-manager-webhook

# installing cert-manager on kubernetes environment
helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace

# waiting for the ingress-nginx deployment to finish
kubectl rollout status deployment -n ingress-nginx ingress-nginx-controller

# kubernetes secret for approle's secred id
secret_id_base64=$(echo -n "$secret_id" | base64)
sed  -e "s/secret_id/$role_id_base64/g" ./approle_secret.yaml
kubectl apply -f approle_secret.yaml

# clusterissuer for vault.
# in the caBundle, must be written the vault's (https://vault.example.az:8200) public certificate with base64
kubectl apply -f vault_cluster_issuer.yaml

# create certificate
kubectl apply -f certificate.yaml

# deploying application
kubectl apply -f application.yaml

