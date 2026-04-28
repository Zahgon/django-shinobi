import datetime
from decimal import Decimal
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Tuple,
    Type,
    TypeVar,
    Union,
    cast,
    no_type_check,
)
from uuid import UUID

from django.db.models import ManyToManyField
from django.db.models.fields import Field as DjangoField
from pydantic import BaseModel, IPvAnyAddress
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined, core_schema
from typing_extensions import Literal

from ninja.enum import NinjaChoicesList
from ninja.errors import ConfigError
from ninja.files import FileFieldType
from ninja.openapi.schema import OpenAPISchema
from ninja.types import DictStrAny

__all__ = ["create_m2m_link_type", "get_schema_field", "get_related_field_schema"]


# keep_lazy seems not needed as .title forces translation anyway
# https://github.com/vitalik/django-ninja/issues/774
# @keep_lazy_text
def title_if_lower(s: str) -> str:
    pass


class AnyObject:
    @classmethod
    def __get_pydantic_core_schema__(
        cls, source: Any, handler: Callable[..., Any]
    ) -> Any:
        return core_schema.with_info_plain_validator_function(cls.validate)

    @classmethod
    def __get_pydantic_json_schema__(
        cls, schema: Any, handler: Callable[..., Any]
    ) -> DictStrAny:
        return {"type": "object"}

    @classmethod
    def validate(cls, value: Any, _: Any) -> Any:
        pass


TYPES = {
    "AutoField": int,
    "BigAutoField": int,
    "BigIntegerField": int,
    "BinaryField": bytes,
    "BooleanField": bool,
    "CharField": str,
    "DateField": datetime.date,
    "DateTimeField": datetime.datetime,
    "DecimalField": Decimal,
    "DurationField": datetime.timedelta,
    "FileField": FileFieldType,
    "FilePathField": str,
    "FloatField": float,
    "GenericIPAddressField": IPvAnyAddress,
    "IPAddressField": IPvAnyAddress,
    "IntegerField": int,
    "ImageField": FileFieldType,
    "JSONField": AnyObject,
    "NullBooleanField": bool,
    "PositiveBigIntegerField": int,
    "PositiveIntegerField": int,
    "PositiveSmallIntegerField": int,
    "SlugField": str,
    "SmallAutoField": int,
    "SmallIntegerField": int,
    "TextField": str,
    "TimeField": datetime.time,
    "UUIDField": UUID,
    # postgres fields:
    "ArrayField": List,
    "CICharField": str,
    "CIEmailField": str,
    "CITextField": str,
    "HStoreField": Dict,
}

TModel = TypeVar("TModel")


def register_field(django_field: str, python_type: Any) -> None:
    pass


@no_type_check
def create_m2m_link_type(type_: Type[TModel]) -> Type[TModel]:
    pass


@no_type_check
def get_schema_field(
    field: DjangoField, *, depth: int = 0, optional: bool = False
) -> Tuple[str, Type, FieldInfo]:
    "Returns pydantic field from django's model field"
    pass


@no_type_check
def get_related_field_schema(
    field: DjangoField, *, depth: int
) -> Tuple[OpenAPISchema, FieldInfo]:
    pass


def get_field_property_accessors(field: DjangoField) -> property:
    pass
