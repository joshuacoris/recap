"""
This module contains the core metadata models that Recap understands. All
models extend Pydantic's `BaseModel` class.

Right now, Recap's only metadata model is a Schema. Other entities, such as
accounts and jobs, are represented by URLs, but have no associated metadata.
"""

from __future__ import annotations

from pydantic import BaseModel, Field as PydanticField

from enum import Enum

from typing import Any


class Field(BaseModel):
    schema_: Schema = PydanticField(alias="schema")
    """
    A field's schema
    """

    name: str | None = None
    """
    A field's name.
    """


class Schema(BaseModel):
    """
    Recap's representation of a Schema.
    """

    type_: Type = PydanticField(alias="type")
    """
    The schema's type.
    """

    default: Any = None
    """
    :returns: Default value for the schema.
    """

    name: str | None = None
    """
    The schema's name.
    """

    optional: bool = True
    """
    :returns: True if the schema is optional.
    """

    version: int | None = None
    """
    Optional schema version. Newer versions must be larger than older versions.
    """

    doc: str | None = None
    """
    A schema's documentation.
    """

    parameters: dict[str, str] | None = None
    """
    A map of optional schema parameters.
    """

    key_schema: Schema | None = None
    """
    Key schema for this map schema. Throws a ValueError if schema is not a map.
    """

    value_schema: Schema | None = None
    """
    Value schema for this map or array schema. Throws a ValueError if schema is
    not a map or array.
    """

    fields: list[Field] | None = None
    """
    List of Fields for this Schema. Throws a ValueError if schema is not a
    Type.STRUCT.
    """

    def field(self, name: str) -> Field | None:
        if self.type_ == Type.STRUCT:
            for field in self.fields or []:
                if field.name == name:
                    return field
        raise ValueError(
            "`field` only supported for STRUCT schemas, but type={self.type}"
        )

    def __str__(self) -> str:
        return self.json(
            by_alias=True,
            exclude_defaults=True,
            exclude_none=True,
            exclude_unset=True,
            indent=2,
        )


class Type(str, Enum):
    INT8 = 'INT8'
    INT16 = 'INT16'
    INT32 = 'INT32'
    INT64 = 'INT64'
    FLOAT32 = 'FLOAT32'
    FLOAT64 = 'FLOAT64'
    BOOLEAN = 'BOOLEAN'
    STRING = 'STRING'
    BYTES = 'BYTES'
    ARRAY = 'ARRAY'
    MAP = 'MAP'
    STRUCT = 'STRUCT'

    def is_primitive(self) -> bool:
        match self:
            case (
                Type.INT8
                | Type.INT16
                | Type.INT32
                | Type.INT64
                | Type.FLOAT32
                | Type.FLOAT64
                | Type.BOOLEAN
                | Type.STRING
                | Type.BYTES
            ):
                return True
        return False


# Update forward refs since Schema references Field, which references Schema.
Schema.update_forward_refs()
Field.update_forward_refs()
