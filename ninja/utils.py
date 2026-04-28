import inspect
from typing import Any, Callable, Dict, Optional, Type

from django.conf import settings
from django.http import HttpRequest, HttpResponseForbidden
from django.middleware.csrf import CsrfViewMiddleware

__all__ = [
    "check_csrf",
    "is_debug_server",
    "normalize_path",
    "contribute_operation_callback",
]


def replace_path_param_notation(path: str) -> str:
    pass


def normalize_path(path: str) -> str:
    pass


def _no_view() -> None:
    pass  # pragma: no cover


def check_csrf(
    request: HttpRequest, callback: Callable = _no_view
) -> Optional[HttpResponseForbidden]:
    pass


def is_debug_server() -> bool:
    """Check if running under the Django Debug Server"""
    return settings.DEBUG and any(
        s.filename.endswith("runserver.py") and s.function == "run"
        for s in inspect.stack(0)[1:]
    )


def is_async_callable(f: Callable[..., Any]) -> bool:
    pass


def is_optional_type(t: Type[Any]) -> bool:
    pass


def contribute_operation_callback(
    func: Callable[..., Any], callback: Callable[..., Any]
) -> None:
    pass


def contribute_operation_args(
    func: Callable[..., Any], arg_name: str, arg_type: Type, arg_source: Any
) -> None:
    pass


def get_annotations(namespace: Dict[str, Any]) -> Any:
    """
    Inspecting annotations was changed in Python 3.14
    :param namespace:
    :return:
    """
    pass
