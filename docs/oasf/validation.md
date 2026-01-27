# Validation Service

The validation service validates OASF records against an OASF schema server via API validation.
The validation service supports the following features:

- Validates records against any OASF schema server URL.
- Returns detailed validation errors and warnings separately.
- Automatic schema version detection from records.
- Warnings do not affect validation result (only errors cause validation to fail).

## Initialization

Create a validator instance by providing a schema URL:

```go
validator, err := validator.New("https://schema.oasf.outshift.com")
if err != nil {
    // Handle error
}
```

The schema URL is required and must be provided when creating the validator.
The validator uses this URL for all validation operations.

## Validation

Use `ValidateRecord` to validate a record against the configured schema URL.

**Parameters:**

- `ctx`: Context for cancellation and timeout control
- `record`: The OASF record to validate (as a Protocol Buffer Struct)

**Returns:**

- `bool`: Whether the record is valid (true if no errors, false if errors present)
- `[]string`: List of validation error messages (empty if valid)
- `[]string`: List of validation warning messages (may be non-empty even if valid)
- `error`: Any error that occurred during validation

!!! note 
    Warnings do not affect the validation result. A record is considered valid if there are no errors, regardless of whether warnings are present.

## Validation Response

The validation response includes errors and warnings.

Errors are critical validation failures that must be fixed. If any errors are present, the record is invalid. Warnings are non-critical issues or deprecation notices. Warnings do not affect the validation result.

Error messages include the following:

- Clear descriptions of what failed validation.
- Attribute paths (e.g., `data.servers[0]`).
- Constraint details for `constraint_failed` errors.

Warning messages include the following:

- Descriptions of non-critical issues.
- Attribute paths where applicable.

## Example Usage

For detailed examples, see the [OASF SDK repository](https://github.com/agntcy/oasf-sdk/blob/main/USAGE.md).

## Validation Comparison

For a detailed comparison between the API validator and JSON Schema Draft-07 validation, including differences in error handling, warnings, and validation coverage, see the [Validation Comparison](validation-comparison.md) page.
