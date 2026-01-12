# Validation Comparison: API Validator vs JSON Schema Draft-07

This table compares validation outcomes between the OASF API validator and JSON Schema Draft-07 validator.

## Legend

- **API Error**:
  API validator returns ERROR
- **API Warning**:
  API validator returns WARNING
- **JSON Schema Pass**:
  JSON Schema Draft-07 validation passes
- **JSON Schema Fail**:
  JSON Schema Draft-07 validation fails

## Comparison Table

| Case                                         | Example                                                               | API Validator                                            | JSON Schema | Notes                                                                                                              |
| -------------------------------------------- | --------------------------------------------------------------------- | -------------------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------ |
| **1.
  Version Incompatibility (Later)**       | `schema_version: "1.0.0"` when server is `0.8.0`                      | ERROR (`version_incompatible_later`)                     | PASS        | JSON Schema validates format only, not semantic compatibility \*                                                   |
| **2.
  Version Incompatibility (Initial Dev)** | `schema_version: "0.1.0"` when server is `0.8.0`                      | ERROR (`version_incompatible_initial_development`)       | PASS        | JSON Schema validates format only, not SemVer rules \*                                                             |
| **3.
  Version Incompatibility (Prerelease)**  | `schema_version: "0.8.0-alpha"` when server is `0.8.0`                | ERROR (`version_incompatible_prerelease`)                | PASS        | JSON Schema validates format only, not prerelease compatibility \*                                                 |
| **4.
  Version Earlier (Compatible)**          | `schema_version: "0.7.0"` when server is `0.8.0`                      | WARNING (`version_earlier`)                              | PASS        | JSON Schema validates format only, not version comparison \*                                                       |
