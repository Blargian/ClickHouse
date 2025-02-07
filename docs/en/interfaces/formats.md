---
slug: /en/interfaces/formats
sidebar_position: 21
sidebar_label: View all formats...
title: Formats for Input and Output Data
---

import CloudNotSupportedBadge from '@theme/badges/CloudNotSupportedBadge';

## Overview

ClickHouse can accept and return data in various formats. A format supported for input can be used to parse the data provided to `INSERT`s, to perform `SELECT`s from a file-backed table such as File, URL or HDFS, or to read a dictionary. A format supported for output can be used to arrange the
results of a `SELECT`, and to perform `INSERT`s into a file-backed table.

:::note
All format names are case-insensitive.
:::

## Supported formats

The supported formats are:

| Format                                                                                                   | Input | Output |
|----------------------------------------------------------------------------------------------------------|-------|--------|
| [TabSeparated](formats/TabSeparated/TabSeparated.md)                                                     | ✔     | ✔      |
| [TabSeparatedRaw](formats/TabSeparatedRaw)                                                               | ✔     | ✔      |
| [TabSeparatedWithNames](formats/TabSeparated/TabSeparatedWithNames.md)                                   | ✔     | ✔      |
| [TabSeparatedWithNamesAndTypes](formats/TabSeparated/TabSeparatedWithNamesAndTypes.md)                   | ✔     | ✔      |
| [TabSeparatedRawWithNames](formats/TabSeparated/TabSeparatedRawWithNames.md)                             | ✔     | ✔      |
| [TabSeparatedRawWithNamesAndTypes](formats/TabSeparated/TabSeparatedRawWithNamesAndTypes.md)             | ✔     | ✔      |
| [Template](formats/Template)                                                                             | ✔     | ✔      |
| [TemplateIgnoreSpaces](formats/Template/TemplateIgnoreSpaces.md)                                         | ✔     | ✗      |
| [CSV](formats/CSV/CSV.md)                                                                                | ✔     | ✔      |
| [CSVWithNames](formats/CSV/CSVWithNames.md)                                                              | ✔     | ✔      |
| [CSVWithNamesAndTypes](formats/CSV/CSVWithNamesAndTypes.md)                                              | ✔     | ✔      |
| [CustomSeparated](formats/CustomSeparated/CustomSeparated.md)                                            | ✔     | ✔      |
| [CustomSeparatedWithNames](formats/CustomSeparated/CustomSeparatedWithNames.md)                          | ✔     | ✔      |
| [CustomSeparatedWithNamesAndTypes](formats/CustomSeparated/CustomSeparatedWithNamesAndTypes.md)          | ✔     | ✔      |
| [SQLInsert](formats/SQLInsert.md)                                                                        | ✗     | ✔      |
| [Values](formats/Values.md)                                                                              | ✔     | ✔      |
| [Vertical](formats/Vertical.md)                                                                          | ✗     | ✔      |
| [JSON](formats/JSON/JSON.md)                                                                             | ✔     | ✔      |
| [JSONAsString](formats/JSON/JSONAsString.md)                                                             | ✔     | ✗      |
| [JSONAsObject](formats/JSON/JSONAsObject.md)                                                             | ✔     | ✗      |
| [JSONStrings](formats/JSON/JSONStrings.md)                                                               | ✔     | ✔      |
| [JSONColumns](formats/JSON/JSONColumns.md)                                                               | ✔     | ✔      |
| [JSONColumnsWithMetadata](formats/JSON/JSONColumnsWithMetadata.md)                                       | ✔     | ✔      |
| [JSONCompact](formats/JSON/JSONCompact.md)                                                               | ✔     | ✔      |
| [JSONCompactStrings](formats/JSON/JSONCompactStrings.md)                                                 | ✗     | ✔      |
| [JSONCompactColumns](formats/JSON/JSONCompactColumns.md)                                                 | ✔     | ✔      |
| [JSONEachRow](formats/JSON/JSONEachRow.md)                                                               | ✔     | ✔      |
| [PrettyJSONEachRow](formats/JSON/PrettyJSONEachRow.md)                                                   | ✗     | ✔      |
| [JSONEachRowWithProgress](formats/JSON/JSONEachRowWithProgress.md)                                       | ✗     | ✔      |
| [JSONStringsEachRow](formats/JSON/JSONStringsEachRow.md)                                                 | ✔     | ✔      |
| [JSONStringsEachRowWithProgress](formats/JSON/JSONStringsEachRowWithProgress.md)                         | ✗     | ✔      |
| [JSONCompactEachRow](formats/JSON/JSONCompactEachRow.md)                                                 | ✔     | ✔      |
| [JSONCompactEachRowWithNames](formats/JSON/JSONCompactEachRowWithNames.md)                               | ✔     | ✔      |
| [JSONCompactEachRowWithNamesAndTypes](formats/JSON/JSONCompactEachRowWithNamesAndTypes.md)               | ✔     | ✔      |
| [JSONCompactStringsEachRow](formats/JSON/JSONCompactStringsEachRow.md)                                   | ✔     | ✔      |
| [JSONCompactStringsEachRowWithNames](formats/JSON/JSONCompactStringsEachRowWithNames.md)                 | ✔     | ✔      |
| [JSONCompactStringsEachRowWithNamesAndTypes](formats/JSON/JSONCompactStringsEachRowWithNamesAndTypes.md) | ✔     | ✔      |
| [JSONObjectEachRow](formats/JSON/JSONObjectEachRow.md)                                                   | ✔     | ✔      |
| [BSONEachRow](formats/BSONEachRow.md)                                                                    | ✔     | ✔      |
| [TSKV](formats/TabSeparated/TSKV.md)                                                                     | ✔     | ✔      |
| [Pretty](formats/Pretty/Pretty.md)                                                                       | ✗     | ✔      |
| [PrettyNoEscapes](formats/Pretty/PrettyNoEscapes.md)                                                     | ✗     | ✔      |
| [PrettyMonoBlock](formats/Pretty/PrettyMonoBlock.md)                                                     | ✗     | ✔      |
| [PrettyNoEscapesMonoBlock](formats/Pretty/PrettyNoEscapesMonoBlock.md)                                   | ✗     | ✔      |
| [PrettyCompact](formats/Pretty/PrettyCompact.md)                                                         | ✗     | ✔      |
| [PrettyCompactNoEscapes](formats/Pretty/PrettyCompactNoEscapes.md)                                       | ✗     | ✔      |
| [PrettyCompactMonoBlock](formats/Pretty/PrettyCompactMonoBlock.md)                                       | ✗     | ✔      |
| [PrettyCompactNoEscapesMonoBlock](formats/Pretty/PrettyCompactNoEscapesMonoBlock.md)                     | ✗     | ✔      |
| [PrettySpace](formats/Pretty/PrettySpace.md)                                                             | ✗     | ✔      |
| [PrettySpaceNoEscapes](formats/Pretty/PrettySpaceNoEscapes)                                              | ✗     | ✔      |
| [PrettySpaceMonoBlock](formats/Pretty/PrettySpaceMonoBlock.md)                                           | ✗     | ✔      |
| [PrettySpaceNoEscapesMonoBlock](formats/Pretty/PrettySpaceNoEscapesMonoBlock.md)                         | ✗     | ✔      |
| [Prometheus](formats/Prometheus.md)                                                                      | ✗     | ✔      |
| [Protobuf](formats/Protobuf/Protobuf.md)                                                                 | ✔     | ✔      |
| [ProtobufSingle](formats/Protobuf/ProtobufSingle.md)                                                     | ✔     | ✔      |
| [ProtobufList](formats/Protobuf/ProtobufList.md)								                            | ✔     | ✔      |
| [Avro](formats/Avro/Avro.md)                                                                             | ✔     | ✔      |
| [AvroConfluent](formats/Avro/AvroConfluent.md)                                                           | ✔     | ✗      |
| [Parquet](formats/Parquet/Parquet.md)                                                                    | ✔     | ✔      |
| [ParquetMetadata](formats/Parquet/ParquetMetadata.md)                                                    | ✔     | ✗      |
| [Arrow](formats/Arrow/ArrowStream.md)                                                                    | ✔     | ✔      |
| [ArrowStream](formats/Arrow/ArrowStream.md)                                                              | ✔     | ✔      |
| [ORC](formats/ORC.md)                                                                                    | ✔     | ✔      |
| [One](formats/One.md)                                                                                    | ✔     | ✗      |
| [Npy](formats/Npy.md)                                                                                    | ✔     | ✔      |
| [RowBinary](formats/RowBinary/RowBinary.md)                                                              | ✔     | ✔      |
| [RowBinaryWithNames](formats/RowBinary/RowBinaryWithNames.md)                                            | ✔     | ✔      |
| [RowBinaryWithNamesAndTypes](formats/RowBinary/RowBinaryWithNamesAndTypes.md)                            | ✔     | ✔      |
| [RowBinaryWithDefaults](formats/RowBinary/RowBinaryWithDefaults.md)                                      | ✔     | ✗      |
| [Native](formats/Native.md)                                                                              | ✔     | ✔      |
| [Null](formats/Null.md)                                                                                  | ✗     | ✔      |
| [XML](formats/XML.md)                                                                                    | ✗     | ✔      |
| [CapnProto](formats/CapnProto.md)                                                                        | ✔     | ✔      |
| [LineAsString](formats/LineAsString/LineAsString.md)                                                     | ✔     | ✔      |
| [LineAsStringWithNames](formats/LineAsString/LineAsStringWithNames.md)                                   | ✗     | ✔      |
| [LineAsStringWithNamesAndTypes](formats/LineAsString/LineAsStringWithNamesAndTypes.md)                   | ✗     | ✔      |
| [Regexp](formats/Regexp.md)                                                                              | ✔     | ✗      |
| [RawBLOB](formats/RawBLOB.md)                                                                            | ✔     | ✔      |
| [MsgPack](formats/MsgPack.md)                                                                            | ✔     | ✔      |
| [MySQLDump](formats/MySQLDump.md)                                                                        | ✔     | ✗      |
| [Dwarf](formats/DWARF.md)                                                                                | ✔     | ✗      |
| [Markdown](formats/Markdown.md)                                                                          | ✗     | ✔      |
| [Form](formats/Form.md)                                                                                  | ✔     | ✗      |
| [SQLInsert](formats/SQLInsert.md)                                                                        | ✗     | ✔      |

You can control some format processing parameters with the ClickHouse settings. For more information read the [Settings](../operations/settings/settings-formats.md) section.

See [JSON Format Settings](formats/JSON/format-settings.md) for an overview of all settings relevant to JSON.

