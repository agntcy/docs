# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [agntcy/dir/sign/v1/sign_service.proto](#agntcy_dir_sign_v1_sign_service-proto)
  - [SignRequest](#agntcy-dir-sign-v1-SignRequest)
  - [SignRequestProvider](#agntcy-dir-sign-v1-SignRequestProvider)
  - [SignResponse](#agntcy-dir-sign-v1-SignResponse)
  - [SignWithKey](#agntcy-dir-sign-v1-SignWithKey)
  - [SignWithOIDC](#agntcy-dir-sign-v1-SignWithOIDC)
  - [SignWithOIDC.SignOpts](#agntcy-dir-sign-v1-SignWithOIDC-SignOpts)
  - [Signature](#agntcy-dir-sign-v1-Signature)
  - [Signature.AnnotationsEntry](#agntcy-dir-sign-v1-Signature-AnnotationsEntry)
  - [VerifyRequest](#agntcy-dir-sign-v1-VerifyRequest)
  - [VerifyResponse](#agntcy-dir-sign-v1-VerifyResponse)
  
  - [SignService](#agntcy-dir-sign-v1-SignService)
  
- [Scalar Value Types](#scalar-value-types)

<a name="agntcy_dir_sign_v1_sign_service-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## agntcy/dir/sign/v1/sign_service.proto

<a name="agntcy-dir-sign-v1-SignRequest"></a>

### SignRequest

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record_ref | [agntcy.dir.core.v1.RecordRef](dir-core-v1-api.md#agntcy-dir-core-v1-RecordRef) |  | Record reference to be signed |
| provider | [SignRequestProvider](#agntcy-dir-sign-v1-SignRequestProvider) |  | Signing provider to use |

<a name="agntcy-dir-sign-v1-SignRequestProvider"></a>

### SignRequestProvider

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| oidc | [SignWithOIDC](#agntcy-dir-sign-v1-SignWithOIDC) |  | Sign with OIDC provider |
| key | [SignWithKey](#agntcy-dir-sign-v1-SignWithKey) |  | Sign with PEM-encoded public key |

<a name="agntcy-dir-sign-v1-SignResponse"></a>

### SignResponse

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| signature | [Signature](#agntcy-dir-sign-v1-Signature) |  | Cryptographic signature of the record |

<a name="agntcy-dir-sign-v1-SignWithKey"></a>

### SignWithKey

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| private_key | [bytes](#bytes) |  | Private key used for signing |
| password | [bytes](#bytes) | optional | Password to unlock the private key |

<a name="agntcy-dir-sign-v1-SignWithOIDC"></a>

### SignWithOIDC

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id_token | [string](#string) |  | Token for OIDC provider |
| options | [SignWithOIDC.SignOpts](#agntcy-dir-sign-v1-SignWithOIDC-SignOpts) |  | Signing options for OIDC |

<a name="agntcy-dir-sign-v1-SignWithOIDC-SignOpts"></a>

### SignWithOIDC.SignOpts
List of sign options for OIDC

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| fulcio_url | [string](#string) | optional | Fulcio authority access URL (default value: https://fulcio.sigstage.dev) |
| rekor_url | [string](#string) | optional | Rekor validator access URL (default value: https://rekor.sigstage.dev) |
| timestamp_url | [string](#string) | optional | Timestamp authority access URL (default value: https://timestamp.sigstage.dev/api/v1/timestamp) |
| oidc_provider_url | [string](#string) | optional | OIDC provider access URL (default value: https://oauth2.sigstage.dev/auth) |

<a name="agntcy-dir-sign-v1-Signature"></a>

### Signature

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| annotations | [Signature.AnnotationsEntry](#agntcy-dir-sign-v1-Signature-AnnotationsEntry) | repeated | Metadata associated with the signature. |
| signed_at | [string](#string) |  | Signing timestamp of the record in the RFC3339 format. Specs: https://www.rfc-editor.org/rfc/rfc3339.html |
| algorithm | [string](#string) |  | The signature algorithm used (e.g., &#34;ECDSA_P256_SHA256&#34;). |
| signature | [string](#string) |  | Base64-encoded signature. |
| certificate | [string](#string) |  | Base64-encoded signing certificate. |
| content_type | [string](#string) |  | Type of the signature content bundle. |
| content_bundle | [string](#string) |  | Base64-encoded signature bundle produced by the signer. It is up to the client to interpret the content of the bundle. |

<a name="agntcy-dir-sign-v1-Signature-AnnotationsEntry"></a>

### Signature.AnnotationsEntry

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [string](#string) |  |  |

<a name="agntcy-dir-sign-v1-VerifyRequest"></a>

### VerifyRequest

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record_ref | [agntcy.dir.core.v1.RecordRef](dir-core-v1-api.md#agntcy-dir-core-v1-RecordRef) |  | Record reference to be verified |

<a name="agntcy-dir-sign-v1-VerifyResponse"></a>

### VerifyResponse

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| success | [bool](#bool) |  | The verify process result |
| error_message | [string](#string) | optional | Optional error message if verification failed |

<a name="agntcy-dir-sign-v1-SignService"></a>

### SignService

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| Sign | [SignRequest](#agntcy-dir-sign-v1-SignRequest) | [SignResponse](#agntcy-dir-sign-v1-SignResponse) | Sign record using keyless OIDC based provider or using PEM-encoded private key with an optional passphrase |
| Verify | [VerifyRequest](#agntcy-dir-sign-v1-VerifyRequest) | [VerifyResponse](#agntcy-dir-sign-v1-VerifyResponse) | Verify signed record using keyless OIDC based provider or using PEM-encoded formatted PEM public key encrypted |

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
