from enum import StrEnum

from langchain_cerebras import ChatCerebras
from langchain_core.messages import BaseMessage

from constants.envs import API_KEYS

from .model_service import ModelService


class CerebrasModelNames(StrEnum):
    GPT_OSS_120B = "gpt-oss-120b"


class CerebrasService(ModelService):
    model: ChatCerebras | None = None

    def __init__(self):
        super().__init__()
        self._set_service_key(API_KEYS.CEREBRAS)

    def set_model(self):
        self.model = ChatCerebras(**self.model_options.model_dump())
        return self

    async def invoke(self, query: str) -> BaseMessage | dict:
        super().pre_invoke()

        try:
            result: BaseMessage = await self.model.ainvoke(query)
            return result
        except Exception as e:
            print("[CerebrasService] ERROR", e)
            return {"has_error": True, "error": str(e)}
