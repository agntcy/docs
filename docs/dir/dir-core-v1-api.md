# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [agntcy/dir/core/v1/record.proto](#agntcy_dir_core_v1_record-proto)
  - [Record](#agntcy-dir-core-v1-Record)
  - [RecordMeta](#agntcy-dir-core-v1-RecordMeta)
  - [RecordMeta.AnnotationsEntry](#agntcy-dir-core-v1-RecordMeta-AnnotationsEntry)
  - [RecordRef](#agntcy-dir-core-v1-RecordRef)
  
- [Scalar Value Types](#scalar-value-types)

<a name="agntcy_dir_core_v1_record-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## agntcy/dir/core/v1/record.proto

<a name="agntcy-dir-core-v1-Record"></a>

### Record
Record is a generic object that encapsulates data of different Record types.

Supported schemas:

v0.3.1: https://schema.oasf.outshift.com/0.3.1/objects/agent
v0.7.0: https://schema.oasf.outshift.com/0.7.0/objects/record

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| data | [google.protobuf.Struct](#google-protobuf-Struct) |  |  |

<a name="agntcy-dir-core-v1-RecordMeta"></a>

### RecordMeta
Defines metadata about a record.

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| cid | [string](#string) |  | CID of the record. |
| annotations | [RecordMeta.AnnotationsEntry](#agntcy-dir-core-v1-RecordMeta-AnnotationsEntry) | repeated | Annotations attached to the record. |
| schema_version | [string](#string) |  | Schema version of the record. |
| created_at | [string](#string) |  | Creation timestamp of the record in the RFC3339 format. Specs: https://www.rfc-editor.org/rfc/rfc3339.html |

<a name="agntcy-dir-core-v1-RecordMeta-AnnotationsEntry"></a>

### RecordMeta.AnnotationsEntry

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [string](#string) |  |  |

<a name="agntcy-dir-core-v1-RecordRef"></a>

### RecordRef
Defines a reference or a globally unique content identifier of a record.

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| cid | [string](#string) |  | Globally-unique content identifier (CID) of the record. Specs: https://github.com/multiformats/cid |

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
