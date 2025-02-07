---
title : JSONEachRow
slug : /en/interfaces/formats/JSONEachRow
keywords : [JSONEachRow]
---

## Description

In this format, ClickHouse outputs each row as a separated, newline-delimited JSON Object. Alias: `JSONLines`, `NDJSON`.

## Example Usage

Example:

```json
{"num":42,"str":"hello","arr":[0,1]}
{"num":43,"str":"hello","arr":[0,1,2]}
{"num":44,"str":"hello","arr":[0,1,2,3]}
```

While importing data columns with unknown names will be skipped if setting [input_format_skip_unknown_fields](/docs/en/operations/settings/settings-formats.md/#input_format_skip_unknown_fields) is set to 1.

## Format Settings

The `JSONEachRow` format can skip broken rows if a parsing error occurred, and continue parsing from the beginning of the next row.
See [input_format_allow_errors_num](/docs/en/operations/settings/settings-formats.md/#input_format_allow_errors_num) and [input_format_allow_errors_ratio](/docs/en/operations/settings/settings-formats.md/#input_format_allow_errors_ratio) settings.

Limitations:
- In case of a parsing error, `JSONEachRow` skips all data until the new line (or EOF), so rows must be delimited by `\n` to count errors correctly.
- `Template` and `CustomSeparated` use a delimiter after the last column and a delimiter between rows to find the beginning of the next row, so skipping errors works only if at least one of them is not empty.