| **5.
  Regex Pattern Mismatch**                | `previous_record_cid: "invalid"` (doesn't match CID regex)            | WARNING (`attribute_value_regex_not_matched`)            | PASS        | JSON Schema may export regex but validation is lenient; API treats as warning                                      |
| **6.
  Regex Pattern Mismatch (Super Type)**   | String doesn't match super type regex                                 | WARNING (`attribute_value_super_type_regex_not_matched`) | PASS        | Same as above for super types                                                                                      |
| **7.
  Using Base Class**                      | `skills: [{"name": "base_skill"}]` or `skills: [{"id": 0}]`           | ERROR (`base_class_used`)                                | FAIL        | Both catch base classes (base_skill, base_domain, base_module); JSON Schema `oneOf` doesn't include parent classes |
| **8.
  Using Deprecated Class**                | Using a deprecated skill/domain/module                                | WARNING (`class_deprecated`)                             | PASS        | JSON Schema doesn't track deprecation                                                                              |
| **9.
  Using Deprecated Attribute**            | Using a deprecated attribute                                          | WARNING (`attribute_deprecated`)                         | PASS        | JSON Schema doesn't track deprecation                                                                              |
| **10.
  Using Deprecated Object**              | Using a deprecated object                                             | WARNING (`object_deprecated`)                            | PASS        | JSON Schema doesn't track deprecation                                                                              |
| **11.
  Using Deprecated Enum Value**          | Using a deprecated enum value                                         | WARNING (`attribute_enum_value_deprecated`)              | PASS        | JSON Schema doesn't track deprecation                                                                              |
| **12.
  Using Deprecated Enum Array Value**    | Using a deprecated enum array value                                   | WARNING (`attribute_enum_array_value_deprecated`)        | PASS        | JSON Schema doesn't track deprecation                                                                              |
| **13.
  Enum Sibling Mismatch**                | Enum value doesn't match sibling caption                              | WARNING (`attribute_enum_sibling_incorrect`)             | PASS        | JSON Schema doesn't validate enum siblings                                                                         |
| **14.
  Enum Sibling Suspicious (Other)**      | Enum value 99 with matching sibling caption                           | WARNING (`attribute_enum_sibling_suspicious_other`)      | PASS        | JSON Schema doesn't validate enum siblings                                                                         |
| **15.
  Missing Recommended Attribute**        | Required attribute missing (if `warn_on_missing_recommended` enabled) | WARNING (`attribute_recommended_missing`)                | PASS        | JSON Schema only validates `required`, not `recommended`                                                           |
| **16.
  Empty Required Array**                 | `skills: []` when skills is required                                  | ERROR (`attribute_required_empty`)                       | FAIL        | JSON Schema now includes `minItems: 1` for required arrays (after fix)                                             |
| **17.
  Wrong Type**                           | `name: 123` when name should be string                                | ERROR (`attribute_wrong_type`)                           | FAIL        | Both catch type mismatches                                                                                         |
| **18.
  Missing Required Attribute**           | Missing required `name` field                                         | ERROR (`attribute_required_missing`)                     | FAIL        | Both catch missing required fields                                                                                 |
| **19.
  Unknown Attribute**                    | Extra attribute not in schema                                         | ERROR (`attribute_unknown`)                              | FAIL        | JSON Schema uses `additionalProperties: false`                                                                     |
| **20.
  Unknown Enum Value**                   | Enum value not in allowed list                                        | ERROR (`attribute_enum_value_unknown`)                   | FAIL        | JSON Schema uses `enum` constraint                                                                                 |
| **21.
  Unknown Enum Array Value**             | Enum array value not in allowed list                                  | ERROR (`attribute_enum_array_value_unknown`)             | FAIL        | JSON Schema validates array items                                                                                  |
| **22.
  Value Outside Range**                  | Number outside type's range                                           | ERROR (`attribute_value_exceeds_range`)                  | FAIL        | JSON Schema uses `minimum`/`maximum`                                                                               |
| **23.
  Value Exceeds Max Length**             | String exceeds type's max length                                      | ERROR (`attribute_value_exceeds_max_len`)                | FAIL        | JSON Schema uses `maxLength`                                                                                       |
| **24.
  Value Not in Type Values**             | Value not in type's allowed values list                               | ERROR (`attribute_value_not_in_type_values`)             | FAIL        | JSON Schema uses `enum` constraint                                                                                 |
| **25.
  Unknown Class ID**                     | `id: 99999` doesn't exist                                             | ERROR (`id_unknown`)                                     | FAIL        | JSON Schema uses `oneOf` with `const` values                                                                       |
| **26.
  Unknown Class Name**                   | `name: "nonexistent"` doesn't exist                                   | ERROR (`name_unknown`)                                   | FAIL        | JSON Schema uses `oneOf` with `const` values                                                                       |
| **27.
  ID/Name Mismatch**                     | `id: 2` and `name: "different"` refer to different classes            | ERROR (`id_name_mismatch`)                               | FAIL        | JSON Schema `oneOf` with `const` prevents mismatches                                                               |
| **28.
  Constraint Failed (at_least_one)**     | None of the constraint fields present                                 | ERROR (`constraint_failed`)                              | FAIL        | JSON Schema uses `anyOf` for `at_least_one`                                                                        |
| **29.
  Constraint Failed (just_one)**         | Both fields in `just_one` constraint present                          | ERROR (`constraint_failed`)                              | FAIL        | JSON Schema `oneOf` pattern correctly prevents both fields from being present                                      |
| **30.
  Enum Array Sibling Missing**           | Enum array sibling array too short                                    | ERROR (`attribute_enum_array_sibling_missing`)           | PASS        | JSON Schema doesn't validate enum array siblings                                                                   |
| **31.
  Enum Array Sibling Incorrect**         | Enum array sibling value doesn't match                                | ERROR (`attribute_enum_array_sibling_incorrect`)         | PASS        | JSON Schema doesn't validate enum array siblings                                                                   |
| **32.
  Enum Object Not Matched**              | Enum object doesn't match any allowed objects                         | ERROR (`enum_object_not_matched`)                        | FAIL        | JSON Schema uses `oneOf` for enum objects                                                                          |
| **33.
  Unknown Profile**                      | Profile in `metadata.profiles` doesn't exist                          | ERROR (`profile_unknown`)                                | PASS        | JSON Schema validates structure but not profile existence (only for classes, not record)                           |
| **34.
  Invalid Version Format**               | `schema_version: "invalid"`                                           | ERROR (`version_invalid_format`)                         | FAIL        | JSON Schema validates semantic versioning format \*                                                                |
| **35.
  Array Duplicates**                     | Duplicate items in array (e.g., same skill twice)                     | ERROR (`attribute_array_duplicate`)                      | FAIL        | Both catch duplicates; JSON Schema uses `uniqueItems: true`                                                        |
| **36.
  Locators Duplicate Types**             | Multiple locators with same type                                      | ERROR (`attribute_locators_duplicate_type`)              | FAIL        | Both catch duplicate types in locators array; JSON Schema uses `uniqueItems: true`                                 |

\* **Note on schema_version validation**:
 When using oasf-sdk, any schema version that is not explicitly supported by the decoder (currently:
 0.3.1, 0.7.0, 0.8.0) will result in a failure, regardless of whether the API validator returns an error or warning.
 The SDK uses a switch statement that only handles specific versions, and any non-supported version will return an error:
 `unsupported OASF version:
 <version>`.

## Summary by Category

### API ERROR, JSON Schema PASSES (Gaps in JSON Schema)

1. Version incompatibility (later, initial dev, prerelease)
2. Enum array sibling validation (missing, incorrect)
3. Unknown profile (for classes)

### API WARNING, JSON Schema PASSES (Non-blocking Issues)

1. Version earlier (compatible)
2. Regex pattern mismatches
3. All deprecation warnings (class, attribute, object, enum values)
4. Enum sibling mismatches
5. Missing recommended attributes

### Both FAIL (Both Catch the Issue)

1. Empty required arrays
2. Wrong types
3. Missing required attributes
4. Unknown attributes
5. Unknown enum values
6. Value range/length violations
7. Unknown class ID/name (including unknown modules, skills, domains)
8. ID/name mismatches
9. Constraint violations (`just_one`, `at_least_one`)
10. Enum object mismatches
11. Invalid version format
12. Using base classes (base_skill, base_domain, base_module)
13. Array duplicates (duplicate items in arrays)
14. Locators duplicate types (duplicate types in locators array)

## Key Insights

1. **JSON Schema is comprehensive** for structural and value validation
2. **Main gaps in JSON Schema**:
   - Semantic version compatibility (only validates format)
   - Enum array sibling validation
   - Deprecation tracking
   - Regex validation (treated as warnings, not errors)
   - Profile existence (for classes)

3. **Both validators catch** most structural and type validation issues, including:
   - Base classes (now errors in API validator, matching JSON Schema behavior)
   - Array duplicates (both use duplicate detection)
   - Locators duplicate types (both catch duplicate types in locators array)
   - Unknown classes (modules, skills, domains - all treated the same way)
