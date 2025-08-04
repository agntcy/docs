# Store API Reference

<a name="store_v1_object-proto"></a>


## store/v1/object.proto



<a name="store-v1-Object"></a>

### Object
Object is a generic data structure that can hold
arbitrary data. It is used to store and associate
objects in a content-addressable store.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| cid | [string](#string) |  | Globally-unique content identifier of the object. Encodes fully-qualified type of the object as part of &#34;codec&#34;. Specs: https://github.com/multiformats/cid |
| type | [ObjectType](#store-v1-ObjectType) |  | Type of the object. Can be extracted from CID. |
| annotations | [Object.AnnotationsEntry](#store-v1-Object-AnnotationsEntry) | repeated | Metadata associated with the object. |
| created_at | [string](#string) |  | Creation timestamp of the object in the RFC3339 format. Specs: https://www.rfc-editor.org/rfc/rfc3339.html |
| size | [uint64](#uint64) |  | Size of the object in bytes. |
| data | [bytes](#bytes) | optional | Opaque data held by this object. Clients can use {type} to handle processing. |






<a name="store-v1-Object-AnnotationsEntry"></a>

### Object.AnnotationsEntry



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| key | [string](#string) |  |  |
| value | [string](#string) |  |  |






<a name="store-v1-ObjectRef"></a>

### ObjectRef
Reference to a content-addressable object.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| cid | [string](#string) |  | Globally-unique content identifier (CID) of the object. Specs: https://github.com/multiformats/cid |





 


<a name="store-v1-ObjectType"></a>

### ObjectType
Defines a list of supported object data types.
Some values may be reserved for future use.
These types are used as a &#34;codec&#34; in the CID.

| Name | Number | Description |
| ---- | ------ | ----------- |
| OBJECT_TYPE_UNSPECIFIED | 0 | invalid type, should not be used |
| OBJECT_TYPE_RAW | 1 | Common Object Types |


 

 

 



<a name="store_v1_store_service-proto"></a>


## store/v1/store_service.proto



<a name="store-v1-PullOptions"></a>

### PullOptions
PullOptions specifies which artifacts to include in pull operations.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| include_signature | [bool](#bool) |  | Signature to be included |






<a name="store-v1-PullWithOptionsRequest"></a>

### PullWithOptionsRequest
PullWithOptionsRequest specifies which record and artifacts to retrieve.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record_ref | [core.v1.RecordRef](#core-v1-RecordRef) |  | Reference to the record to retrieve |
| options | [PullOptions](#store-v1-PullOptions) |  | Pull options specifying which artifacts to include |






<a name="store-v1-PullWithOptionsResponse"></a>

### PullWithOptionsResponse
PullWithOptionsResponse contains a record and its associated artifacts.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record | [core.v1.Record](#core-v1-Record) |  | Stored record |
| signature | [sign.v1.Signature](#sign-v1-Signature) | optional | Associated signature, if requested and available |






<a name="store-v1-PushOptions"></a>

### PushOptions
PushOptions contains optional artifacts for push operations.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| signature | [sign.v1.Signature](#sign-v1-Signature) | optional | Optional signature to be stored as separate manifest |






<a name="store-v1-PushWithOptionsRequest"></a>

### PushWithOptionsRequest
PushWithOptionsRequest represents a record with optional OCI artifacts for push operations.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record | [core.v1.Record](#core-v1-Record) |  | Record to be stored |
| options | [PushOptions](#store-v1-PushOptions) |  | Push options containing optional artifacts |






<a name="store-v1-PushWithOptionsResponse"></a>

### PushWithOptionsResponse
PushWithOptionsResponse is returned after successfully storing a record with options.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record_ref | [core.v1.RecordRef](#core-v1-RecordRef) |  | Reference to the stored record |





 

 

 


<a name="store-v1-StoreService"></a>

### StoreService
Defines an interface for content-addressable storage
service for objects.

Max object size: 4MB (to fully fit in a single request)
Max metadata size: 100KB

Store service can be implemented by various storage backends,
such as local file system, OCI registry, etc.

Middleware should be used to control who can perform these RPCs.
Policies for the middleware can be handled via separate service.

Each operation is performed sequentially, meaning that
for the N-th request, N-th response will be returned.
If an error occurs, the stream will be cancelled.

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| Push | [.core.v1.Record](#core-v1-Record) stream | [.core.v1.RecordRef](#core-v1-RecordRef) stream | Push performs write operation for given records. |
| Pull | [.core.v1.RecordRef](#core-v1-RecordRef) stream | [.core.v1.Record](#core-v1-Record) stream | Pull performs read operation for given records. |
| Lookup | [.core.v1.RecordRef](#core-v1-RecordRef) stream | [.core.v1.RecordMeta](#core-v1-RecordMeta) stream | Lookup resolves basic metadata for the records. |
| Delete | [.core.v1.RecordRef](#core-v1-RecordRef) stream | [.google.protobuf.Empty](#google-protobuf-Empty) | Remove performs delete operation for the records. |
| PushWithOptions | [PushWithOptionsRequest](#store-v1-PushWithOptionsRequest) stream | [PushWithOptionsResponse](#store-v1-PushWithOptionsResponse) stream | PushWithOptions performs write operation for records with optional OCI artifacts like signatures. |
| PullWithOptions | [PullWithOptionsRequest](#store-v1-PullWithOptionsRequest) stream | [PullWithOptionsResponse](#store-v1-PullWithOptionsResponse) stream | PullWithOptions retrieves records along with their associated OCI artifacts. |

 



<a name="store_v1_sync_service-proto"></a>


## store/v1/sync_service.proto



<a name="store-v1-BasicAuthCredentials"></a>

### BasicAuthCredentials
Supporting credential type definitions


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| username | [string](#string) |  |  |
| password | [string](#string) |  |  |






<a name="store-v1-CreateSyncRequest"></a>

### CreateSyncRequest
CreateSyncRequest defines the parameters for creating a new synchronization operation.

Currently supports basic synchronization of all objects from a remote Directory.
Future versions may include additional options for filtering and scheduling capabilities.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| remote_directory_url | [string](#string) |  | URL of the remote Registry to synchronize from.

This should be a complete URL including protocol and port if non-standard. Examples: - &#34;https://directory.example.com&#34; - &#34;http://localhost:8080&#34; - &#34;https://directory.example.com:9443&#34; |






<a name="store-v1-CreateSyncResponse"></a>

### CreateSyncResponse
CreateSyncResponse contains the result of creating a new synchronization operation.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| sync_id | [string](#string) |  | Unique identifier for the created synchronization operation. This ID can be used with other SyncService RPCs to monitor and manage the sync. |






<a name="store-v1-DeleteSyncRequest"></a>

### DeleteSyncRequest
DeleteSyncRequest specifies which synchronization to delete.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| sync_id | [string](#string) |  | Unique identifier of the synchronization operation to delete. |






<a name="store-v1-DeleteSyncResponse"></a>

### DeleteSyncResponse
DeleteSyncResponse






<a name="store-v1-GetSyncRequest"></a>

### GetSyncRequest
GetSyncRequest specifies which synchronization status to retrieve.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| sync_id | [string](#string) |  | Unique identifier of the synchronization operation to query. |






<a name="store-v1-GetSyncResponse"></a>

### GetSyncResponse
GetSyncResponse provides detailed information about a specific synchronization operation.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| sync_id | [string](#string) |  | Unique identifier of the synchronization operation. |
| status | [SyncStatus](#store-v1-SyncStatus) |  | Current status of the synchronization operation. |
| remote_directory_url | [string](#string) |  | URL of the remote Directory node being synchronized from. |
| created_time | [string](#string) |  | Timestamp when the synchronization operation was created in the RFC3339 format. Specs: https://www.rfc-editor.org/rfc/rfc3339.html |
| last_update_time | [string](#string) |  | Timestamp of the most recent status update for this synchronization in the RFC3339 format. |






<a name="store-v1-ListSyncsItem"></a>

### ListSyncsItem
ListSyncItem represents a single synchronization in the list of all syncs.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| sync_id | [string](#string) |  | Unique identifier of the synchronization operation. |
| status | [SyncStatus](#store-v1-SyncStatus) |  | Current status of the synchronization operation. |
| remote_directory_url | [string](#string) |  | URL of the remote Directory being synchronized from. |






<a name="store-v1-ListSyncsRequest"></a>

### ListSyncsRequest
ListSyncsRequest specifies parameters for listing synchronization operations.


| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| limit | [uint32](#uint32) | optional | Optional limit on the number of results to return. |
| offset | [uint32](#uint32) | optional | Optional offset for pagination of results. |






<a name="store-v1-RequestRegistryCredentialsRequest"></a>

### RequestRegistryCredentialsRequest



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| requesting_node_id | [string](#string) |  | Identity of the requesting node For example: spiffe://example.org/service/foo |






<a name="store-v1-RequestRegistryCredentialsResponse"></a>

### RequestRegistryCredentialsResponse



| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| success | [bool](#bool) |  | Success status of the credential negotiation |
| error_message | [string](#string) |  | Error message if negotiation failed |
| remote_registry_url | [string](#string) |  | URL of the remote Registry being synchronized from. |
| basic_auth | [BasicAuthCredentials](#store-v1-BasicAuthCredentials) |  | CertificateCredentials certificate = 5; |





 


<a name="store-v1-SyncStatus"></a>

### SyncStatus
SyncStatus enumeration defines the possible states of a synchronization operation.

| Name | Number | Description |
| ---- | ------ | ----------- |
| SYNC_STATUS_UNSPECIFIED | 0 | Default/unset status - should not be used in practice |
| SYNC_STATUS_PENDING | 1 | Sync operation has been created but not yet started |
| SYNC_STATUS_IN_PROGRESS | 2 | Sync operation is actively discovering and transferring objects |
| SYNC_STATUS_FAILED | 3 | Sync operation encountered an error and stopped |
| SYNC_STATUS_DELETE_PENDING | 4 | Sync operation has been marked for deletion but cleanup not yet started |
| SYNC_STATUS_DELETED | 5 | Sync operation has been successfully deleted and cleaned up |


 

 


<a name="store-v1-SyncService"></a>

### SyncService
SyncService provides functionality for synchronizing objects between Directory nodes.

This service enables one-way synchronization from a remote Directory node to the local node,
allowing distributed Directory instances to share and replicate objects. The service supports
both on-demand synchronization and tracking of sync operations through their lifecycle.

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| CreateSync | [CreateSyncRequest](#store-v1-CreateSyncRequest) | [CreateSyncResponse](#store-v1-CreateSyncResponse) | CreateSync initiates a new synchronization operation from a remote Directory node.

The operation is non-blocking and returns immediately with a sync ID that can be used to track progress and manage the sync operation. |
| ListSyncs | [ListSyncsRequest](#store-v1-ListSyncsRequest) | [ListSyncsItem](#store-v1-ListSyncsItem) stream | ListSyncs returns a stream of all sync operations known to the system.

This includes active, completed, and failed synchronizations. |
| GetSync | [GetSyncRequest](#store-v1-GetSyncRequest) | [GetSyncResponse](#store-v1-GetSyncResponse) | GetSync retrieves detailed status information for a specific synchronization. |
| DeleteSync | [DeleteSyncRequest](#store-v1-DeleteSyncRequest) | [DeleteSyncResponse](#store-v1-DeleteSyncResponse) | DeleteSync removes a synchronization operation from the system. |
| RequestRegistryCredentials | [RequestRegistryCredentialsRequest](#store-v1-RequestRegistryCredentialsRequest) | [RequestRegistryCredentialsResponse](#store-v1-RequestRegistryCredentialsResponse) | RequestRegistryCredentials requests registry credentials between two Directory nodes.

This RPC allows a requesting node to authenticate with this node and obtain temporary registry credentials for secure Zot-based synchronization. |

 



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

