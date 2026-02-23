# Federation Profile Configuration

This document provides implementation details for the [https_web](federation-profiles.md#profile-1-https_web) and [https_spiffe](federation-profiles.md#profile-2-https_spiffe) federation bundle profiles. For profile comparison and selection guidance, see [Federation Bundle Profiles](federation-profiles.md).

---

## Side-by-Side Configuration

### https_web Configuration

**Prerequisites:**

```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.19.1/cert-manager.yaml

# Wait for cert-manager to be ready
kubectl wait --for=condition=Available --timeout=300s \
  -n cert-manager deployment/cert-manager

# Configure ClusterIssuer for Let's Encrypt
kubectl apply -f - <<EOF
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt
spec:
  acme:
    server: https://acme-v02.api.letsencrypt.org/directory
    email: your-email@example.com
    privateKeySecretRef:
      name: letsencrypt-account-key
    solvers:
    - http01:
        ingress:
          class: nginx
EOF

# Verify ClusterIssuer is ready
kubectl get clusterissuer letsencrypt -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}'
# Expected output: True

# Configure DNS (required for Let's Encrypt validation)
# Create A record: spire.example.com → <ingress-external-ip>
# Verify DNS propagation:
nslookup spire.example.com
```

**SPIRE Server Helm Values:**

```yaml
global:
  spire:
    trustDomain: "example.com"
    ingressControllerType: other  # Prevents automatic ssl-passthrough annotation

spire-server:
  caTTL: "720h"  # 30 days

  federation:
    enabled: true
    tls:
      spire:
        enabled: false  # Disable SPIFFE mTLS
      certManager:
        enabled: true   # Enable cert-manager integration
        issuer:
          create: false  # Use existing ClusterIssuer
        certificate:
          issuerRef:
            kind: ClusterIssuer
            name: letsencrypt
    ingress:
      enabled: true
      className: "nginx"
      controllerType: "other"  # Prevents template from forcing ssl-passthrough
      host: spire.example.com
      # cert-manager will create this secret containing Let's Encrypt certificate
      tlsSecret: "spire-server-federation-cert"
      annotations:
        # Rate limiting
        nginx.ingress.kubernetes.io/limit-rps: "100"
        nginx.ingress.kubernetes.io/limit-burst-multiplier: "5"
        # TLS re-encryption configuration (SSL bridging)
        nginx.ingress.kubernetes.io/ssl-passthrough: "false"
        nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
        # Upstream SNI configuration for backend connection
        nginx.ingress.kubernetes.io/proxy-ssl-server-name: "on"
        nginx.ingress.kubernetes.io/proxy-ssl-name: "spire.example.com"
        nginx.ingress.kubernetes.io/proxy-ssl-verify: "off"

  controllerManager:
    watchClassless: true
    className: "dir-spire"
    identities:
      clusterFederatedTrustDomain:
        enabled: true
```

**Federation Resource:**

```yaml
# onboarding/federation/example.com.yaml
className: dir-spire
trustDomain: example.com
bundleEndpointURL: https://spire.example.com
bundleEndpointProfile:
  type: https_web
```

**Verification Procedures:**

```bash
# Test bundle endpoint accessibility (should return JSON bundle)
curl https://spire.example.com

# Verify certificate is issued by Let's Encrypt
openssl s_client -connect spire.example.com:443 -showcerts 2>&1 | \
  grep -A2 "issuer="
# Expected: issuer=C = US, O = Let's Encrypt, CN = R3

# Check certificate expiration
echo | openssl s_client -connect spire.example.com:443 2>/dev/null | \
  openssl x509 -noout -dates

# Monitor SPIRE server logs for bundle refresh
kubectl logs -n dir-spire -l app.kubernetes.io/name=server -c spire-server --follow | \
  grep "Bundle refreshed"
# Expected: level=info msg="Bundle refreshed" subsystem_name=bundle_client trust_domain=example.com

# Verify cert-manager Certificate status
kubectl get certificate -n dir-spire spire-server-federation-cert
# Expected: READY=True
```

---

### https_spiffe Configuration

**Prerequisites:**

```bash
# Enable SSL passthrough on NGINX Ingress Controller
kubectl patch deployment -n ingress-nginx ingress-nginx-controller --type='json' \
  -p='[{"op": "add", "path": "/spec/template/spec/containers/0/args/-", "value":"--enable-ssl-passthrough"}]'

# Verify SSL passthrough is enabled
kubectl get deployment -n ingress-nginx ingress-nginx-controller -o yaml | \
  grep "enable-ssl-passthrough"
# Expected: - --enable-ssl-passthrough

# Wait for deployment rollout
kubectl rollout status -n ingress-nginx deployment/ingress-nginx-controller

# Exchange bootstrap bundles with federation partners
# See "Bootstrap Bundle Exchange Process" section for detailed procedures

# Optional: Configure DNS (can use IP addresses)
# Create A record: spire.example.com → <ingress-external-ip>
```

**SPIRE Server Helm Values:**

```yaml
global:
  spire:
    trustDomain: "example.com"
    ingressControllerType: ingress-nginx  # Enables ssl-passthrough annotation

spire-server:
  caTTL: "720h"  # 30 days

  federation:
    enabled: true
    tls:
      spire:
        enabled: true  # Enable SPIFFE mTLS
      certManager:
        enabled: false
    ingress:
      enabled: true
      className: "nginx"
      host: spire.example.com
      annotations:
        # Rate limiting
        nginx.ingress.kubernetes.io/limit-rps: "100"
        nginx.ingress.kubernetes.io/limit-burst-multiplier: "5"
        # SSL passthrough for end-to-end SPIFFE mTLS
        nginx.ingress.kubernetes.io/ssl-passthrough: "true"

  controllerManager:
    watchClassless: true
    className: "dir-spire"
    identities:
      clusterFederatedTrustDomain:
        enabled: true
```

**Federation Resource:**

```yaml
# onboarding/federation/example.com.yaml
className: dir-spire
trustDomain: example.com
bundleEndpointURL: https://spire.example.com
bundleEndpointProfile:
  type: https_spiffe
  endpointSPIFFEID: spiffe://example.com/spire/server
trustDomainBundle: |-
  {
    "keys": [
      {
        "use": "x509-svid",
        "kty": "RSA",
        "n": "xGOr-H7A-qwXJhXm...",
        "e": "AQAB",
        "x5c": [
          "MIICBzCCAa2gAwIBAgIQZ..."
        ]
      },
      {
        "use": "jwt-svid",
        "kty": "RSA",
        "kid": "bJV3zF2L4",
        "n": "yH3s-K9BrT...",
        "e": "AQAB"
      }
    ],
    "spiffe_refresh_hint": 450000,
    "spiffe_sequence_number": 1
  }
```

**Verification Procedures:**

```bash
# Test bundle endpoint (requires -k for self-signed SPIFFE cert)
curl -k https://spire.example.com

# Verify SSL passthrough is working (certificate should contain URI SAN)
openssl s_client -connect spire.example.com:443 -showcerts 2>&1 | \
  openssl x509 -text -noout | \
  grep -A1 "Subject Alternative Name"
# Expected: URI:spiffe://example.com/spire/server

# Verify SPIFFE ID in certificate
echo | openssl s_client -connect spire.example.com:443 2>/dev/null | \
  openssl x509 -noout -text | \
  grep "URI:spiffe://"
# Expected: URI:spiffe://example.com/spire/server

# Monitor SPIRE server logs for bundle refresh
kubectl logs -n dir-spire -l app.kubernetes.io/name=server -c spire-server --follow | \
  grep "Bundle refreshed"
# Expected: level=info msg="Bundle refreshed" subsystem_name=bundle_client trust_domain=example.com

# Verify SPIRE server issued itself a federation SVID
kubectl logs -n dir-spire -l app.kubernetes.io/name=server -c spire-server | \
  grep "federation SVID"
```
