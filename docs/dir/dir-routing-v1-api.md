# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [agntcy/dir/routing/v1/peer.proto](#agntcy_dir_routing_v1_peer-proto)
    - [Peer](#agntcy-dir-routing-v1-Peer)
    - [Peer.AnnotationsEntry](#agntcy-dir-routing-v1-Peer-AnnotationsEntry)
  
    - [PeerConnectionType](#agntcy-dir-routing-v1-PeerConnectionType)
  
- [agntcy/dir/routing/v1/publication_service.proto](#agntcy_dir_routing_v1_publication_service-proto)
    - [CreatePublicationResponse](#agntcy-dir-routing-v1-CreatePublicationResponse)
    - [GetPublicationRequest](#agntcy-dir-routing-v1-GetPublicationRequest)
    - [GetPublicationResponse](#agntcy-dir-routing-v1-GetPublicationResponse)
    - [ListPublicationsItem](#agntcy-dir-routing-v1-ListPublicationsItem)
    - [ListPublicationsRequest](#agntcy-dir-routing-v1-ListPublicationsRequest)
  
    - [PublicationStatus](#agntcy-dir-routing-v1-PublicationStatus)
  
    - [PublicationService](#agntcy-dir-routing-v1-PublicationService)
  
- [agntcy/dir/routing/v1/record_query.proto](#agntcy_dir_routing_v1_record_query-proto)
    - [RecordQuery](#agntcy-dir-routing-v1-RecordQuery)
  
    - [RecordQueryType](#agntcy-dir-routing-v1-RecordQueryType)
  
- [agntcy/dir/routing/v1/routing_service.proto](#agntcy_dir_routing_v1_routing_service-proto)
    - [ListRequest](#agntcy-dir-routing-v1-ListRequest)
    - [ListResponse](#agntcy-dir-routing-v1-ListResponse)
    - [PublishRequest](#agntcy-dir-routing-v1-PublishRequest)
    - [RecordQueries](#agntcy-dir-routing-v1-RecordQueries)
    - [RecordRefs](#agntcy-dir-routing-v1-RecordRefs)
    - [SearchRequest](#agntcy-dir-routing-v1-SearchRequest)
    - [SearchResponse](#agntcy-dir-routing-v1-SearchResponse)
    - [UnpublishRequest](#agntcy-dir-routing-v1-UnpublishRequest)
  
    - [RoutingService](#agntcy-dir-routing-v1-RoutingService)
  
- [Scalar Value Types](#scalar-value-types)



<a name="agntcy_dir_routing_v1_peer-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## agntcy/dir/routing/v1/peer.proto



<a name="agntcy-dir-routing-v1-Peer"></a>

### Peer



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| id | [string](#string) |  | ID of a given peer, typically described by a protocol. For example: - SPIFFE: &#34;spiffe://example.org/service/foo&#34; - JWT: &#34;jwt:sub=alice,iss=https://issuer.example.com&#34; - Tor: &#34;onion:abcdefghijklmno.onion&#34; - DID: &#34;did:example:123456789abcdefghi&#34; - IPFS: &#34;ipfs:QmYwAPJzv5CZsnAzt8auVZRn2E6sD1c4x8pN5o6d5cW4D5&#34; |
| addrs | [string](#string) | repeated | Multiaddrs for a given peer. For example: - &#34;/ip4/127.0.0.1/tcp/4001&#34; - &#34;/ip6/::1/tcp/4001&#34; - &#34;/dns4/example.com/tcp/443/https&#34; |
| annotations | [Peer.AnnotationsEntry](#agntcy-dir-routing-v1-Peer-AnnotationsEntry) | repeated | Additional metadata about the peer. |
| connection | [PeerConnectionType](#agntcy-dir-routing-v1-PeerConnectionType) |  | Used to signal the sender&#39;s connection capabilities to the peer. |






<a name="agntcy-dir-routing-v1-Peer-AnnotationsEntry"></a>

### Peer.AnnotationsEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [string](#string) |  |  |





 


<a name="agntcy-dir-routing-v1-PeerConnectionType"></a>

### PeerConnectionType


| Name | Number | Description |
| ---- | ------ | ----------- |
| PEER_CONNECTION_TYPE_NOT_CONNECTED | 0 | Sender does not have a connection to peer, and no extra information (default) |
| PEER_CONNECTION_TYPE_CONNECTED | 1 | Sender has a live connection to peer. |
| PEER_CONNECTION_TYPE_CAN_CONNECT | 2 | Sender recently connected to peer. |
| PEER_CONNECTION_TYPE_CANNOT_CONNECT | 3 | Sender made strong effort to connect to peer repeatedly but failed. |


 

 

 



<a name="agntcy_dir_routing_v1_publication_service-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## agntcy/dir/routing/v1/publication_service.proto



<a name="agntcy-dir-routing-v1-CreatePublicationResponse"></a>

### CreatePublicationResponse
CreatePublicationResponse returns the result of creating a publication request.
This includes the publication ID and any relevant metadata.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| publication_id | [string](#string) |  | Unique identifier of the publication operation. |






<a name="agntcy-dir-routing-v1-GetPublicationRequest"></a>

### GetPublicationRequest
GetPublicationRequest specifies which publication to retrieve by its identifier.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| publication_id | [string](#string) |  | Unique identifier of the publication operation to query. |






<a name="agntcy-dir-routing-v1-GetPublicationResponse"></a>

### GetPublicationResponse
GetPublicationResponse contains the full details of a specific publication request.
Includes status, progress information, and any error details if applicable.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| publication_id | [string](#string) |  | Unique identifier of the publication operation. |
| status | [PublicationStatus](#agntcy-dir-routing-v1-PublicationStatus) |  | Current status of the publication operation. |
| created_time | [string](#string) |  | Timestamp when the publication operation was created in the RFC3339 format. Specs: https://www.rfc-editor.org/rfc/rfc3339.html |
| last_update_time | [string](#string) |  | Timestamp of the most recent status update for this publication in the RFC3339 format. |






<a name="agntcy-dir-routing-v1-ListPublicationsItem"></a>

### ListPublicationsItem
ListPublicationsItem represents a single publication request in the list response.
Contains publication details including ID, status, and creation timestamp.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| publication_id | [string](#string) |  | Unique identifier of the publication operation. |
| status | [PublicationStatus](#agntcy-dir-routing-v1-PublicationStatus) |  | Current status of the publication operation. |
| created_time | [string](#string) |  | Timestamp when the publication operation was created in the RFC3339 format. Specs: https://www.rfc-editor.org/rfc/rfc3339.html |
| last_update_time | [string](#string) |  | Timestamp of the most recent status update for this publication in the RFC3339 format. |






<a name="agntcy-dir-routing-v1-ListPublicationsRequest"></a>

### ListPublicationsRequest
ListPublicationsRequest contains optional filters for listing publication requests.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| limit | [uint32](#uint32) | optional | Optional limit on the number of results to return. |
| offset | [uint32](#uint32) | optional | Optional offset for pagination of results. |





 


<a name="agntcy-dir-routing-v1-PublicationStatus"></a>

### PublicationStatus
PublicationStatus represents the current state of a publication request.
Publications progress from pending to processing to completed or failed states.

| Name | Number | Description |
| ---- | ------ | ----------- |
| PUBLICATION_STATUS_UNSPECIFIED | 0 | Default/unset status - should not be used in practice |
| PUBLICATION_STATUS_PENDING | 1 | Sync operation has been created but not yet started |
| PUBLICATION_STATUS_IN_PROGRESS | 2 | Sync operation is actively discovering and transferring objects |
| PUBLICATION_STATUS_COMPLETED | 3 | Sync operation has been successfully completed |
| PUBLICATION_STATUS_FAILED | 4 | Sync operation encountered an error and stopped |


 

 


<a name="agntcy-dir-routing-v1-PublicationService"></a>

### PublicationService
PublicationService manages publication requests for announcing records to the DHT.

Publications are stored in the database and processed by a worker that runs every hour.
The publication workflow:
1. Publications are created via routing&#39;s Publish RPC by specifying either a query, a list of CIDs, or all records
2. Publication requests are added to the database
3. PublicationWorker queries the data using the publication request from the database to get the list of CIDs to be published
4. PublicationWorker announces the records with these CIDs to the DHT

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| CreatePublication | [PublishRequest](#agntcy-dir-routing-v1-PublishRequest) | [CreatePublicationResponse](#agntcy-dir-routing-v1-CreatePublicationResponse) | CreatePublication creates a new publication request that will be processed by the PublicationWorker. The publication request can specify either a query, a list of specific CIDs, or all records to be announced to the DHT. |
| ListPublications | [ListPublicationsRequest](#agntcy-dir-routing-v1-ListPublicationsRequest) | [ListPublicationsItem](#agntcy-dir-routing-v1-ListPublicationsItem) stream | ListPublications returns a stream of all publication requests in the system. This allows monitoring of pending, processing, and completed publication requests. |
| GetPublication | [GetPublicationRequest](#agntcy-dir-routing-v1-GetPublicationRequest) | [GetPublicationResponse](#agntcy-dir-routing-v1-GetPublicationResponse) | GetPublication retrieves details of a specific publication request by its identifier. This includes the current status and any associated metadata. |

 



<a name="agntcy_dir_routing_v1_record_query-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## agntcy/dir/routing/v1/record_query.proto



<a name="agntcy-dir-routing-v1-RecordQuery"></a>

### RecordQuery
A query to match the record against during discovery.
For example:
 { type: RECORD_QUERY_TYPE_SKILL, value: &#34;Natural Language Processing&#34; }
 { type: RECORD_QUERY_TYPE_LOCATOR, value: &#34;helm-chart&#34; }
 { type: RECORD_QUERY_TYPE_DOMAIN, value: &#34;research&#34; }
 { type: RECORD_QUERY_TYPE_FEATURE, value: &#34;runtime/language&#34; }


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| type | [RecordQueryType](#agntcy-dir-routing-v1-RecordQueryType) |  | The type of the query to match against. |
| value | [string](#string) |  | The query value to match against. |





 


<a name="agntcy-dir-routing-v1-RecordQueryType"></a>

### RecordQueryType
Defines a list of supported record query types.

| Name | Number | Description |
| ---- | ------ | ----------- |
| RECORD_QUERY_TYPE_UNSPECIFIED | 0 | Unspecified query type. |
| RECORD_QUERY_TYPE_SKILL | 1 | Query for a skill name. |
| RECORD_QUERY_TYPE_LOCATOR | 2 | Query for a locator type. |
| RECORD_QUERY_TYPE_DOMAIN | 3 | Query for a domain name. |
| RECORD_QUERY_TYPE_FEATURE | 4 | Query for a feature name. |


 

 

 



<a name="agntcy_dir_routing_v1_routing_service-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## agntcy/dir/routing/v1/routing_service.proto



<a name="agntcy-dir-routing-v1-ListRequest"></a>

### ListRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| queries | [RecordQuery](#agntcy-dir-routing-v1-RecordQuery) | repeated | List of queries to match against the records. If set, all queries must match for the record to be returned. |
| limit | [uint32](#uint32) | optional | Limit the number of results returned. If not set, it will return all records that this peer is providing. |






<a name="agntcy-dir-routing-v1-ListResponse"></a>

### ListResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record_ref | [agntcy.dir.core.v1.RecordRef](#agntcy-dir-core-v1-RecordRef) |  | The record that matches the list queries. |
| labels | [string](#string) | repeated | Labels associated with this record (skills, domains, features) Derived from the record content for CLI display purposes |






<a name="agntcy-dir-routing-v1-PublishRequest"></a>

### PublishRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record_refs | [RecordRefs](#agntcy-dir-routing-v1-RecordRefs) |  | References to the records to be published. |
| queries | [RecordQueries](#agntcy-dir-routing-v1-RecordQueries) |  | Queries to match against the records to be published. |






<a name="agntcy-dir-routing-v1-RecordQueries"></a>

### RecordQueries



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| queries | [agntcy.dir.search.v1.RecordQuery](#agntcy-dir-search-v1-RecordQuery) | repeated |  |






<a name="agntcy-dir-routing-v1-RecordRefs"></a>

### RecordRefs



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| refs | [agntcy.dir.core.v1.RecordRef](#agntcy-dir-core-v1-RecordRef) | repeated |  |






<a name="agntcy-dir-routing-v1-SearchRequest"></a>

### SearchRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| queries | [RecordQuery](#agntcy-dir-routing-v1-RecordQuery) | repeated | List of queries to match against the records. |
| min_match_score | [uint32](#uint32) | optional | Minimal target query match score. For example, if min_match_score=2, it will return records that match at least two of the queries. If not set, it will return records that match at least one query. |
| limit | [uint32](#uint32) | optional | Limit the number of results returned. If not set, it will return all discovered records. Note that this is a soft limit, as the search may return more results than the limit if there are multiple peers providing the same record. |






<a name="agntcy-dir-routing-v1-SearchResponse"></a>

### SearchResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record_ref | [agntcy.dir.core.v1.RecordRef](#agntcy-dir-core-v1-RecordRef) |  | The record that matches the search query. |
| peer | [Peer](#agntcy-dir-routing-v1-Peer) |  | The peer that provided the record. |
| match_queries | [RecordQuery](#agntcy-dir-routing-v1-RecordQuery) | repeated | The queries that were matched. |
| match_score | [uint32](#uint32) |  | The score of the search match. |






<a name="agntcy-dir-routing-v1-UnpublishRequest"></a>

### UnpublishRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record_refs | [RecordRefs](#agntcy-dir-routing-v1-RecordRefs) |  | References to the records to be unpublished. |
| queries | [RecordQueries](#agntcy-dir-routing-v1-RecordQueries) |  | Queries to match against the records to be unpublished. |





 

 

 


<a name="agntcy-dir-routing-v1-RoutingService"></a>

### RoutingService
Defines an interface for announcement and discovery
of records across interconnected network.

Middleware should be used to control who can perform these RPCs.
Policies for the middleware can be handled via separate service.

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| Publish | [PublishRequest](#agntcy-dir-routing-v1-PublishRequest) | [.google.protobuf.Empty](#google-protobuf-Empty) | Announce to the network that this peer is providing a given record. This enables other peers to discover this record and retrieve it from this peer. Listeners can use this event to perform custom operations, for example by cloning the record.

Items need to be periodically republished (eg. 24h) to the network to avoid stale data. Republication should be done in the background. |
| Unpublish | [UnpublishRequest](#agntcy-dir-routing-v1-UnpublishRequest) | [.google.protobuf.Empty](#google-protobuf-Empty) | Stop serving this record to the network. If other peers try to retrieve this record, the peer will refuse the request. |
| Search | [SearchRequest](#agntcy-dir-routing-v1-SearchRequest) | [SearchResponse](#agntcy-dir-routing-v1-SearchResponse) stream | Search records based on the request across the network. This will search the network for the record with the given parameters.

It is possible that the records are stale or that they do not exist. Some records may be provided by multiple peers.

Results from the search can be used as an input to Pull operation to retrieve the records. |
| List | [ListRequest](#agntcy-dir-routing-v1-ListRequest) | [ListResponse](#agntcy-dir-routing-v1-ListResponse) stream | List all records that this peer is currently providing that match the given parameters. This operation does not interact with the network. |

 



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

