# Standard
from typing import Any, Union
from typing import get_args, get_origin


class __NoPydanticModule:
    pass


# Third-party
try:
    from pydantic import BaseModel, ValidationError
except ModuleNotFoundError:
    BaseModel = __NoPydanticModule
    ValidationError = __NoPydanticModule

try:
    from pydantic import TypeAdapter
except ImportError:
    TypeAdapter = __NoPydanticModule

try:
    from pydantic import parse_obj_as
except ImportError:
    parse_obj_as = __NoPydanticModule

# Local
from .resolvers import eval_adapters
from toboggan.aliases import AdaptersEvalType
from toboggan.models import TypeEvalErrDump

__all__ = ('EvalReturn',)


class EvalReturn:
    __slots__ = ('__eval_type',)

    def __init__(self, eval_type: Any):
        self.__eval_type = eval_type
    
    def __eval_pydantic_v1(self, response: Any):
        validated = parse_obj_as(self.__eval_type, response)
        return validated
    
    def __eval_pydantic_v2(self, response: Any):
        validated = TypeAdapter(self.__eval_type).validate_python(response)
        return validated

    def __assessible_adapter_type(self) -> bool:
        if self.__eval_type:
            if args := get_args(self.__eval_type):
                return any(issubclass(arg, BaseModel) for arg in args)
            if issubclass(self.__eval_type, BaseModel):
                return True
        return False
    
    def __validate_adapter_type(self, response: Any):
        try:
            if AdaptersEvalType.PYDANTIC_V2 in eval_adapters:
                return self.__eval_pydantic_v2(response=response)
            if AdaptersEvalType.PYDANTIC_V1 in eval_adapters:
                return self.__eval_pydantic_v1(response=response)
        except ValidationError as err:
            err = TypeEvalErrDump(
                type_expected=err.errors(),
                type_evaluated=type(response)
            )
            raise Exception(err)
    
    def __validate_std_type(self, response: Any):
        # TODO: Fix the check for scenarios where Python arbitrary types are
        # nested as type hints.  i.e., `list[str]`.
        if not isinstance(response, type(self.__eval_type)):
                err = TypeEvalErrDump(
                    type_expected=self.__eval_type,
                    type_evaluated=type(response)
                )
                raise Exception(err)
        return response

    def evaluate(self, response: Any) -> Any:
        if self.__assessible_adapter_type():
            return self.__validate_adapter_type(response=response)
        if self.__eval_type:
            return self.__validate_std_type(response=response)
        return response
