from sqlalchemy import types
from recap.metadata import Field, Schema, Type
from typing import Any


def to_recap_schema(columns: list[dict[str, Any]]) -> Schema:
    fields = []
    for column in columns:
        match column["type"]:
            case types.SmallInteger():
                type_ = Type.INT16
            case types.Integer():
                type_ = Type.INT32
            case types.BigInteger():
                type_ = Type.INT64
            case types.Boolean():
                type_ = Type.BOOLEAN
            case types.Float():
                type_ = Type.FLOAT32
            case types.LargeBinary() | types._Binary():
                type_ = Type.BYTES
            case types.Numeric():
                type_ = Type.FLOAT64
            case types.String() | types.Text() | types.Unicode() | types.UnicodeText():
                type_ = Type.STRING
            case _:
                raise ValueError(
                    "Can't convert to Recap type from frictionless "
                    f"type={type(column['type'])}"
                )
        fields.append(Field(
            name=column["name"],
            schema=Schema(
                type=type_,
                default=column["default"],
                optional=column["nullable"],
                doc=column.get("comment"),
            )
        ))
    return Schema(type=Type.STRUCT, fields=fields)
