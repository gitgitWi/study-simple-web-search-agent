from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Any, Optional, Self, Union

from pydantic import BaseModel, Field, SecretStr


class ModelReasoningEffort(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ModelOptions(BaseModel):
    api_key: Optional[SecretStr] = None
    model_name: str = Field(min_length=2, default="")
    temperature: float = Field(default=0.5)
    max_tokens: int = Field(default=4096)
    reasoning_effort: ModelReasoningEffort | None = Field(
        default=ModelReasoningEffort.MEDIUM
    )


class ModelService(ABC):
    model: Union[Any, None] = None
    model_options: ModelOptions = ModelOptions()

    def _set_service_key(self, api_key: SecretStr) -> Self:
        self.model_options = self.model_options.model_copy(update={"api_key": api_key})
        return self

    def set_model_options(
        self,
        model_name: str,
        temperature=0.5,
        max_tokens=4096,
        support_reasoning_effort=False,
        reasoning_effort: ModelReasoningEffort | None = None,
    ) -> Self:
        merged_option = self.model_options.model_copy(
            update={
                "model_name": model_name,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "reasoning_effort": reasoning_effort
                if support_reasoning_effort
                else None,
            }
        )
        self.model_options = ModelOptions.model_validate(merged_option)
        return self

    @abstractmethod
    def set_model(self) -> Self:
        raise NotImplementedError()

    def pre_invoke(self) -> Self:
        if not self.model:
            raise ValueError("Model is not set")
        return self

    @abstractmethod
    async def invoke(self, query: str) -> Any:
        raise NotImplementedError()
