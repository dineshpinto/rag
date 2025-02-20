from dataclasses import dataclass

from flare_ai_rag.openrouter.model import Model
from flare_ai_rag.settings import settings
from flare_ai_rag.utils import load_txt

# Load base prompt
BASE_PROMPT = load_txt(settings.input_path / "responder" / "prompts.txt")


@dataclass(frozen=True)
class ResponderConfig:
    model: Model
    base_prompt: str

    @staticmethod
    def load(model_config: dict) -> "ResponderConfig":
        """Loads the Responder config."""
        model = Model(
            model_id=model_config["id"],
            max_tokens=model_config["max_tokens"],
            temperature=model_config["temperature"],
        )

        return ResponderConfig(model=model, base_prompt=BASE_PROMPT)
