## Install

Start by installing Recap. Python 3.9 or above is required.

    pip install recap-core

## Crawl

Now let's crawl a database:

    recap refresh postgresql://username@localhost/some_db

You can use any [SQLAlchemy](https://docs.sqlalchemy.org/en/14/dialects/) connect string.

    recap refresh bigquery://some-project-12345
    recap refresh snowflake://some_user:some_pass@some_account_id

For Snowflake and BigQuery, you'll have to `pip install snowflake-sqlalchemy` or `pip install sqlalchemy-bigquery`, respectively.

## List

Crawled metadata is stored in a directory structure. See what's available using:

    recap list /

Recap will respond with a JSON list:

```json
[
  "databases"
]
```

Append children to the path to browse around:

    recap list /databases

## Read

After you poke around, try and read some metadata. Every node in the path can have metadata, but right now only tables and views do. You can look at metadata using the `recap read` command:

    recap read /databases/postgresql/instances/localhost/schemas/some_db/tables/some_table

Recap will print all of `some_table`'s metadata to the CLI in JSON format:

```json
{
  "access": {
    "username": {
      "privileges": [
        "INSERT",
        "SELECT",
        "UPDATE",
        "DELETE",
        "TRUNCATE",
        "REFERENCES",
        "TRIGGER"
      ],
      "read": true,
      "write": true
    }
  },
  "columns": {
    "email": {
      "autoincrement": false,
      "default": null,
      "generic_type": "VARCHAR",
      "nullable": false,
      "type": "VARCHAR"
    },
    "id": {
      "autoincrement": true,
      "default": "nextval('\"some_db\".some_table_id_seq'::regclass)",
      "generic_type": "BIGINT",
      "nullable": false,
      "type": "BIGINT"
    }
  },
  "data_profile": {
    "email": {
      "count": 10,
      "distinct": 10,
      "empty_strings": 0,
      "max_length": 32,
      "min_length": 13,
      "nulls": 0
    },
    "id": {
      "average": 5.5,
      "count": 10,
      "max": 10,
      "min": 1,
      "negatives": 0,
      "nulls": 0,
      "sum": 55.0,
      "zeros": 0
    }
  },
  "indexes": {
    "index_some_table_on_email": {
      "columns": [
        "email"
      ],
      "unique": false
    }
  },
  "location": {
    "database": "postgresql",
    "instance": "localhost",
    "schema": "some_db",
    "table": "some_table"
  },
  "primary_key": {
    "constrained_columns": [
      "id"
    ],
    "name": "some_table_pkey"
  }
}
```

## Search

You can search for metadata, too. Recap stores its metadata in [DuckDB](https://duckdb.org) by default, so you can use DuckDB's [JSON path syntax](https://duckdb.org/docs/extensions/json) to search the catalog:

    recap search "metadata->'$.location'->>'$.table' = 'some_table'"

The database file defaults to `~/.recap/catalog/recap.duckdb`, if you wish to open a DuckDB client directly.
