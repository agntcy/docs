# Routing API Reference


<a name="routing_v1_routing_service-proto"></a>


## routing/v1/routing_service.proto



<a name="routing-v1-LegacyListRequest"></a>

### LegacyListRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| peer | [Peer](#routing-v1-Peer) | optional | Target peer. If selected, it returns the skill details for this peer. It may use labels to only return selected labels. |
| labels | [string](#string) | repeated | Target labels. For example, labels={&#34;skill=text&#34;, &#34;skill=text/rag&#34;} |
| ref | [core.v1.RecordRef](#core-v1-RecordRef) | optional | Target record, if any. If set, it will return only the record with the given reference. |
| max_hops | [uint32](#uint32) | optional | Max routing depth. |






<a name="routing-v1-LegacyListResponse"></a>

### LegacyListResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| items | [LegacyListResponse.Item](#routing-v1-LegacyListResponse-Item) | repeated | Returned items that match a given request |






<a name="routing-v1-LegacyListResponse-Item"></a>

### LegacyListResponse.Item



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| labels | [string](#string) | repeated | Labels associated with a given record |
| label_counts | [LegacyListResponse.Item.LabelCountsEntry](#routing-v1-LegacyListResponse-Item-LabelCountsEntry) | repeated | Optionally sends count details about individual skill. This is only set when querying labels or our own current peer. For record requests, only returns the data about that record. |
| peer | [Peer](#routing-v1-Peer) |  | Peer that returned this record. |
| ref | [core.v1.RecordRef](#core-v1-RecordRef) | optional | Found record if any. If empty, then only the labels are important. |






<a name="routing-v1-LegacyListResponse-Item-LabelCountsEntry"></a>

### LegacyListResponse.Item.LabelCountsEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [uint64](#uint64) |  |  |






<a name="routing-v1-ListRequest"></a>

### ListRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| queries | [RecordQuery](#routing-v1-RecordQuery) | repeated | List of queries to match against the records. If set, all queries must match for the record to be returned. |
| limit | [uint32](#uint32) | optional | Limit the number of results returned. If not set, it will return all records that this peer is providing. |
| legacy_list_request | [LegacyListRequest](#routing-v1-LegacyListRequest) | optional | Legacy list request. TODO Remove when new announce and discovery design is implemented |






<a name="routing-v1-ListResponse"></a>

### ListResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record_cid | [string](#string) |  | The record that matches the list queries. |
| legacy_list_response | [LegacyListResponse](#routing-v1-LegacyListResponse) | optional | Legacy list response. TODO Remove when new announce and discovery design is implemented |






<a name="routing-v1-PublishRequest"></a>

### PublishRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record_cid | [string](#string) |  | Reference to the agent record to be published. |






<a name="routing-v1-SearchRequest"></a>

### SearchRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| queries | [RecordQuery](#routing-v1-RecordQuery) | repeated | List of queries to match against the records. |
| min_match_score | [uint32](#uint32) | optional | Minimal target query match score. For example, if min_match_score=2, it will return records that match at least two of the queries. If not set, it will return records that match at least one query. |
| limit | [uint32](#uint32) | optional | Limit the number of results returned. If not set, it will return all discovered records. Note that this is a soft limit, as the search may return more results than the limit if there are multiple peers providing the same record. |






<a name="routing-v1-SearchResponse"></a>

### SearchResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record_cid | [string](#string) |  | The record that matches the search query. |
| peer | [Peer](#routing-v1-Peer) |  | The peer that provided the record. |
| match_queries | [RecordQuery](#routing-v1-RecordQuery) | repeated | The queries that were matched. |
| match_score | [uint32](#uint32) |  | The score of the search match. |






<a name="routing-v1-UnpublishRequest"></a>

### UnpublishRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record_cid | [string](#string) |  | Reference to the agent record to be unpublished. |





 

 

 


<a name="routing-v1-RoutingService"></a>

### RoutingService
Defines an interface for announcement and discovery
of records across interconnected network.

Middleware should be used to control who can perform these RPCs.
Policies for the middleware can be handled via separate service.

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| Publish | [PublishRequest](#routing-v1-PublishRequest) | [.google.protobuf.Empty](#google-protobuf-Empty) | Announce to the network that this peer is providing a given record. This enables other peers to discover this record and retrieve it from this peer. Listeners can use this event to perform custom operations, for example by cloning the record.

Items need to be periodically republished (eg. 24h) to the network to avoid stale data. Republication should be done in the background. |
| Unpublish | [UnpublishRequest](#routing-v1-UnpublishRequest) | [.google.protobuf.Empty](#google-protobuf-Empty) | Stop serving this record to the network. If other peers try to retrieve this record, the peer will refuse the request. |
| Search | [SearchRequest](#routing-v1-SearchRequest) | [SearchResponse](#routing-v1-SearchResponse) stream | Search records based on the request across the network. This will search the network for the record with the given parameters.

It is possible that the records are stale or that they do not exist. Some records may be provided by multiple peers.

Results from the search can be used as an input to Pull operation to retrieve the records. |
| List | [ListRequest](#routing-v1-ListRequest) | [ListResponse](#routing-v1-ListResponse) stream | List all records that this peer is currently providing that match the given parameters. This operation does not interact with the network. |

 



<a name="routing_v1_peer-proto"></a>


## routing/v1/peer.proto



<a name="routing-v1-Peer"></a>

### Peer



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  | ID of a given peer, typically described by a protocol. For example: - SPIFFE: &#34;spiffe://example.org/service/foo&#34; - JWT: &#34;jwt:sub=alice,iss=https://issuer.example.com&#34; - Tor: &#34;onion:abcdefghijklmno.onion&#34; - DID: &#34;did:example:123456789abcdefghi&#34; - IPFS: &#34;ipfs:QmYwAPJzv5CZsnAzt8auVZRn2E6sD1c4x8pN5o6d5cW4D5&#34; |
| addrs | [string](#string) | repeated | Multiaddrs for a given peer. For example: - &#34;/ip4/127.0.0.1/tcp/4001&#34; - &#34;/ip6/::1/tcp/4001&#34; - &#34;/dns4/example.com/tcp/443/https&#34; |
| annotations | [Peer.AnnotationsEntry](#routing-v1-Peer-AnnotationsEntry) | repeated | Additional metadata about the peer. |
| connection | [PeerConnectionType](#routing-v1-PeerConnectionType) |  | Used to signal the sender&#39;s connection capabilities to the peer. |






<a name="routing-v1-Peer-AnnotationsEntry"></a>

### Peer.AnnotationsEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [string](#string) |  |  |





 


<a name="routing-v1-PeerConnectionType"></a>

### PeerConnectionType


| Name | Number | Description |
| ---- | ------ | ----------- |
| PEER_CONNECTION_TYPE_NOT_CONNECTED | 0 | Sender does not have a connection to peer, and no extra information (default) |
| PEER_CONNECTION_TYPE_CONNECTED | 1 | Sender has a live connection to peer. |
| PEER_CONNECTION_TYPE_CAN_CONNECT | 2 | Sender recently connected to peer. |
| PEER_CONNECTION_TYPE_CANNOT_CONNECT | 3 | Sender made strong effort to connect to peer repeatedly but failed. |


 

 

 



<a name="routing_v1_record_query-proto"></a>


## routing/v1/record_query.proto



<a name="routing-v1-RecordQuery"></a>

### RecordQuery
A query to match the record against during discovery.
For example:
 { type: RECORD_QUERY_TYPE_SKILL, value: &#34;Natural Language Processing&#34; }
 { type: RECORD_QUERY_TYPE_LOCATOR, value: &#34;helm-chart&#34; }


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| type | [RecordQueryType](#routing-v1-RecordQueryType) |  | The type of the query to match against. |
| value | [string](#string) |  | The query value to match against. |





 


<a name="routing-v1-RecordQueryType"></a>

### RecordQueryType
Defines a list of supported record query types.

| Name | Number | Description |
| ---- | ------ | ----------- |
| RECORD_QUERY_TYPE_UNSPECIFIED | 0 | Unspecified query type. |
| RECORD_QUERY_TYPE_SKILL | 1 | Query for a skill name. |
| RECORD_QUERY_TYPE_LOCATOR | 2 | Query for a locator type. |


 

 

 



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

