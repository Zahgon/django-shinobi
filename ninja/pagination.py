import inspect
from abc import ABC, abstractmethod
from functools import partial, wraps
from math import inf
from typing import Any, AsyncGenerator, Callable, List, Optional, Tuple, Type, Union

from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils.module_loading import import_string
from typing_extensions import get_args as get_collection_args

from ninja import Field, Query, Router, Schema
from ninja.conf import settings
from ninja.constants import NOT_SET
from ninja.errors import ConfigError
from ninja.operation import Operation
from ninja.signature.details import is_collection_type
from ninja.utils import (
    contribute_operation_args,
    contribute_operation_callback,
    is_async_callable,
)


class PaginationBase(ABC):
    class Input(Schema):
        pass

    InputSource = Query(...)

    class Output(Schema):
        items: List[Any]
        count: int

    items_attribute: str = "items"

    def __init__(self, *, pass_parameter: Optional[str] = None, **kwargs: Any) -> None:
        self.pass_parameter = pass_parameter

    @abstractmethod
    def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Any,
        **params: Any,
    ) -> Any:
        pass  # pragma: no cover

    def _items_count(self, queryset: QuerySet) -> int:
        """
        Since lists are mainly compatible with QuerySets and can be passed to paginator.
        We will first to try to use .count - and if not there will use a len
        """
        pass


class AsyncPaginationBase(PaginationBase):
    @abstractmethod
    async def apaginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Any,
        **params: Any,
    ) -> Any:
        pass  # pragma: no cover

    async def _aitems_count(self, queryset: QuerySet) -> int:
        pass


class LimitOffsetPagination(AsyncPaginationBase):
    class Input(Schema):
        limit: int = Field(
            settings.PAGINATION_PER_PAGE,
            ge=1,
            le=(
                settings.PAGINATION_MAX_LIMIT
                if settings.PAGINATION_MAX_LIMIT != inf
                else None
            ),
        )
        offset: int = Field(0, ge=0)

    def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Input,
        **params: Any,
    ) -> Any:
        pass

    async def apaginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Input,
        **params: Any,
    ) -> Any:
        pass


class PageNumberPagination(AsyncPaginationBase):
    class Input(Schema):
        page: int = Field(1, ge=1)
        page_size: Optional[int] = Field(None, ge=1)

    def __init__(
        self,
        page_size: int = settings.PAGINATION_PER_PAGE,
        max_page_size: int = settings.PAGINATION_MAX_PER_PAGE_SIZE,
        **kwargs: Any,
    ) -> None:
        self.page_size = page_size
        self.max_page_size = max_page_size
        super().__init__(**kwargs)

    def _get_page_size(self, requested_page_size: Optional[int]) -> int:
        pass

    def paginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Input,
        **params: Any,
    ) -> Any:
        pass

    async def apaginate_queryset(
        self,
        queryset: QuerySet,
        pagination: Input,
        **params: Any,
    ) -> Any:
        pass


def paginate(func_or_pgn_class: Any = NOT_SET, **paginator_params: Any) -> Callable:
    """
    @api.get(...
    @paginate
    def my_view(request):

    or

    @api.get(...
    @paginate(PageNumberPagination)
    def my_view(request):

    """

    isfunction = inspect.isfunction(func_or_pgn_class)
    isnotset = func_or_pgn_class == NOT_SET

    pagination_class: Type[Union[PaginationBase, AsyncPaginationBase]] = import_string(
        settings.PAGINATION_CLASS
    )

    if isfunction:
        return _inject_pagination(func_or_pgn_class, pagination_class)

    if not isnotset:
        pagination_class = func_or_pgn_class

    def wrapper(func: Callable) -> Any:
        pass

    return wrapper


def _inject_pagination(
    func: Callable,
    paginator_class: Type[Union[PaginationBase, AsyncPaginationBase]],
    **paginator_params: Any,
) -> Callable:
    pass


class RouterPaginated(Router):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.pagination_class = import_string(settings.PAGINATION_CLASS)

    def add_api_operation(
        self, path: str, methods: List[str], view_func: Callable, **kwargs: Any
    ) -> None:
        pass


def make_response_paginated(paginator: PaginationBase, op: Operation) -> None:
    """
    Takes operation response and changes it to the paginated response
    for example:
        response=List[Some]
    will be changed to:
        response=PagedSome
    where Paged some will be a subclass of paginator.Output:
        class PagedSome:
            items: List[Some]
            count: int
    """
    pass


def _find_collection_response(op: Operation) -> Tuple[int, Any]:
    """
    Walks through defined operation responses and finds the first
    that is of a collection type (e.g. List[SomeSchema])
    """
    pass
