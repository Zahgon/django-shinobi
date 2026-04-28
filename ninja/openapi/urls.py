from functools import partial
from typing import TYPE_CHECKING, Any, List

from django.urls import path

from .views import default_home, openapi_json, openapi_view

if TYPE_CHECKING:
    from ninja import NinjaAPI  # pragma: no cover

__all__ = ["get_openapi_urls", "get_root_url"]


def get_openapi_urls(api: "NinjaAPI") -> List[Any]:
    pass


def get_root_url(api: "NinjaAPI") -> Any:
    pass
