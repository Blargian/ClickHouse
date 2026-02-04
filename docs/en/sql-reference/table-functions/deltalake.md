---
description: 'Provides a table-like interface to Delta Lake tables in Amazon S3, supporting both reads and writes.'
sidebar_label: 'deltaLake'
sidebar_position: 45
slug: /sql-reference/table-functions/deltalake
title: 'deltaLake'
doc_type: 'reference'
---

# deltaLake Table Function

Provides a table-like interface to [Delta Lake](https://github.com/delta-io/delta) tables in Amazon S3, Azure Blob Storage, or a locally mounted file system, supporting both reads and writes.

## Syntax {#syntax}

`deltaLake` is an alias of `deltaLakeS3`, its supported for compatibility.

```sql
deltaLake(url [,aws_access_key_id, aws_secret_access_key] [,format] [,structure] [,compression])

deltaLakeS3(url [,aws_access_key_id, aws_secret_access_key] [,format] [,structure] [,compression])

deltaLakeAzure(connection_string|storage_account_url, container_name, blobpath, [,account_name], [,account_key] [,format] [,compression_method])

deltaLakeLocal(path, [,format])
```

## Arguments {#arguments}

Description of the arguments coincides with description of arguments in table functions `s3`, `azureBlobStorage`, `HDFS` and `file` correspondingly.
`format` stands for the format of data files in the Delta lake table.

## Returned value {#returned_value}

A table with the specified structure for reading or writing data in the specified Delta Lake table.

## Writing data {#writing-data}

The `deltaLake` table function supports `INSERT` queries to write data to Delta Lake tables.

:::note
Writing to Delta Lake tables is an experimental feature. To enable it, set `allow_experimental_delta_lake_writes = 1`.
:::

**Example**

:::note[Compatibility note for MacOS]
If you're using a recent version but still getting an error `Received exception:
Code: 46. DB::Exception: Unknown table function deltaLake. (UNKNOWN_FUNCTION)` this is because builds on Mac don't include DeltaLake due to the usage of Rust.
:::

```sql
INSERT INTO TABLE FUNCTION deltaLake('https://example.s3.amazonaws.com/my-delta-table/', 'access_key', 'secret_key')
SELECT * FROM source_table;
```

For more details on write settings, see the [DeltaLake table engine documentation](../../../engines/table-engines/integrations/deltalake.md#write-settings).

## Examples {#examples}

Selecting rows from the table in S3 `https://clickhouse-public-datasets.s3.amazonaws.com/delta_lake/hits/`:

```sql
SELECT
    URL,
    UserAgent
FROM deltaLake('https://clickhouse-public-datasets.s3.amazonaws.com/delta_lake/hits/')
WHERE URL IS NOT NULL
LIMIT 2
```

```response
┌─URL───────────────────────────────────────────────────────────────────┬─UserAgent─┐
│ http://auto.ria.ua/search/index.kz/jobinmoscow/detail/55089/hasimages │         1 │
│ http://auto.ria.ua/search/index.kz/jobinmoscow.ru/gosushi             │         1 │
└───────────────────────────────────────────────────────────────────────┴───────────┘
```

## Virtual Columns {#virtual-columns}

- `_path` — Path to the file. Type: `LowCardinality(String)`.
- `_file` — Name of the file. Type: `LowCardinality(String)`.
- `_size` — Size of the file in bytes. Type: `Nullable(UInt64)`. If the file size is unknown, the value is `NULL`.
- `_time` — Last modified time of the file. Type: `Nullable(DateTime)`. If the time is unknown, the value is `NULL`.
- `_etag` — The etag of the file. Type: `LowCardinality(String)`. If the etag is unknown, the value is `NULL`.

## Related {#related}

- [DeltaLake engine](engines/table-engines/integrations/deltalake.md)
- [DeltaLake cluster table function](sql-reference/table-functions/deltalakeCluster.md)
