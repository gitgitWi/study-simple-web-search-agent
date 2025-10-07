from enum import StrEnum
from environs import env
from pydantic import SecretStr, BaseModel, Field


env.read_env()


class ApiKeyNames(StrEnum):
    CEREBRAS = "CEREBRAS"
    GROQ = "GROQ"


class ApiKeys(BaseModel):
    CEREBRAS: SecretStr = Field(
        min_length=2,
    )
    GROQ: SecretStr = Field(
        min_length=2,
    )


API_KEYS = ApiKeys(
    **{
        ApiKeyNames.CEREBRAS.value: env("CEREBRAS_API_KEY"),
        ApiKeyNames.GROQ.value: env("GROQ_API_KEY"),
    }
)
