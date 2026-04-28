import asyncio
import inspect
import re
from typing import Any, Callable, ForwardRef, List, Set

from django.urls import register_converter
from django.urls.converters import UUIDConverter
from pydantic._internal._typing_extra import eval_type_lenient as evaluate_forwardref

from ninja.types import DictStrAny

__all__ = [
    "get_typed_signature",
    "get_typed_annotation",
    "make_forwardref",
    "get_path_param_names",
    "is_async",
]


def get_typed_signature(call: Callable[..., Any]) -> inspect.Signature:
    "Finds call signature and resolves all forwardrefs"
    pass


def get_typed_annotation(param: inspect.Parameter, globalns: DictStrAny) -> Any:
    pass


def make_forwardref(annotation: str, globalns: DictStrAny) -> Any:
    # NOTE: in future versions of pydantic, the import may be changed to:
    # from pydantic._internal._typing_extra import try_eval_type
    # usage:
    # result, _ = try_eval_type(forward_ref, globalns, globalns)
    pass


def get_path_param_names(path: str) -> Set[str]:
    """turns path string like /foo/{var}/path/{int:another}/end to set {'var', 'another'}"""
    pass


def is_async(callable: Callable[..., Any]) -> bool:
    pass


def has_kwargs(func: Callable[..., Any]) -> bool:
    pass


def get_args_names(func: Callable[..., Any]) -> List[str]:
    "returns list of function argument names"
    pass


class UUIDStrConverter(UUIDConverter):
    """Return a path converted UUID as a str instead of the standard UUID"""

    def to_python(self, value: str) -> str:  # type: ignore
        pass


register_converter(UUIDStrConverter, "uuidstr")
