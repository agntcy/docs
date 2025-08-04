# Sign API Reference

<a name="sign_v1_sign_service-proto"></a>


## sign/v1/sign_service.proto



<a name="sign-v1-SignRequest"></a>

### SignRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record | [core.v1.Record](#core-v1-Record) |  | Record to be signed |
| provider | [SignRequestProvider](#sign-v1-SignRequestProvider) |  | Signing provider to use |






<a name="sign-v1-SignRequestProvider"></a>

### SignRequestProvider



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| oidc | [SignWithOIDC](#sign-v1-SignWithOIDC) |  | Sign with OIDC provider |
| key | [SignWithKey](#sign-v1-SignWithKey) |  | Sign with PEM-encoded public key |






<a name="sign-v1-SignResponse"></a>

### SignResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| signature | [Signature](#sign-v1-Signature) |  | Cryptographic signature of the record |






<a name="sign-v1-SignWithKey"></a>

### SignWithKey



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| private_key | [bytes](#bytes) |  | Private key used for signing |
| password | [bytes](#bytes) | optional | Password to unlock the private key |






<a name="sign-v1-SignWithOIDC"></a>

### SignWithOIDC



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id_token | [string](#string) |  | Token for OIDC provider |
| options | [SignWithOIDC.SignOpts](#sign-v1-SignWithOIDC-SignOpts) |  | Signing options for OIDC |






<a name="sign-v1-SignWithOIDC-SignOpts"></a>

### SignWithOIDC.SignOpts
List of sign options for OIDC


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| fulcio_url | [string](#string) | optional | Fulcio authority access URL (default value: https://fulcio.sigstage.dev) |
| rekor_url | [string](#string) | optional | Rekor validator access URL (default value: https://rekor.sigstage.dev) |
| timestamp_url | [string](#string) | optional | Timestamp authority access URL (default value: https://timestamp.sigstage.dev/api/v1/timestamp) |
| oidc_provider_url | [string](#string) | optional | OIDC provider access URL (default value: https://oauth2.sigstage.dev/auth) |






<a name="sign-v1-Signature"></a>

### Signature



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| annotations | [Signature.AnnotationsEntry](#sign-v1-Signature-AnnotationsEntry) | repeated | Metadata associated with the signature. |
| signed_at | [string](#string) |  | Signing timestamp of the record in the RFC3339 format. Specs: https://www.rfc-editor.org/rfc/rfc3339.html |
| algorithm | [string](#string) |  | The signature algorithm used (e.g., &#34;ECDSA_P256_SHA256&#34;). |
| signature | [string](#string) |  | Base64-encoded signature. |
| certificate | [string](#string) |  | Base64-encoded signing certificate. |
| content_type | [string](#string) |  | Type of the signature content bundle. |
| content_bundle | [string](#string) |  | Base64-encoded signature bundle produced by the signer. It is up to the client to interpret the content of the bundle. |






<a name="sign-v1-Signature-AnnotationsEntry"></a>

### Signature.AnnotationsEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [string](#string) |  |  |






<a name="sign-v1-VerifyRequest"></a>

### VerifyRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record | [core.v1.Record](#core-v1-Record) |  | Record to be verified |
| signature | [Signature](#sign-v1-Signature) |  | Signature to verify against the record |
| provider | [VerifyRequestProvider](#sign-v1-VerifyRequestProvider) |  | Verification provider to use |






<a name="sign-v1-VerifyRequestProvider"></a>

### VerifyRequestProvider



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| oidc | [VerifyWithOIDC](#sign-v1-VerifyWithOIDC) |  | Verify with OIDC provider |
| key | [VerifyWithKey](#sign-v1-VerifyWithKey) |  | Verify with PEM-encoded public key |






<a name="sign-v1-VerifyResponse"></a>

### VerifyResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| success | [bool](#bool) |  | The verify process result |
| error_message | [string](#string) | optional | Optional error message if verification failed |






<a name="sign-v1-VerifyWithKey"></a>

### VerifyWithKey



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| public_key | [bytes](#bytes) |  | Public key to validate the signed record |






<a name="sign-v1-VerifyWithOIDC"></a>

### VerifyWithOIDC



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| expected_issuer | [string](#string) |  | Expected issuer in the signed record |
| expected_signer | [string](#string) |  | Expected signer in the signed record |





 

 

 


<a name="sign-v1-SignService"></a>

### SignService


| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| Sign | [SignRequest](#sign-v1-SignRequest) | [SignResponse](#sign-v1-SignResponse) | Sign record using keyless OIDC based provider or using PEM-encoded private key with an optional passphrase |
| Verify | [VerifyRequest](#sign-v1-VerifyRequest) | [VerifyResponse](#sign-v1-VerifyResponse) | Verify signed record using keyless OIDC based provider or using PEM-encoded formatted PEM public key encrypted |

 



## Scalar Value Types

| .proto Type | Notes | C++ | Java | Python | Go | C# | PHP | Ruby |
| ----------- | ----- | --- | ---- | ------ | -- | -- | --- | ---- |
| <a name="double" /> double |  | double | double | float | float64 | double | float | Float |
| <a name="float" /> float |  | float | float | float | float32 | float | float | Float |
| <a name="int32" /> int32 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint32 instead. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="int64" /> int64 | Uses variable-length encoding. Inefficient for encoding negative numbers – if your field is likely to have negative values, use sint64 instead. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="uint32" /> uint32 | Uses variable-length encoding. | uint32 | int | int/long | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="uint64" /> uint64 | Uses variable-length encoding. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum or Fixnum (as required) |
| <a name="sint32" /> sint32 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int32s. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sint64" /> sint64 | Uses variable-length encoding. Signed int value. These more efficiently encode negative numbers than regular int64s. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="fixed32" /> fixed32 | Always four bytes. More efficient than uint32 if values are often greater than 2^28. | uint32 | int | int | uint32 | uint | integer | Bignum or Fixnum (as required) |
| <a name="fixed64" /> fixed64 | Always eight bytes. More efficient than uint64 if values are often greater than 2^56. | uint64 | long | int/long | uint64 | ulong | integer/string | Bignum |
| <a name="sfixed32" /> sfixed32 | Always four bytes. | int32 | int | int | int32 | int | integer | Bignum or Fixnum (as required) |
| <a name="sfixed64" /> sfixed64 | Always eight bytes. | int64 | long | int/long | int64 | long | integer/string | Bignum |
| <a name="bool" /> bool |  | bool | boolean | boolean | bool | bool | boolean | TrueClass/FalseClass |
| <a name="string" /> string | A string must always contain UTF-8 encoded or 7-bit ASCII text. | string | String | str/unicode | string | string | string | String (UTF-8) |
| <a name="bytes" /> bytes | May contain any arbitrary sequence of bytes. | string | ByteString | str | []byte | ByteString | string | String (ASCII-8BIT) |

