from frictionless.schema import Schema as FrictionlessSchema
from recap.metadata import Field, Schema, Type


def to_recap_schema(frictionless_schema: FrictionlessSchema) -> Schema:
    fields = []
    for frictionless_field in frictionless_schema.fields:
        match frictionless_field.type:
            case "string":
                type_ = Type.STRING
            case "number":
                type_ = Type.FLOAT64
            case "integer":
                type_ = Type.INT64
            case "boolean":
                type_ = Type.BOOLEAN
            # TODO Should handle types (object, array) here.
            case _:
                raise ValueError(
                    "Can't convert to Recap type from frictionless "
                    f"type={frictionless_field.type}"
                )
        fields.append(
            Field(
                name=frictionless_field.name,
                schema=Schema(
                    type=type_,
                    doc=frictionless_field.description,
                ),
            )
        )
    return Schema(
        type=Type.STRUCT,
        fields=fields,
    )
