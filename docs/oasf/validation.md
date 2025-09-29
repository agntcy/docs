# Validation Service

The validation service validates OASF records against JSON schemas. It supports both embedded schemas and custom schema URLs. The validation service supports the following features:

* Validates records against embedded schema versions (v0.3.1 and v0.7.0).
* Supports custom schema URLs for remote validation.
* Returns detailed validation errors.
* Automatic schema version detection from records.

Use `ValidateRecord` to validate a record against a specified schema URL or its embedded schema version.

**Parameters:**

* `record`: The OASF record to validate (as a Protocol Buffer Struct)
* `options`: Optional validation options

**Returns:**

* `bool`: Whether the record is valid
* `[]string`: List of validation errors (empty if valid)
* `error`: Any error that occurred during validation

**Options:**

* `WithSchemaURL(url string)`: Validate against a custom schema URL instead of embedded schemas

## Example Usage

For detailed examples, see the [OASF SDK repository](https://github.com/agntcy/oasf-sdk/blob/main/USAGE.md).
