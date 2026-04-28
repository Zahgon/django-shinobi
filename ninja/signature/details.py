import inspect
import warnings
from collections import defaultdict, namedtuple
from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Generator,
    List,
    Optional,
    Tuple,
    Type,
)

import pydantic
from django.http import HttpResponse
from pydantic.fields import FieldInfo
from pydantic_core import PydanticUndefined
from typing_extensions import Annotated, _AnnotatedAlias, get_args, get_origin

from ninja import UploadedFile
from ninja.compatibility.util import UNION_TYPES
from ninja.errors import ConfigError
from ninja.params.models import (
    Body,
    File,
    Form,
    Param,
    Path,
    Query,
    TModel,
    TModels,
    _MultiPartBody,
)
from ninja.signature.utils import get_path_param_names, get_typed_signature

__all__ = [
    "ViewSignature",
    "is_pydantic_model",
    "is_collection_type",
    "detect_collection_fields",
]

FuncParam = namedtuple(
    "FuncParam", ["name", "alias", "source", "annotation", "is_collection"]
)


class ViewSignature:
    FLATTEN_PATH_SEP = (
        "\x1e"  # ASCII Record Separator.  IE: not generally used in query names
    )
    response_arg: Optional[str] = None

    def __init__(self, path: str, view_func: Callable[..., Any]) -> None:
        self.view_func = view_func
        self.signature = get_typed_signature(self.view_func)
        self.path = path
        self.path_params_names = get_path_param_names(path)
        self.docstring = inspect.cleandoc(view_func.__doc__ or "")
        self.has_kwargs = False

        self.params = []
        for name, arg in self.signature.parameters.items():
            if name == "request":
                # TODO: maybe better assert that 1st param is request or check by type?
                # maybe even have attribute like `has_request`
                # so that users can ignore passing request if not needed
                continue

            if arg.kind == arg.VAR_KEYWORD:
                # Skipping **kwargs
                self.has_kwargs = True
                continue

            if arg.kind == arg.VAR_POSITIONAL:
                # Skipping *args
                continue

            if arg.annotation is HttpResponse:
                self.response_arg = name
                continue

            if (
                arg.annotation is inspect.Parameter.empty
                and isinstance(arg.default, type)
                and issubclass(arg.default, pydantic.BaseModel)
            ):
                raise ConfigError(
                    f"Looks like you are using `{name}={arg.default.__name__}` instead of `{name}: {arg.default.__name__}` (annotation)"
                )

            func_param = self._get_param_type(name, arg)
            self.params.append(func_param)

        if hasattr(view_func, "_ninja_contribute_args"):
            # _ninja_contribute_args is a special attribute
            # which allows developers to create custom function params
            # inside decorators or other functions
            for p_name, p_type, p_source in view_func._ninja_contribute_args:
                self.params.append(
                    FuncParam(p_name, p_source.alias or p_name, p_source, p_type, False)
                )

        self.models: TModels = self._create_models()

        self._validate_view_path_params()

    def _validate_view_path_params(self) -> None:
        """verify all path params are present in the path model fields"""
        pass

    def _create_models(self) -> TModels:
        pass

    def _args_flatten_map(self, args: List[FuncParam]) -> Dict[str, Tuple[str, ...]]:
        pass

    def _model_flatten_map(self, model: TModel, prefix: str) -> Generator:
        pass

    def _get_param_type(self, name: str, arg: inspect.Parameter) -> FuncParam:
        # _EMPTY = self.signature.empty
        pass


def is_pydantic_model(cls: Any) -> bool:
    pass


def is_collection_type(type_annotation: Type) -> bool:
    pass


def detect_collection_fields(
    args: List[FuncParam], flatten_map: Dict[str, Tuple[str, ...]]
) -> List[str]:
    """
    Django QueryDict has values that are always lists, so we need to help django ninja to understand
    better the input parameters if it's a list or a single value
    This method detects attributes that should be treated by ninja as lists and returns this list as a result
    """
    pass


def is_optional(type_annotation: Type) -> bool:
    pass


def is_classvar_type(type_annotation: Type) -> bool:
    pass


def has_type(type_annotation: Type, f: Callable[[Type], bool]) -> bool:
    # Unwrap any type aliases (List, Set, etc.)
    pass
