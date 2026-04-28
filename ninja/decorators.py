from functools import partial
from typing import Any, Callable, Tuple

from ninja.operation import Operation
from ninja.types import TCallable
from ninja.utils import contribute_operation_callback

# Since @api.method decorator is applied to function
# that is not always returns a HttpResponse object
# there is no way to apply some standard decorators form
# django stdlib or public plugins
#
# @decorate_view allows to apply any view decorator to Ninja api operation
#
# @api.get("/some")
# @decorate_view(cache_page(60 * 15)) # <-------
# def some(request):
#     ...
#


def decorate_view(*decorators: Callable[..., Any]) -> Callable[[TCallable], TCallable]:
    pass


def _apply_decorators(
    decorators: Tuple[Callable[..., Any]], operation: Operation
) -> None:
    pass
