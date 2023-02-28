from typing import Any

from recap import metadata

DOLLAR_SCHEMA = "https://json-schema.org/draft/2020-12/schema"


def to_json_schema(schema: metadata.Schema) -> dict[str, Any]:
    json_schema = {
        "title": schema.name,
        "description": schema.doc,
    }
    match schema:
        case (
            metadata.Int8Schema()
            | metadata.Int16Schema()
            | metadata.Int32Schema()
            | metadata.Int64Schema()
        ):
            json_schema["type"] = "integer"
        case metadata.StringSchema():
            json_schema["type"] = "string"
        case (metadata.Float32Schema() | metadata.Float64Schema()):
            json_schema["type"] = "number"
        case metadata.BooleanSchema():
            json_schema["type"] = "boolean"
        case metadata.TimestampSchema():
            json_schema |= {
                "type": "string",
                "format": "date-time",
            }
        case metadata.DateSchema():
            json_schema |= {
                "type": "string",
                "format": "date",
            }
        case metadata.TimeSchema():
            json_schema |= {
                "type": "string",
                "format": "time",
            }
        case metadata.ArraySchema() if schema.value_schema:
            json_schema |= {
                "type": "array",
                "items": to_json_schema(schema.value_schema),
            }
        case metadata.StructSchema():
            properties = {}
            json_schema |= {
                "$schema": DOLLAR_SCHEMA,
                "type": "object",
                "properties": properties,
            }
            for field in schema.fields or []:
                properties[field.name] = to_json_schema(field.schema_)
        case _:
            raise ValueError(
                "Can't convert from Recap type to JSON schema schema={schema}"
            )
    return json_schema
