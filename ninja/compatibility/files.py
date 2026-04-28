from typing import Any, List

from asgiref.sync import iscoroutinefunction, sync_to_async
from django.conf import settings
from django.http import HttpRequest
from django.utils.decorators import sync_and_async_middleware

from ninja.conf import settings as ninja_settings
from ninja.params.models import FileModel

FIX_MIDDLEWARE_PATH: str = "ninja.compatibility.files.fix_request_files_middleware"
FIX_METHODS = ninja_settings.FIX_REQUEST_FILES_METHODS


def need_to_fix_request_files(methods: List[str], params_models: List[Any]) -> bool:
    pass


@sync_and_async_middleware
def fix_request_files_middleware(get_response: Any) -> Any:
    """
    This middleware fixes long historical Django behavior where request.FILES is only
    populated for POST requests.
    https://code.djangoproject.com/ticket/12635
    """
    pass
