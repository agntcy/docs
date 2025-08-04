# Search API Reference


<a name="search_v1_record_query-proto"></a>


## search/v1/record_query.proto



<a name="search-v1-RecordQuery"></a>

### RecordQuery
A query to match the record against during discovery.
For example:
 { type: RECORD_QUERY_TYPE_SKILL_NAME, value: &#34;Natural Language Processing&#34; }
 { type: RECORD_QUERY_TYPE_LOCATOR, value: &#34;docker-image:https://example.com/docker-image&#34; }


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| type | [RecordQueryType](#search-v1-RecordQueryType) |  | The type of the query to match against. |
| value | [string](#string) |  | The query value to match against. |





 


<a name="search-v1-RecordQueryType"></a>

### RecordQueryType
Defines a list of supported record query types.

| Name | Number | Description |
| ---- | ------ | ----------- |
| RECORD_QUERY_TYPE_UNSPECIFIED | 0 | Unspecified query type. |
| RECORD_QUERY_TYPE_NAME | 1 | Query for an agent name. |
| RECORD_QUERY_TYPE_VERSION | 2 | Query for an agent version. |
| RECORD_QUERY_TYPE_SKILL_ID | 3 | Query for a skill ID. |
| RECORD_QUERY_TYPE_SKILL_NAME | 4 | Query for a skill name. |
| RECORD_QUERY_TYPE_LOCATOR | 5 | Query for a locator. |
| RECORD_QUERY_TYPE_EXTENSION | 6 | Query for an extension. |


 

 

 



<a name="search_v1_search_service-proto"></a>


## search/v1/search_service.proto



<a name="search-v1-SearchRequest"></a>

### SearchRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| queries | [RecordQuery](#search-v1-RecordQuery) | repeated | List of queries to match against the records. |
| limit | [uint32](#uint32) | optional | Optional limit on the number of results to return. |
| offset | [uint32](#uint32) | optional | Optional offset for pagination of results. |






<a name="search-v1-SearchResponse"></a>

### SearchResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record_cid | [string](#string) |  | The CID of the record that matches the search criteria. |





 

 

 


<a name="search-v1-SearchService"></a>

### SearchService


| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| Search | [SearchRequest](#search-v1-SearchRequest) | [SearchResponse](#search-v1-SearchResponse) stream | List records that this peer is currently providing that match the given parameters. This operation does not interact with the network. |

 



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

