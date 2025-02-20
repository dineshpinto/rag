import structlog

from flare_ai_rag.openrouter import OpenRouterClient
from flare_ai_rag.responder import OpenRouterResponder, ResponderConfig
from flare_ai_rag.settings import settings
from flare_ai_rag.utils import load_json

logger = structlog.get_logger(__name__)


def main() -> None:
    # Initialize OpenRouter client
    client = OpenRouterClient(
        api_key=settings.open_router_api_key, base_url=settings.open_router_base_url
    )

    # Set up responder config
    model_config = load_json(settings.input_path / "input_parameters.json")[
        "responder_model"
    ]
    responder_config = ResponderConfig.load(model_config)

    # Set up the Responder
    responder = OpenRouterResponder(client=client, responder_config=responder_config)

    # Mock retrieved documents
    query = "What is Flare?"
    retrieved_docs = [
        {
            "text": (
                "Flare is the blockchain for data ☀️**, offering developers and users "
                "secure, decentralized access to high-integrity data from other "
                "chains and the internet."
            ),
            "metadata": {"filename": "1-intro.mdx"},
        },
        {
            "text": (
                "Flare's Layer-1 network uniquely supports enshrined data protocols "
                "at the network layer, making it the only EVM-compatible smart "
                "contract platform optimized for decentralized data acquisition, "
                "including price and time-series data, blockchain event and state "
                "data, and Web2 API data.",
            ),
            "metadata": {"filename": "details.mdx"},
        },
    ]

    # Get answer
    answer = responder.generate_response(query, retrieved_docs)
    logger.info("Answer provided.", answer=answer)


if __name__ == "__main__":
    main()
