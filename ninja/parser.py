import json
from typing import List, cast

from django.http import HttpRequest
from django.utils.datastructures import MultiValueDict

from ninja.types import DictStrAny

__all__ = ["Parser"]


class Parser:
    "Default json parser"

    def parse_body(self, request: HttpRequest) -> DictStrAny:
        pass

    def parse_querydict(
        self, data: MultiValueDict, list_fields: List[str], request: HttpRequest
    ) -> DictStrAny:
        pass
