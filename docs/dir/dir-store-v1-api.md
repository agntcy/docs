# Protocol Documentation
<a name="top"></a>

## Table of Contents

- [agntcy/dir/store/v1/store_service.proto](#agntcy_dir_store_v1_store_service-proto)
  - [PullReferrerRequest](#agntcy-dir-store-v1-PullReferrerRequest)
  - [PullReferrerResponse](#agntcy-dir-store-v1-PullReferrerResponse)
  - [PushReferrerRequest](#agntcy-dir-store-v1-PushReferrerRequest)
  - [PushReferrerResponse](#agntcy-dir-store-v1-PushReferrerResponse)
  
  - [StoreService](#agntcy-dir-store-v1-StoreService)
  
- [agntcy/dir/store/v1/sync_service.proto](#agntcy_dir_store_v1_sync_service-proto)
  - [BasicAuthCredentials](#agntcy-dir-store-v1-BasicAuthCredentials)
  - [CreateSyncRequest](#agntcy-dir-store-v1-CreateSyncRequest)
  - [CreateSyncResponse](#agntcy-dir-store-v1-CreateSyncResponse)
  - [DeleteSyncRequest](#agntcy-dir-store-v1-DeleteSyncRequest)
  - [DeleteSyncResponse](#agntcy-dir-store-v1-DeleteSyncResponse)
  - [GetSyncRequest](#agntcy-dir-store-v1-GetSyncRequest)
  - [GetSyncResponse](#agntcy-dir-store-v1-GetSyncResponse)
  - [ListSyncsItem](#agntcy-dir-store-v1-ListSyncsItem)
  - [ListSyncsRequest](#agntcy-dir-store-v1-ListSyncsRequest)
  - [RequestRegistryCredentialsRequest](#agntcy-dir-store-v1-RequestRegistryCredentialsRequest)
  - [RequestRegistryCredentialsResponse](#agntcy-dir-store-v1-RequestRegistryCredentialsResponse)
  
  - [SyncStatus](#agntcy-dir-store-v1-SyncStatus)
  
  - [SyncService](#agntcy-dir-store-v1-SyncService)
  
- [Scalar Value Types](#scalar-value-types)

<a name="agntcy_dir_store_v1_store_service-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## agntcy/dir/store/v1/store_service.proto

<a name="agntcy-dir-store-v1-PullReferrerRequest"></a>

### PullReferrerRequest
PullReferrerRequest represents a record with optional OCI artifacts for pull operations.

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record_ref | [agntcy.dir.core.v1.RecordRef](#agntcy-dir-core-v1-RecordRef) |  | Record reference |
| pull_signature | [bool](#bool) |  | Pull signature referrer |
| pull_public_key | [bool](#bool) |  | Pull public key referrer |

<a name="agntcy-dir-store-v1-PullReferrerResponse"></a>

### PullReferrerResponse
PullReferrerResponse is returned after successfully fetching a record referrer.

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| signature | [agntcy.dir.sign.v1.Signature](#agntcy-dir-sign-v1-Signature) |  | Signature to be fetched as a referrer |
| public_key | [string](#string) |  | Public key to be fetched as a referrer |

<a name="agntcy-dir-store-v1-PushReferrerRequest"></a>

### PushReferrerRequest
PushReferrerRequest represents a record with optional OCI artifacts for push operations.

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| record_ref | [agntcy.dir.core.v1.RecordRef](#agntcy-dir-core-v1-RecordRef) |  | Record reference |
| signature | [agntcy.dir.sign.v1.Signature](#agntcy-dir-sign-v1-Signature) |  | Signature to be stored as a referrer for the record |
| public_key | [string](#string) |  | Public key to be stored as a referrer for the record and uploaded as a file to zot for verification |

<a name="agntcy-dir-store-v1-PushReferrerResponse"></a>

### PushReferrerResponse
PushReferrerResponse

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| success | [bool](#bool) |  | The push process result |
| error_message | [string](#string) | optional | Optional error message if push failed |

<a name="agntcy-dir-store-v1-StoreService"></a>

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
| Push | [.agntcy.dir.core.v1.Record](#agntcy-dir-core-v1-Record) stream | [.agntcy.dir.core.v1.RecordRef](#agntcy-dir-core-v1-RecordRef) stream | Push performs write operation for given records. |
| Pull | [.agntcy.dir.core.v1.RecordRef](#agntcy-dir-core-v1-RecordRef) stream | [.agntcy.dir.core.v1.Record](#agntcy-dir-core-v1-Record) stream | Pull performs read operation for given records. |
| Lookup | [.agntcy.dir.core.v1.RecordRef](#agntcy-dir-core-v1-RecordRef) stream | [.agntcy.dir.core.v1.RecordMeta](#agntcy-dir-core-v1-RecordMeta) stream | Lookup resolves basic metadata for the records. |
| Delete | [.agntcy.dir.core.v1.RecordRef](#agntcy-dir-core-v1-RecordRef) stream | [.google.protobuf.Empty](#google-protobuf-Empty) | Remove performs delete operation for the records. |
| PushReferrer | [PushReferrerRequest](#agntcy-dir-store-v1-PushReferrerRequest) stream | [PushReferrerResponse](#agntcy-dir-store-v1-PushReferrerResponse) stream | PushReferrer performs write operation for record referrers. |
| PullReferrer | [PullReferrerRequest](#agntcy-dir-store-v1-PullReferrerRequest) stream | [PullReferrerResponse](#agntcy-dir-store-v1-PullReferrerResponse) stream | PullReferrer performs read operation for record referrers. |

<a name="agntcy_dir_store_v1_sync_service-proto"></a>
<p align="right"><a href="#top">Top</a></p>

## agntcy/dir/store/v1/sync_service.proto

<a name="agntcy-dir-store-v1-BasicAuthCredentials"></a>

### BasicAuthCredentials
Supporting credential type definitions

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| username | [string](#string) |  |  |
| password | [string](#string) |  |  |

<a name="agntcy-dir-store-v1-CreateSyncRequest"></a>

### CreateSyncRequest
CreateSyncRequest defines the parameters for creating a new synchronization operation.

Currently supports basic synchronization of all objects from a remote Directory.
Future versions may include additional options for filtering and scheduling capabilities.

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| remote_directory_url | [string](#string) |  | URL of the remote Registry to synchronize from.

This should be a complete URL including protocol and port if non-standard. Examples: - &#34;https://directory.example.com&#34; - &#34;http://localhost:8080&#34; - &#34;https://directory.example.com:9443&#34; |
| cids | [string](#string) | repeated | List of CIDs to synchronize from the remote Directory. If empty, all objects will be synchronized. |

<a name="agntcy-dir-store-v1-CreateSyncResponse"></a>

### CreateSyncResponse
CreateSyncResponse contains the result of creating a new synchronization operation.

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| sync_id | [string](#string) |  | Unique identifier for the created synchronization operation. This ID can be used with other SyncService RPCs to monitor and manage the sync. |

<a name="agntcy-dir-store-v1-DeleteSyncRequest"></a>

### DeleteSyncRequest
DeleteSyncRequest specifies which synchronization to delete.

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| sync_id | [string](#string) |  | Unique identifier of the synchronization operation to delete. |

<a name="agntcy-dir-store-v1-DeleteSyncResponse"></a>

### DeleteSyncResponse
DeleteSyncResponse

<a name="agntcy-dir-store-v1-GetSyncRequest"></a>

### GetSyncRequest
GetSyncRequest specifies which synchronization status to retrieve.

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| sync_id | [string](#string) |  | Unique identifier of the synchronization operation to query. |

<a name="agntcy-dir-store-v1-GetSyncResponse"></a>

### GetSyncResponse
GetSyncResponse provides detailed information about a specific synchronization operation.

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| sync_id | [string](#string) |  | Unique identifier of the synchronization operation. |
| status | [SyncStatus](#agntcy-dir-store-v1-SyncStatus) |  | Current status of the synchronization operation. |
| remote_directory_url | [string](#string) |  | URL of the remote Directory node being synchronized from. |
| created_time | [string](#string) |  | Timestamp when the synchronization operation was created in the RFC3339 format. Specs: https://www.rfc-editor.org/rfc/rfc3339.html |
| last_update_time | [string](#string) |  | Timestamp of the most recent status update for this synchronization in the RFC3339 format. |

<a name="agntcy-dir-store-v1-ListSyncsItem"></a>

### ListSyncsItem
ListSyncItem represents a single synchronization in the list of all syncs.

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| sync_id | [string](#string) |  | Unique identifier of the synchronization operation. |
| status | [SyncStatus](#agntcy-dir-store-v1-SyncStatus) |  | Current status of the synchronization operation. |
| remote_directory_url | [string](#string) |  | URL of the remote Directory being synchronized from. |

<a name="agntcy-dir-store-v1-ListSyncsRequest"></a>

### ListSyncsRequest
ListSyncsRequest specifies parameters for listing synchronization operations.

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| limit | [uint32](#uint32) | optional | Optional limit on the number of results to return. |
| offset | [uint32](#uint32) | optional | Optional offset for pagination of results. |

<a name="agntcy-dir-store-v1-RequestRegistryCredentialsRequest"></a>

### RequestRegistryCredentialsRequest

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| requesting_node_id | [string](#string) |  | Identity of the requesting node For example: spiffe://example.org/service/foo |

<a name="agntcy-dir-store-v1-RequestRegistryCredentialsResponse"></a>

### RequestRegistryCredentialsResponse

| Field | Type | Label | Description |
| ----- | ---- | ----- | ----------- |
| success | [bool](#bool) |  | Success status of the credential negotiation |
| error_message | [string](#string) |  | Error message if negotiation failed |
| remote_registry_url | [string](#string) |  | URL of the remote Registry being synchronized from. |
| basic_auth | [BasicAuthCredentials](#agntcy-dir-store-v1-BasicAuthCredentials) |  | CertificateCredentials certificate = 5; |

<a name="agntcy-dir-store-v1-SyncStatus"></a>

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

<a name="agntcy-dir-store-v1-SyncService"></a>

### SyncService
SyncService provides functionality for synchronizing objects between Directory nodes.

This service enables one-way synchronization from a remote Directory node to the local node,
allowing distributed Directory instances to share and replicate objects. The service supports
both on-demand synchronization and tracking of sync operations through their lifecycle.

| Method Name | Request Type | Response Type | Description |
| ----------- | ------------ | ------------- | ------------|
| CreateSync | [CreateSyncRequest](#agntcy-dir-store-v1-CreateSyncRequest) | [CreateSyncResponse](#agntcy-dir-store-v1-CreateSyncResponse) | CreateSync initiates a new synchronization operation from a remote Directory node.

The operation is non-blocking and returns immediately with a sync ID that can be used to track progress and manage the sync operation. |
| ListSyncs | [ListSyncsRequest](#agntcy-dir-store-v1-ListSyncsRequest) | [ListSyncsItem](#agntcy-dir-store-v1-ListSyncsItem) stream | ListSyncs returns a stream of all sync operations known to the system.

This includes active, completed, and failed synchronizations. |
| GetSync | [GetSyncRequest](#agntcy-dir-store-v1-GetSyncRequest) | [GetSyncResponse](#agntcy-dir-store-v1-GetSyncResponse) | GetSync retrieves detailed status information for a specific synchronization. |
| DeleteSync | [DeleteSyncRequest](#agntcy-dir-store-v1-DeleteSyncRequest) | [DeleteSyncResponse](#agntcy-dir-store-v1-DeleteSyncResponse) | DeleteSync removes a synchronization operation from the system. |
| RequestRegistryCredentials | [RequestRegistryCredentialsRequest](#agntcy-dir-store-v1-RequestRegistryCredentialsRequest) | [RequestRegistryCredentialsResponse](#agntcy-dir-store-v1-RequestRegistryCredentialsResponse) | RequestRegistryCredentials requests registry credentials between two Directory nodes.

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
