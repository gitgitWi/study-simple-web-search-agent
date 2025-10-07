from fastapi import APIRouter
from pydantic import BaseModel, Field

from model_services import ModelReasoningEffort
from model_services.cerebras import CerebrasModelNames, CerebrasService

router = APIRouter(prefix="")


class ChatMessage(BaseModel):
    prompt: str = Field(min_length=1)


@router.post("/cerebras")
async def cerebras_chat_handler(chat_message: ChatMessage):
    cerebras_service = CerebrasService()
    cerebras_service.set_model_options(
        model_name=CerebrasModelNames.GPT_OSS_120B,
        support_reasoning_effort=True,
        reasoning_effort=ModelReasoningEffort.HIGH,
    )

    return await cerebras_service.set_model().invoke(chat_message.prompt)
