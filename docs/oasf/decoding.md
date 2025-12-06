# Decoding Service

The decoding service converts between different data formats and creates OASF-compliant records.

## `JsonToProto`

Converts a JSON object to a Protocol Buffer Struct.

```go
func JsonToProto(data []byte) (*structpb.Struct, error)
```

**Parameters:**

* `data`: JSON data as byte array

Returns `*structpb.Struct`: Protocol Buffer Struct representation.

## `StructToProto`

Converts a Go struct to a Protocol Buffer Struct.

```go
func StructToProto(goObj any) (*structpb.Struct, error)
```

**Parameters:**

* `goObj`: Any Go struct or object

Returns `*structpb.Struct`: Protocol Buffer Struct representation.

## `ProtoToStruct`

Converts a Protocol Buffer Struct to a Go struct.

```go
func ProtoToStruct[T any](obj *structpb.Struct) (*T, error)
```

**Parameters:**

* `obj`: Protocol Buffer Struct to convert

Returns `*T`: Pointer to the converted Go struct.

## `DecodeRecord`

Decodes a record object into a structured format based on its schema version.

```go
func DecodeRecord(record *structpb.Struct) (*decodingv1.DecodeRecordResponse, error)
```

**Parameters:**

* `record`: OASF record as Protocol Buffer Struct

Returns `*decodingv1.DecodeRecordResponse`: decoded record response with version-specific structure.

## `GetRecordSchemaVersion`

Extracts the schema version from a record object.

```go
func GetRecordSchemaVersion(record *structpb.Struct) (string, error)
```

**Parameters:**

* `record`: OASF record as Protocol Buffer Struct

Returns `string`: schema version (e.g., "0.3.1", "0.7.0").
