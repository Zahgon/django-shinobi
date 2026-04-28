from json import dumps as json_dumps
from json import loads as json_loads
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from unittest.mock import Mock
from urllib.parse import urljoin

from django.http import QueryDict, StreamingHttpResponse
from django.http.request import HttpHeaders, HttpRequest

from ninja import NinjaAPI, Router
from ninja.responses import NinjaJSONEncoder
from ninja.responses import Response as HttpResponse


def build_absolute_uri(location: Optional[str] = None) -> str:
    pass


# TODO: this should be changed
# maybe add here urlconf object and add urls from here
class NinjaClientBase:
    __test__ = False  # <- skip pytest

    def __init__(
        self,
        router_or_app: Union[NinjaAPI, Router],
        headers: Optional[Dict[str, str]] = None,
        COOKIES: Optional[Dict[str, str]] = None,
    ) -> None:
        self.headers = headers or {}
        self.cookies = COOKIES or {}
        self.router_or_app = router_or_app

    def get(
        self, path: str, data: Optional[Dict] = None, **request_params: Any
    ) -> "NinjaResponse":
        return self.request("GET", path, data, **request_params)

    def post(
        self,
        path: str,
        data: Optional[Dict] = None,
        json: Any = None,
        **request_params: Any,
    ) -> "NinjaResponse":
        return self.request("POST", path, data, json, **request_params)

    def patch(
        self,
        path: str,
        data: Optional[Dict] = None,
        json: Any = None,
        **request_params: Any,
    ) -> "NinjaResponse":
        return self.request("PATCH", path, data, json, **request_params)

    def put(
        self,
        path: str,
        data: Optional[Dict] = None,
        json: Any = None,
        **request_params: Any,
    ) -> "NinjaResponse":
        return self.request("PUT", path, data, json, **request_params)

    def delete(
        self,
        path: str,
        data: Optional[Dict] = None,
        json: Any = None,
        **request_params: Any,
    ) -> "NinjaResponse":
        return self.request("DELETE", path, data, json, **request_params)

    def request(
        self,
        method: str,
        path: str,
        data: Optional[Dict] = None,
        json: Any = None,
        **request_params: Any,
    ) -> "NinjaResponse":
        pass

    @property
    def urls(self) -> List:
        pass

    def _resolve(
        self, method: str, path: str, data: Dict, request_params: Any
    ) -> Tuple[Callable, Mock, Dict]:
        pass

    def _build_request(
        self, method: str, path: str, data: Dict, request_params: Any
    ) -> Mock:
        pass


class TestClient(NinjaClientBase):
    def _call(self, func: Callable, request: Mock, kwargs: Dict) -> "NinjaResponse":
        pass


class TestAsyncClient(NinjaClientBase):
    async def _call(
        self, func: Callable, request: Mock, kwargs: Dict
    ) -> "NinjaResponse":
        pass


class NinjaResponse:
    def __init__(self, http_response: Union[HttpResponse, StreamingHttpResponse]):
        self._response = http_response
        self.status_code = http_response.status_code
        self.streaming = http_response.streaming
        if self.streaming:
            self.content = b"".join(http_response.streaming_content)  # type: ignore
        else:
            self.content = http_response.content  # type: ignore[union-attr]
        self._data = None

    def json(self) -> Any:
        pass

    @property
    def data(self) -> Any:
        pass

    def __getitem__(self, key: str) -> Any:
        return self._response[key]

    def __getattr__(self, attr: str) -> Any:
        return getattr(self._response, attr)
