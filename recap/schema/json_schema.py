from typing import Any

from recap import metadata

DOLLAR_SCHEMA = "https://json-schema.org/draft/2020-12/schema"


def from_json_schema(json_schema: dict[str, Any]) -> metadata.Schema:
    match json_schema.get("type"):
        case "integer":
            return metadata.Int64Schema(
                name=json_schema.get("title"),
                default=json_schema.get("default"),
                doc=json_schema.get("description"),
            )
        case "string" if json_schema.get("format") == "date-time":
            return metadata.TimestampSchema(
                name=json_schema.get("title"),
                default=json_schema.get("default"),
                doc=json_schema.get("description"),
            )
        case "string" if json_schema.get("format") == "date":
            return metadata.DateSchema(
                name=json_schema.get("title"),
                default=json_schema.get("default"),
                doc=json_schema.get("description"),
            )
        case "string" if json_schema.get("format") == "time":
            return metadata.TimeSchema(
                name=json_schema.get("title"),
                default=json_schema.get("default"),
                doc=json_schema.get("description"),
            )
        case "string":
            return metadata.StringSchema(
                name=json_schema.get("title"),
                default=json_schema.get("default"),
                doc=json_schema.get("description"),
            )
        case "number":
            return metadata.Float64Schema(
                name=json_schema.get("title"),
                default=json_schema.get("default"),
                doc=json_schema.get("description"),
            )
        case "boolean":
            return metadata.BooleanSchema(
                name=json_schema.get("title"),
                default=json_schema.get("default"),
                doc=json_schema.get("description"),
            )
        case "object":
            fields = []
            properties = json_schema.get("properties", {})
            required = set(json_schema.get("required", []))
            for name, field_schema in properties.items():
                schema = from_json_schema(field_schema)
                schema.optional = (name in required)
                fields.append(
                    metadata.Field(
                        name=name,
                        schema=schema,
                    )
                )
            return metadata.StructSchema(
                name=json_schema.get("title"),
                default=json_schema.get("default"),
                doc=json_schema.get("description"),
                fields=fields,
            )
        case "array":
            schema = from_json_schema(json_schema.get("items", {}))
            return metadata.ArraySchema(
                name=json_schema.get("title"),
                default=json_schema.get("default"),
                doc=json_schema.get("description"),
                value_schema=schema,
            )
        case _:
            raise ValueError(
                "Can't convert to Recap type from JSON schema "
                f"type={json_schema.get('type')}"
            )


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
            required = []
            json_schema |= {
                "$schema": DOLLAR_SCHEMA,
                "type": "object",
                "properties": properties,
                "required": required,
            }
            for field in schema.fields or []:
                properties[field.name] = to_json_schema(field.schema_)
                if not field.schema_.optional:
                    required.append(field.name)
        case _:
            raise ValueError(
                "Can't convert from Recap type to JSON schema schema={schema}"
            )
    return json_schema
