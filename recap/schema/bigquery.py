from google.cloud.bigquery import SchemaField
from recap.metadata import Field, Schema, Type


def to_recap_schema(columns: list[SchemaField]) -> Schema:
    fields = []
    for column in columns:
        match column.field_type:
            case "STRING":
                type_ = Type.STRING
            case "BYTES":
                type_ = Type.BYTES
            case "INTEGER" | "INT64":
                type_ = Type.INT64
            case "FLOAT" | "FLOAT64":
                type_ = Type.FLOAT64
            case "BOOLEAN" | "BOOL":
                type_ = Type.BOOLEAN
            case _:
                raise ValueError(
                    "Can't convert to Recap type from bigquery "
                    f"type={column.field_type}"
                )
        fields.append(Field(
            name=column.name,
            schema=Schema(
                type=type_,
                default=column.default_value_expression,
                optional=column.is_nullable,
                doc=column.description,
            )
        ))
    return Schema(type=Type.STRUCT, fields=fields)
