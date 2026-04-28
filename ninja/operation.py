import inspect
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    Dict,
    Iterable,
    List,
    Optional,
    Sequence,
    Type,
    Union,
    cast,
)

import pydantic
from asgiref.sync import async_to_sync
from django.http import HttpRequest, HttpResponse, HttpResponseNotAllowed
from django.http.response import HttpResponseBase

from ninja.compatibility.files import FIX_MIDDLEWARE_PATH, need_to_fix_request_files
from ninja.constants import NOT_SET, NOT_SET_TYPE
from ninja.errors import (
    AuthenticationError,
    ConfigError,
    Throttled,
    ValidationErrorContext,
)
from ninja.params.models import TModels
from ninja.schema import Schema, pydantic_version
from ninja.signature import ViewSignature, is_async
from ninja.throttling import BaseThrottle
from ninja.types import DictStrAny
from ninja.utils import check_csrf, is_async_callable

if TYPE_CHECKING:
    from ninja import NinjaAPI, Router  # pragma: no cover

__all__ = ["Operation", "PathView", "ResponseObject"]


class Operation:
    def __init__(
        self,
        path: str,
        methods: List[str],
        view_func: Callable,
        *,
        auth: Optional[Union[Sequence[Callable], Callable, NOT_SET_TYPE]] = NOT_SET,
        throttle: Union[BaseThrottle, List[BaseThrottle], NOT_SET_TYPE] = NOT_SET,
        response: Any = NOT_SET,
        operation_id: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        deprecated: Optional[bool] = None,
        by_alias: Optional[bool] = None,
        exclude_unset: Optional[bool] = None,
        exclude_defaults: Optional[bool] = None,
        exclude_none: Optional[bool] = None,
        include_in_schema: bool = True,
        url_name: Optional[str] = None,
        openapi_extra: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.is_async = False
        self.path: str = path
        self.methods: List[str] = methods
        self.view_func: Callable = view_func
        self.api: NinjaAPI = cast("NinjaAPI", None)
        if url_name is not None:
            self.url_name = url_name

        self.auth_param: Optional[Union[Sequence[Callable], Callable, object]] = auth
        self.auth_callbacks: Sequence[Callable] = []
        self._set_auth(auth)

        if isinstance(throttle, BaseThrottle):
            throttle = [throttle]
        self.throttle_param = throttle
        self.throttle_objects: List[BaseThrottle] = []
        if throttle is not NOT_SET:
            for th in throttle:  # type: ignore
                assert isinstance(
                    th, BaseThrottle
                ), "Throttle should be an instance of BaseThrottle"
                self.throttle_objects.append(th)

        self.signature = ViewSignature(self.path, self.view_func)
        self.models: TModels = self.signature.models

        self.response_models: Dict[Any, Any]
        if response is NOT_SET:
            self.response_models = {200: NOT_SET}
        elif isinstance(response, dict):
            self.response_models = self._create_response_model_multiple(response)
        else:
            self.response_models = {200: self._create_response_model(response)}

        if need_to_fix_request_files(methods, self.models):
            raise ConfigError(
                f"Router '{path}' has method(s) {methods}  that require fixing request.FILES. "
                f"Please add '{FIX_MIDDLEWARE_PATH}' to settings.MIDDLEWARE"
            )

        self.operation_id = operation_id
        self.summary = summary or self.view_func.__name__.title().replace("_", " ")
        self.description = description or self.signature.docstring
        self.tags = tags
        self.deprecated = deprecated
        self.include_in_schema = include_in_schema
        self.openapi_extra = openapi_extra

        # Exporting models params
        self.by_alias = by_alias or False
        self.exclude_unset = exclude_unset or False
        self.exclude_defaults = exclude_defaults or False
        self.exclude_none = exclude_none or False

        if hasattr(view_func, "_ninja_contribute_to_operation"):
            # Allow 3rd party code to contribute to the operation behavior
            callbacks: List[Callable] = view_func._ninja_contribute_to_operation
            for callback in callbacks:
                callback(self)

    def run(self, request: HttpRequest, **kw: Any) -> HttpResponseBase:
        pass

    def set_api_instance(self, api: "NinjaAPI", router: "Router") -> None:
        pass

    def _set_auth(
        self, auth: Optional[Union[Sequence[Callable], Callable, object]]
    ) -> None:
        pass

    def _run_checks(self, request: HttpRequest) -> Optional[HttpResponse]:
        "Runs security/throttle checks for each operation"
        pass

    def _run_authentication(self, request: HttpRequest) -> Optional[HttpResponse]:
        pass

    def _check_throttles(self, request: HttpRequest) -> Optional[HttpResponse]:
        pass

    def _result_to_response(
        self, request: HttpRequest, result: Any, temporal_response: HttpResponse
    ) -> HttpResponseBase:
        """
        The protocol for results
         - if HttpResponse - returns as is
         - if tuple with 2 elements - means http_code + body
         - otherwise it's a body
        """
        pass

    def _get_values(
        self, request: HttpRequest, path_params: Any, temporal_response: HttpResponse
    ) -> DictStrAny:
        pass

    def _create_response_model_multiple(
        self, response_param: DictStrAny
    ) -> Dict[str, Optional[Type[Schema]]]:
        pass

    def _create_response_model(self, response_param: Any) -> Optional[Type[Schema]]:
        pass


class AsyncOperation(Operation):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.is_async = True

    async def run(self, request: HttpRequest, **kw: Any) -> HttpResponseBase:  # type: ignore
        pass

    async def _run_checks(self, request: HttpRequest) -> Optional[HttpResponse]:  # type: ignore
        "Runs security checks for each operation"
        pass

    async def _run_authentication(self, request: HttpRequest) -> Optional[HttpResponse]:  # type: ignore
        pass


class PathView:
    def __init__(self) -> None:
        self.operations: List[Operation] = []
        self.is_async = False  # if at least one operation is async - will become True
        self.url_name: Optional[str] = None

    def add_operation(
        self,
        path: str,
        methods: List[str],
        view_func: Callable,
        *,
        auth: Optional[Union[Sequence[Callable], Callable, NOT_SET_TYPE]] = NOT_SET,
        throttle: Union[BaseThrottle, List[BaseThrottle], NOT_SET_TYPE] = NOT_SET,
        response: Any = NOT_SET,
        operation_id: Optional[str] = None,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        deprecated: Optional[bool] = None,
        by_alias: Optional[bool] = None,
        exclude_unset: Optional[bool] = None,
        exclude_defaults: Optional[bool] = None,
        exclude_none: Optional[bool] = None,
        url_name: Optional[str] = None,
        include_in_schema: bool = True,
        openapi_extra: Optional[Dict[str, Any]] = None,
    ) -> Operation:
        pass

    def set_api_instance(self, api: "NinjaAPI", router: "Router") -> None:
        pass

    def get_view(self) -> Callable:
        pass

    def _sync_view(self, request: HttpRequest, *a: Any, **kw: Any) -> HttpResponseBase:
        pass

    async def _async_view(
        self, request: HttpRequest, *a: Any, **kw: Any
    ) -> HttpResponseBase:
        pass

    def _find_operation(self, request: HttpRequest) -> Optional[Operation]:
        pass

    def _not_allowed(self) -> HttpResponse:
        pass


class ResponseObject:
    "Basically this is just a helper to be able to pass response to pydantic's model_validate"

    def __init__(self, response: HttpResponse) -> None:
        self.response = response
