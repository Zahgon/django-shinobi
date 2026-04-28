import itertools
import re
from http.client import responses
from typing import TYPE_CHECKING, Any, Dict, Generator, List, Optional, Set, Tuple

from django.utils.termcolors import make_style

from ninja.constants import NOT_SET
from ninja.operation import Operation
from ninja.params.models import TModel, TModels
from ninja.schema import NinjaGenerateJsonSchema
from ninja.types import DictStrAny
from ninja.utils import normalize_path

if TYPE_CHECKING:
    from ninja import NinjaAPI  # pragma: no cover

REF_TEMPLATE: str = "#/components/schemas/{model}"

BODY_CONTENT_TYPES: Dict[str, str] = {
    "body": "application/json",
    "form": "application/x-www-form-urlencoded",
    "file": "multipart/form-data",
}


def get_schema(api: "NinjaAPI", path_prefix: str = "") -> "OpenAPISchema":
    pass


bold_red_style = make_style(opts=("bold",), fg="red")


class OpenAPISchema(dict):
    def __init__(self, api: "NinjaAPI", path_prefix: str) -> None:
        self.api = api
        self.path_prefix = path_prefix
        self.schemas: DictStrAny = {}
        self.securitySchemes: DictStrAny = {}
        self.all_operation_ids: Set = set()
        extra_info = api.openapi_extra.get("info", {})
        super().__init__([
            ("openapi", "3.1.0"),
            (
                "info",
                {
                    "title": api.title,
                    "version": api.version,
                    "description": api.description,
                    **extra_info,
                },
            ),
            ("paths", self.get_paths()),
            ("components", self.get_components()),
            ("servers", api.servers),
        ])
        for k, v in api.openapi_extra.items():
            if k not in self:
                self[k] = v

    def get_paths(self) -> DictStrAny:
        pass

    def methods(self, operations: list) -> DictStrAny:
        pass

    def deep_dict_update(
        self, main_dict: Dict[Any, Any], update_dict: Dict[Any, Any]
    ) -> None:
        pass

    def operation_details(self, operation: Operation) -> DictStrAny:
        pass

    def operation_parameters(self, operation: Operation) -> List[DictStrAny]:
        pass

    def _extract_parameters(self, model: TModel) -> List[DictStrAny]:
        pass

    def _flatten_schema(self, model: TModel) -> DictStrAny:
        pass

    def _create_schema_from_model(
        self,
        model: TModel,
        by_alias: bool = True,
        remove_level: bool = True,
    ) -> Tuple[DictStrAny, bool]:
        pass

    def _create_multipart_schema_from_models(
        self, models: TModels
    ) -> Tuple[DictStrAny, str]:
        # We have File and Form or Body, so we need to use multipart (File)
        pass

    def request_body(self, operation: Operation) -> DictStrAny:
        pass

    def responses(self, operation: Operation) -> Dict[int, DictStrAny]:
        pass

    def operation_security(self, operation: Operation) -> Optional[List[DictStrAny]]:
        pass

    def get_components(self) -> DictStrAny:
        pass

    def add_schema_definitions(self, definitions: dict) -> None:
        # TODO: check if schema["definitions"] are unique
        # if not - workaround (maybe use pydantic.schema.schema(models)) to process list of models
        # assert set(definitions.keys()) - set(self.schemas.keys()) == set()
        # ::TODO:: this is broken in interesting ways for by_alias,
        #     because same schema (name) can have different values
        pass


def flatten_properties(
    prop_name: str,
    prop_details: DictStrAny,
    prop_required: bool,
    definitions: DictStrAny,
) -> Generator[Tuple[str, DictStrAny, bool], None, None]:
    """
    extracts all nested model's properties into flat properties
    (used f.e. in GET params with multiple arguments and models)
    """
    pass


def resolve_allOf(details: DictStrAny, definitions: DictStrAny) -> None:
    """
    resolves all $ref's in 'allOf' section
    """
    pass


def merge_schemas(schemas: List[DictStrAny]) -> DictStrAny:
    pass
