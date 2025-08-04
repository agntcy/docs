# Core API Reference

<a name="core_v1_record-proto"></a>


## core/v1/record.proto



<a name="core-v1-Record"></a>

### Record
Record unifies different versions of records into a single message.
It allows for backward compatibility and easier handling of different
record versions in the same service or application.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| v1 | [objects.v1.Agent](#objects-v1-Agent) |  |  |
| v2 | [objects.v2.AgentRecord](#objects-v2-AgentRecord) |  |  |
| v3 | [objects.v3.Record](#objects-v3-Record) |  |  |






<a name="core-v1-RecordMeta"></a>

### RecordMeta
Defines metadata about a record.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| cid | [string](#string) |  | CID of the record. |
| annotations | [RecordMeta.AnnotationsEntry](#core-v1-RecordMeta-AnnotationsEntry) | repeated | Annotations attached to the record. |
| schema_version | [string](#string) |  | Schema version of the record. |
| created_at | [string](#string) |  | Creation timestamp of the record in the RFC3339 format. Specs: https://www.rfc-editor.org/rfc/rfc3339.html |






<a name="core-v1-RecordMeta-AnnotationsEntry"></a>

### RecordMeta.AnnotationsEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [string](#string) |  |  |






<a name="core-v1-RecordRef"></a>

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

