from typing import TYPE_CHECKING, Any, NoReturn

from django.http import Http404, HttpRequest, HttpResponse

from ninja.openapi.docs import DocsBase
from ninja.responses import Response

if TYPE_CHECKING:
    # if anyone knows a cleaner way to make mypy happy - welcome
    from ninja import NinjaAPI  # pragma: no cover


def default_home(request: HttpRequest, api: "NinjaAPI", **kwargs: Any) -> NoReturn:
    "This view is mainly needed to determine the full path for API operations"
    pass


def openapi_json(request: HttpRequest, api: "NinjaAPI", **kwargs: Any) -> HttpResponse:
    pass


def openapi_view(request: HttpRequest, api: "NinjaAPI", **kwargs: Any) -> HttpResponse:
    pass
