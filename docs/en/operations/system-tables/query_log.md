---
description: 'System table containing information about executed queries, for example,
  start time, duration of processing, error messages.'
keywords: ['system table', 'query_log']
slug: /operations/system-tables/query_log
title: 'system.query_log'
---

import SystemTableCloud from '@site/docs/_snippets/_system_table_cloud.md';

# system.query_log

<SystemTableCloud/>

## Overview {#overview}

Contains information about executed queries, for example, start time, duration of processing, error messages.

:::note
This table does not contain the ingested data for `INSERT` queries.
:::

You can change settings of queries logging in the [query_log](../../operations/server-configuration-parameters/settings.md#query_log) section of the server configuration.

You can disable queries logging by setting [log_queries = 0](/operations/settings/settings#log_queries). We do not recommend to turn off logging because information in this table is important for solving issues.

The flushing period of data is set in `flush_interval_milliseconds` parameter of the [query_log](../../operations/server-configuration-parameters/settings.md#query_log) server settings section. To force flushing, use the [SYSTEM FLUSH LOGS](/sql-reference/statements/system#flush-logs) query.

ClickHouse does not delete data from the table automatically. See [Introduction](/operations/system-tables/overview#system-tables-introduction) for more details.

The `system.query_log` table registers two kinds of queries:

1.  Initial queries that were run directly by the client.
2.  Child queries that were initiated by other queries (for distributed query execution). For these types of queries, information about the parent queries is shown in the `initial_*` columns.

Each query creates one or two rows in the `query_log` table, depending on the status (see the `type` column) of the query:

1.  If the query execution was successful, two rows with the `QueryStart` and `QueryFinish` types are created.
2.  If an error occurred during query processing, two events with the `QueryStart` and `ExceptionWhileProcessing` types are created.
3.  If an error occurred before launching the query, a single event with the `ExceptionBeforeStart` type is created.

You can use the [log_queries_probability](/operations/settings/settings#log_queries_probability)) setting to reduce the number of queries, registered in the `query_log` table.

You can use the [log_formatted_queries](/operations/settings/settings#log_formatted_queries)) setting to log formatted queries to the `formatted_query` column.

## Columns {#columns}

<table>
  <thead>
    <tr>
      <th>Column</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>hostname</code></td>
      <td>Hostname of the server executing the query.</td>
    </tr>
    <tr>
      <td><code>type</code></td>
      <td>
        Type of an event that occurred when executing the query. Values:
        <ul>
          <li><code>'QueryStart' = 1</code> — Successful start of query execution.</li>
          <li><code>'QueryFinish' = 2</code> — Successful end of query execution.</li>
          <li><code>'ExceptionBeforeStart' = 3</code> — Exception before the start of query execution.</li>
          <li><code>'ExceptionWhileProcessing' = 4</code> — Exception during the query execution.</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td><code>event_date</code></td>
      <td>Query starting date.</td>
    </tr>
    <tr>
      <td><code>event_time</code></td>
      <td>Query starting time.</td>
    </tr>
    <tr>
      <td><code>event_time_microseconds</code></td>
      <td>Query starting time with microseconds precision.</td>
    </tr>
    <tr>
      <td><code>query_start_time</code></td>
      <td>Start time of query execution.</td>
    </tr>
    <tr>
      <td><code>query_start_time_microseconds</code></td>
      <td>Start time of query execution with microsecond precision.</td>
    </tr>
    <tr>
      <td><code>query_duration_ms</code></td>
      <td>Duration of query execution in milliseconds.</td>
    </tr>
    <tr>
      <td><code>read_rows</code></td>
      <td>Total number of rows read from all tables and table functions participated in query. It includes usual subqueries, subqueries for <code>IN</code> and <code>JOIN</code>. For distributed queries <code>read_rows</code> includes the total number of rows read at all replicas. Each replica sends its <code>read_rows</code> value, and the server-initiator of the query summarizes all received and local values. The cache volumes do not affect this value.</td>
    </tr>
    <tr>
      <td><code>read_bytes</code></td>
      <td>Total number of bytes read from all tables and table functions participated in query. It includes usual subqueries, subqueries for <code>IN</code> and <code>JOIN</code>. For distributed queries <code>read_bytes</code> includes the total number of rows read at all replicas. Each replica sends its <code>read_bytes</code> value, and the server-initiator of the query summarizes all received and local values. The cache volumes do not affect this value.</td>
    </tr>
    <tr>
      <td><code>written_rows</code></td>
      <td>For <code>INSERT</code> queries, the number of written rows. For other queries, the column value is 0.</td>
    </tr>
    <tr>
      <td><code>written_bytes</code></td>
      <td>For <code>INSERT</code> queries, the number of written bytes (uncompressed). For other queries, the column value is 0.</td>
    </tr>
    <tr>
      <td><code>result_rows</code></td>
      <td>Number of rows in a result of the <code>SELECT</code> query, or a number of rows in the <code>INSERT</code> query.</td>
    </tr>
    <tr>
      <td><code>result_bytes</code></td>
      <td>RAM volume in bytes used to store a query result.</td>
    </tr>
    <tr>
      <td><code>memory_usage</code></td>
      <td>Memory consumption by the query.</td>
    </tr>
    <tr>
      <td><code>current_database</code></td>
      <td>Name of the current database.</td>
    </tr>
    <tr>
      <td><code>query</code></td>
      <td>Query string.</td>
    </tr>
    <tr>
      <td><code>formatted_query</code></td>
      <td>Formatted query string.</td>
    </tr>
    <tr>
      <td><code>normalized_query_hash</code></td>
      <td>A numeric hash value, such as it is identical for queries differ only by values of literals.</td>
    </tr>
    <tr>
      <td><code>query_kind</code></td>
      <td>Type of the query.</td>
    </tr>
    <tr>
      <td><code>databases</code></td>
      <td>Names of the databases present in the query.</td>
    </tr>
    <tr>
      <td><code>tables</code></td>
      <td>Names of the tables present in the query.</td>
    </tr>
    <tr>
      <td><code>columns</code></td>
      <td>Names of the columns present in the query.</td>
    </tr>
    <tr>
      <td><code>partitions</code></td>
      <td>Names of the partitions present in the query.</td>
    </tr>
    <tr>
      <td><code>projections</code></td>
      <td>Names of the projections used during the query execution.</td>
    </tr>
    <tr>
      <td><code>views</code></td>
      <td>Names of the (materialized or live) views present in the query.</td>
    </tr>
    <tr>
      <td><code>exception_code</code></td>
      <td>Code of an exception.</td>
    </tr>
    <tr>
      <td><code>exception</code></td>
      <td>Exception message.</td>
    </tr>
    <tr>
      <td><code>stack_trace</code></td>
      <td>Stack trace. An empty string, if the query was completed successfully.</td>
    </tr>
    <tr>
      <td><code>is_initial_query</code></td>
      <td>
        Query type. Possible values:
        <ul>
          <li>1 — Query was initiated by the client.</li>
          <li>0 — Query was initiated by another query as part of distributed query execution.</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td><code>user</code></td>
      <td>Name of the user who initiated the current query.</td>
    </tr>
    <tr>
      <td><code>query_id</code></td>
      <td>ID of the query.</td>
    </tr>
    <tr>
      <td><code>address</code></td>
      <td>IP address that was used to make the query.</td>
    </tr>
    <tr>
      <td><code>port</code></td>
      <td>The client port that was used to make the query.</td>
    </tr>
    <tr>
      <td><code>initial_user</code></td>
      <td>Name of the user who ran the initial query (for distributed query execution).</td>
    </tr>
    <tr>
      <td><code>initial_query_id</code></td>
      <td>ID of the initial query (for distributed query execution).</td>
    </tr>
    <tr>
      <td><code>initial_address</code></td>
      <td>IP address that the parent query was launched from.</td>
    </tr>
    <tr>
      <td><code>initial_port</code></td>
      <td>The client port that was used to make the parent query.</td>
    </tr>
    <tr>
      <td><code>initial_query_start_time</code></td>
      <td>Initial query starting time (for distributed query execution).</td>
    </tr>
    <tr>
      <td><code>initial_query_start_time_microseconds</code></td>
      <td>Initial query starting time with microseconds precision (for distributed query execution).</td>
    </tr>
    <tr>
      <td><code>interface</code></td>
      <td>
        Interface that the query was initiated from. Possible values:
        <ul>
          <li>1 — TCP.</li>
          <li>2 — HTTP.</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td><code>os_user</code></td>
      <td>Operating system username who runs clickhouse-client.</td>
    </tr>
    <tr>
      <td><code>client_hostname</code></td>
      <td>Hostname of the client machine where the clickhouse-client or another TCP client is run.</td>
    </tr>
    <tr>
      <td><code>client_name</code></td>
      <td>The clickhouse-client or another TCP client name.</td>
    </tr>
    <tr>
      <td><code>client_revision</code></td>
      <td>Revision of the clickhouse-client or another TCP client.</td>
    </tr>
    <tr>
      <td><code>client_version_major</code></td>
      <td>Major version of the clickhouse-client or another TCP client.</td>
    </tr>
    <tr>
      <td><code>client_version_minor</code></td>
      <td>Minor version of the clickhouse-client or another TCP client.</td>
    </tr>
    <tr>
      <td><code>client_version_patch</code></td>
      <td>Patch component of the clickhouse-client or another TCP client version.</td>
    </tr>
    <tr>
      <td><code>script_query_number</code></td>
      <td>The query number in a script with multiple queries for clickhouse-client.</td>
    </tr>
    <tr>
      <td><code>script_line_number</code></td>
      <td>The line number of the query start in a script with multiple queries for clickhouse-client.</td>
    </tr>
    <tr>
      <td><code>http_method</code></td>
      <td>
        HTTP method that initiated the query. Possible values:
        <ul>
          <li>0 — The query was launched from the TCP interface.</li>
          <li>1 — <code>GET</code> method was used.</li>
          <li>2 — <code>POST</code> method was used.</li>
        </ul>
      </td>
    </tr>
    <tr>
      <td><code>http_user_agent</code></td>
      <td>HTTP header <code>UserAgent</code> passed in the HTTP query.</td>
    </tr>
    <tr>
      <td><code>http_referer</code></td>
      <td>HTTP header <code>Referer</code> passed in the HTTP query (contains an absolute or partial address of the page making the query).</td>
    </tr>
    <tr>
      <td><code>forwarded_for</code></td>
      <td>HTTP header <code>X-Forwarded-For</code> passed in the HTTP query.</td>
    </tr>
    <tr>
      <td><code>quota_key</code></td>
      <td>The <code>quota key</code> specified in the quotas setting (see <code>keyed</code>).</td>
    </tr>
    <tr>
      <td><code>revision</code></td>
      <td>ClickHouse revision.</td>
    </tr>
    <tr>
      <td><code>ProfileEvents</code></td>
      <td>ProfileEvents that measure different metrics. The description of them could be found in the table <code>system.events</code>.</td>
    </tr>
    <tr>
      <td><code>Settings</code></td>
      <td>Settings that were changed when the client ran the query. To enable logging changes to settings, set the <code>log_query_settings</code> parameter to 1.</td>
    </tr>
    <tr>
      <td><code>log_comment</code></td>
      <td>Log comment. It can be set to arbitrary string no longer than <code>max_query_size</code>. An empty string if it is not defined.</td>
    </tr>
    <tr>
      <td><code>thread_ids</code></td>
      <td>Thread ids that are participating in query execution. These threads may not have run simultaneously.</td>
    </tr>
    <tr>
      <td><code>peak_threads_usage</code></td>
      <td>Maximum count of simultaneous threads executing the query.</td>
    </tr>
    <tr>
      <td><code>used_aggregate_functions</code></td>
      <td>Canonical names of <code>aggregate functions</code>, which were used during query execution.</td>
    </tr>
    <tr>
      <td><code>used_aggregate_function_combinators</code></td>
      <td>Canonical names of <code>aggregate functions combinators</code>, which were used during query execution.</td>
    </tr>
    <tr>
      <td><code>used_database_engines</code></td>
      <td>Canonical names of <code>database engines</code>, which were used during query execution.</td>
    </tr>
    <tr>
      <td><code>used_data_type_families</code></td>
      <td>Canonical names of <code>data type families</code>, which were used during query execution.</td>
    </tr>
    <tr>
      <td><code>used_dictionaries</code></td>
      <td>Canonical names of <code>dictionaries</code>, which were used during query execution. For dictionaries configured using an XML file this is the name of the dictionary, and for dictionaries created by an SQL statement, the canonical name is the fully qualified object name.</td>
    </tr>
    <tr>
      <td><code>used_formats</code></td>
      <td>Canonical names of <code>formats</code>, which were used during query execution.</td>
    </tr>
    <tr>
      <td><code>used_functions</code></td>
      <td>Canonical names of <code>functions</code>, which were used during query execution.</td>
    </tr>
    <tr>
      <td><code>used_storages</code></td>
      <td>Canonical names of <code>storages</code>, which were used during query execution.</td>
    </tr>
    <tr>
      <td><code>used_table_functions</code></td>
      <td>Canonical names of <code>table functions</code>, which were used during query execution.</td>
    </tr>
    <tr>
      <td><code>used_privileges</code></td>
      <td>Privileges which were successfully checked during query execution.</td>
    </tr>
    <tr>
      <td><code>missing_privileges</code></td>
      <td>Privileges that are missing during query execution.</td>
    </tr>
    <tr>
      <td><code>query_cache_usage</code></td>
      <td>
        Usage of the query cache during query execution. Values:
        <ul>
          <li><code>'Unknown'</code> = Status unknown.</li>
          <li><code>'None'</code> = The query result was neither written into nor read from the query cache.</li>
          <li><code>'Write'</code> = The query result was written into the query cache.</li>
          <li><code>'Read'</code> = The query result was read from the query cache.</li>
        </ul>
      </td>
    </tr>
  </tbody>
</table>

## Example {#example}

```sql
SELECT * FROM system.query_log WHERE type = 'QueryFinish' ORDER BY query_start_time DESC LIMIT 1 FORMAT Vertical;
```

```text
Row 1:
──────
hostname:                              clickhouse.eu-central1.internal
type:                                  QueryFinish
event_date:                            2021-11-03
event_time:                            2021-11-03 16:13:54
event_time_microseconds:               2021-11-03 16:13:54.953024
query_start_time:                      2021-11-03 16:13:54
query_start_time_microseconds:         2021-11-03 16:13:54.952325
query_duration_ms:                     0
read_rows:                             69
read_bytes:                            6187
written_rows:                          0
written_bytes:                         0
result_rows:                           69
result_bytes:                          48256
memory_usage:                          0
current_database:                      default
query:                                 DESCRIBE TABLE system.query_log
formatted_query:
normalized_query_hash:                 8274064835331539124
query_kind:
databases:                             []
tables:                                []
columns:                               []
projections:                           []
views:                                 []
exception_code:                        0
exception:
stack_trace:
is_initial_query:                      1
user:                                  default
query_id:                              7c28bbbb-753b-4eba-98b1-efcbe2b9bdf6
address:                               ::ffff:127.0.0.1
port:                                  40452
initial_user:                          default
initial_query_id:                      7c28bbbb-753b-4eba-98b1-efcbe2b9bdf6
initial_address:                       ::ffff:127.0.0.1
initial_port:                          40452
initial_query_start_time:              2021-11-03 16:13:54
initial_query_start_time_microseconds: 2021-11-03 16:13:54.952325
interface:                             1
os_user:                               sevirov
client_hostname:                       clickhouse.eu-central1.internal
client_name:                           ClickHouse
client_revision:                       54449
client_version_major:                  21
client_version_minor:                  10
client_version_patch:                  1
http_method:                           0
http_user_agent:
http_referer:
forwarded_for:
quota_key:
revision:                              54456
log_comment:
thread_ids:                            [30776,31174]
ProfileEvents:                         {'Query':1,'NetworkSendElapsedMicroseconds':59,'NetworkSendBytes':2643,'SelectedRows':69,'SelectedBytes':6187,'ContextLock':9,'RWLockAcquiredReadLocks':1,'RealTimeMicroseconds':817,'UserTimeMicroseconds':427,'SystemTimeMicroseconds':212,'OSCPUVirtualTimeMicroseconds':639,'OSReadChars':894,'OSWriteChars':319}
Settings:                              {'load_balancing':'random','max_memory_usage':'10000000000'}
used_aggregate_functions:              []
used_aggregate_function_combinators:   []
used_database_engines:                 []
used_data_type_families:               []
used_dictionaries:                     []
used_formats:                          []
used_functions:                        []
used_storages:                         []
used_table_functions:                  []
used_privileges:                       []
missing_privileges:                    []
query_cache_usage:                     None
```

## Related content {#related-content}

- [`system.query_thread_log`](/operations/system-tables/query_thread_log) — This table contains information about each query execution thread.
