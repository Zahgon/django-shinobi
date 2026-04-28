from abc import ABC, abstractmethod
from collections import defaultdict
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Optional,
    Pattern,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from django.conf import settings
from django.http import HttpRequest
from pydantic import BaseModel
from pydantic.fields import FieldInfo

from ninja.errors import HttpError
from ninja.types import DictStrAny

if TYPE_CHECKING:
    from ninja import NinjaAPI  # pragma: no cover

__all__ = [
    "ParamModel",
    "QueryModel",
    "PathModel",
    "HeaderModel",
    "CookieModel",
    "BodyModel",
    "FormModel",
    "FileModel",
]

TModel = TypeVar("TModel", bound="ParamModel")
TModels = List[TModel]


def NestedDict() -> DictStrAny:
    pass


class ParamModel(BaseModel, ABC):
    __ninja_param_source__ = None

    @classmethod
    @abstractmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        pass  # pragma: no cover

    @classmethod
    def resolve(
        cls: Type[TModel],
        request: HttpRequest,
        api: "NinjaAPI",
        path_params: DictStrAny,
    ) -> TModel:
        data = cls.get_request_data(request, api, path_params)
        if data is None:
            return cls()

        data = cls._map_data_paths(data)
        return cls.model_validate(data, context={"request": request})

    @classmethod
    def _map_data_paths(cls, data: DictStrAny) -> DictStrAny:
        pass

    @classmethod
    def _map_data_path(cls, data: DictStrAny, value: Any, path: Tuple) -> None:
        pass


class QueryModel(ParamModel):
    @classmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        pass


class PathModel(ParamModel):
    @classmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        pass


class HeaderModel(ParamModel):
    __ninja_flatten_map__: DictStrAny

    @classmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        pass


class CookieModel(ParamModel):
    @classmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        pass


class BodyModel(ParamModel):
    __read_from_single_attr__: str

    @classmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        pass


class FormModel(ParamModel):
    @classmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        pass


class FileModel(ParamModel):
    @classmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        pass


class _HttpRequest(HttpRequest):
    body: bytes = b""


class _MultiPartBodyModel(BodyModel):
    __ninja_body_params__: DictStrAny

    @classmethod
    def get_request_data(
        cls, request: HttpRequest, api: "NinjaAPI", path_params: DictStrAny
    ) -> Optional[DictStrAny]:
        pass


class Param(FieldInfo):  # type: ignore[misc]
    def __init__(
        self,
        default: Any,
        *,
        alias: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        gt: Optional[float] = None,
        ge: Optional[float] = None,
        lt: Optional[float] = None,
        le: Optional[float] = None,
        min_length: Optional[int] = None,
        max_length: Optional[int] = None,
        example: Optional[Any] = None,
        examples: Optional[Dict[str, Any]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: Optional[bool] = True,
        pattern: Union[str, Pattern[str], None] = None,
        # param_name: str = None,
        # param_type: Any = None,
        **extra: Any,
    ):
        self.deprecated = deprecated
        # self.param_name: str = None
        # self.param_type: Any = None
        self.model_field: Optional[FieldInfo] = None
        json_schema_extra = {}
        if example:
            json_schema_extra["example"] = example
        if examples:
            json_schema_extra["examples"] = examples
        if deprecated:
            json_schema_extra["deprecated"] = deprecated
        if not include_in_schema:
            json_schema_extra["include_in_schema"] = include_in_schema
        if alias and not extra.get("validation_alias"):
            extra["validation_alias"] = alias
        if alias and not extra.get("serialization_alias"):
            extra["serialization_alias"] = alias

        super().__init__(
            default=default,
            alias=alias,
            title=title,
            description=description,
            gt=gt,
            ge=ge,
            lt=lt,
            le=le,
            min_length=min_length,
            max_length=max_length,
            pattern=pattern,
            json_schema_extra=json_schema_extra,
            **extra,
        )

    @classmethod
    def _param_source(cls) -> str:
        "Openapi param.in value or body type"
        pass


class Path(Param):  # type: ignore[misc]
    _model = PathModel


class Query(Param):  # type: ignore[misc]
    _model = QueryModel


class Header(Param):  # type: ignore[misc]
    _model = HeaderModel


class Cookie(Param):  # type: ignore[misc]
    _model = CookieModel


class Body(Param):  # type: ignore[misc]
    _model = BodyModel


class Form(Param):  # type: ignore[misc]
    _model = FormModel


class File(Param):  # type: ignore[misc]
    _model = FileModel


class _MultiPartBody(Param):  # type: ignore[misc]
    _model = _MultiPartBodyModel

    @classmethod
    def _param_source(cls) -> str:
        pass
