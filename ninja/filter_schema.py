from typing import Any, TypeVar, cast

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Q, QuerySet
from pydantic.fields import FieldInfo
from typing_extensions import Literal

from .schema import Schema

DEFAULT_IGNORE_NONE = True
DEFAULT_CLASS_LEVEL_EXPRESSION_CONNECTOR = "AND"
DEFAULT_FIELD_LEVEL_EXPRESSION_CONNECTOR = "OR"

# XOR is available only in Django 4.1+: https://docs.djangoproject.com/en/4.1/ref/models/querysets/#xor
ExpressionConnector = Literal["AND", "OR", "XOR"]


# class FilterConfig(BaseConfig):
#     ignore_none: bool = DEFAULT_IGNORE_NONE
#     expression_connector: ExpressionConnector = cast(
#         ExpressionConnector, DEFAULT_CLASS_LEVEL_EXPRESSION_CONNECTOR
#     )


T = TypeVar("T", bound=QuerySet)


class FilterSchema(Schema):
    # if TYPE_CHECKING:
    #     __config__: ClassVar[Type[FilterConfig]] = FilterConfig  # pragma: no cover

    # Config = FilterConfig

    class Config(Schema.Config):
        ignore_none: bool = DEFAULT_IGNORE_NONE
        expression_connector: ExpressionConnector = cast(
            ExpressionConnector, DEFAULT_CLASS_LEVEL_EXPRESSION_CONNECTOR
        )

    def custom_expression(self) -> Q:
        """
        Implement this method to return a combination of filters that will be used
        """
        raise NotImplementedError

    def get_filter_expression(self) -> Q:
        """
        Returns a Q expression based on the current filters
        """
        pass

    def filter(self, queryset: T) -> T:
        pass

    def _resolve_field_expression(
        self, field_name: str, field_value: Any, field: FieldInfo
    ) -> Q:
        pass

    def _connect_fields(self) -> Q:
        pass
