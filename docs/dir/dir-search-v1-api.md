# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [agntcy/dir/search/v1/record_query.proto](#agntcy_dir_search_v1_record_query-proto)
  - [RecordQuery](#agntcy-dir-search-v1-RecordQuery)
  
  - [RecordQueryType](#agntcy-dir-search-v1-RecordQueryType)
  
- [agntcy/dir/search/v1/search_service.proto](#agntcy_dir_search_v1_search_service-proto)
  - [SearchRequest](#agntcy-dir-search-v1-SearchRequest)
  - [SearchResponse](#agntcy-dir-search-v1-SearchResponse)
  
  - [SearchService](#agntcy-dir-search-v1-SearchService)
  
- [Scalar Value Types](#scalar-value-types)

<a name="agntcy_dir_search_v1_record_query-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## agntcy/dir/search/v1/record_query.proto

<a name="agntcy-dir-search-v1-RecordQuery"></a>

### RecordQuery
A query to match the record against during discovery.
For example:
  Exact match:      { type: RECORD_QUERY_TYPE_NAME, value: &#34;my-agent&#34; }
  Wildcard match:   { type: RECORD_QUERY_TYPE_NAME, value: &#34;web*&#34; }
  Pattern match:    { type: RECORD_QUERY_TYPE_SKILL_NAME, value: &#34;*machine*learning*&#34; }
  Question mark:    { type: RECORD_QUERY_TYPE_VERSION, value: &#34;v1.0.?&#34; }
  Complex match:    { type: RECORD_QUERY_TYPE_LOCATOR, value: &#34;docker-image:https://*.example.com/*&#34; }

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| type | [RecordQueryType](#agntcy-dir-search-v1-RecordQueryType) |  | The type of the query to match against. |
| value | [string](#string) |  | The query value to match against. Supports wildcard patterns: &#39;*&#39; - matches zero or more characters &#39;?&#39; - matches exactly one character &#39;[]&#39; - matches any character within brackets (e.g., [0-9], [a-z], [abc]) |

<a name="agntcy-dir-search-v1-RecordQueryType"></a>

### RecordQueryType
Defines a list of supported record query types.

| Name | Number | Description |
| ---- | ------ | ----------- |
| RECORD_QUERY_TYPE_UNSPECIFIED | 0 | Unspecified query type. |
| RECORD_QUERY_TYPE_NAME | 1 | Query for a record name. Supports wildcard patterns: &#34;web*&#34;, &#34;*service&#34;, &#34;api-*-v2&#34;, &#34;???api&#34;, &#34;agent-[0-9]&#34; |
| RECORD_QUERY_TYPE_VERSION | 2 | Query for a record version. Supports wildcard patterns: &#34;v1.*&#34;, &#34;v2.*&#34;, &#34;*-beta&#34;, &#34;v1.0.?&#34;, &#34;v[0-9].*&#34; |
| RECORD_QUERY_TYPE_SKILL_ID | 3 | Query for a skill ID. Numeric field - exact match only, no wildcard support. |
| RECORD_QUERY_TYPE_SKILL_NAME | 4 | Query for a skill name. Supports wildcard patterns: &#34;python*&#34;, &#34;*script&#34;, &#34;*machine*learning*&#34;, &#34;Python?&#34;, &#34;[A-M]*&#34; |
| RECORD_QUERY_TYPE_LOCATOR | 5 | Query for a locator type. Supports wildcard patterns: &#34;http*&#34;, &#34;ftp*&#34;, &#34;*docker*&#34;, &#34;[hf]tt[ps]*&#34; |
| RECORD_QUERY_TYPE_MODULE | 6 | Query for a module. Supports wildcard patterns: &#34;*-plugin&#34;, &#34;*-module&#34;, &#34;core*&#34;, &#34;mod-?&#34;, &#34;plugin-[0-9]&#34; |

<a name="agntcy_dir_search_v1_search_service-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## agntcy/dir/search/v1/search_service.proto

<a name="agntcy-dir-search-v1-SearchRequest"></a>

### SearchRequest

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| queries | [RecordQuery](#agntcy-dir-search-v1-RecordQuery) | repeated | List of queries to match against the records. |
| limit | [uint32](#uint32) | optional | Optional limit on the number of results to return. |
| offset | [uint32](#uint32) | optional | Optional offset for pagination of results. |

<a name="agntcy-dir-search-v1-SearchResponse"></a>

### SearchResponse

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record_cid | [string](#string) |  | The CID of the record that matches the search criteria. |

<a name="agntcy-dir-search-v1-SearchService"></a>

### SearchService

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| Search | [SearchRequest](#agntcy-dir-search-v1-SearchRequest) | [SearchResponse](#agntcy-dir-search-v1-SearchResponse) stream | List records that this peer is currently providing that match the given parameters. This operation does not interact with the network. |

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
