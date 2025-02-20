from dataclasses import dataclass


@dataclass(frozen=True)
class Model:
    model_id: str
    max_tokens: int
    temperature: float
