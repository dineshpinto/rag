import pandas as pd
import structlog
from qdrant_client import QdrantClient

from flare_ai_rag.openrouter import OpenRouterClient
from flare_ai_rag.responder import OpenRouterResponder, ResponderConfig
from flare_ai_rag.retriever import QdrantConfig, QdrantRetriever, generate_collection
from flare_ai_rag.router import QueryRouter, RouterConfig
from flare_ai_rag.settings import settings
from flare_ai_rag.utils import load_json, load_txt, save_json

logger = structlog.get_logger(__name__)


def setup_clients(input_config: dict) -> tuple[OpenRouterClient, QdrantClient]:
    """Initialize OpenRouter and Qdrant clients."""
    # Setup OpenRouter client.
    logger.info("Setting up Open Router client...")
    openrouter_client = OpenRouterClient(
        api_key=settings.open_router_api_key, base_url=settings.open_router_base_url
    )
    logger.info("Open Router client has been set up.")

    # Setup Qdrant client.
    logger.info("Setting up Qdrant client...")
    qdrant_config = QdrantConfig.load(input_config["qdrant_config"])
    qdrant_client = QdrantClient(host=qdrant_config.host, port=qdrant_config.port)
    logger.info("Qdrant client has been set up.")

    return openrouter_client, qdrant_client


def setup_router(
    openrouter_client: OpenRouterClient, input_config: dict
) -> QueryRouter:
    """Initialize the query router."""
    router_model_config = input_config["router_model"]
    router_config = RouterConfig.load(router_model_config)
    return QueryRouter(client=openrouter_client, config=router_config)


def setup_responder(
    openrouter_client: OpenRouterClient, input_config: dict
) -> OpenRouterResponder:
    """Initialize the responder."""
    responder_config = input_config["responder_model"]
    responder_config = ResponderConfig.load(responder_config)
    return OpenRouterResponder(
        client=openrouter_client, responder_config=responder_config
    )


def setup_retriever(
    qdrant_client: QdrantClient,
    input_config: dict,
    df_docs: pd.DataFrame,
    collection_name: str | None = None,
) -> QdrantRetriever:
    """Initialize the Qdrant retriever."""
    qdrant_config = QdrantConfig.load(input_config["qdrant_config"])

    # (Re)generate qdrant collection
    if collection_name:
        generate_collection(
            df_docs, qdrant_client, qdrant_config, collection_name=collection_name
        )
        logger.info(
            "The Qdrant collection has been generated.", collection_name=collection_name
        )
    # Return retriever
    return QdrantRetriever(client=qdrant_client, qdrant_config=qdrant_config)


def main() -> None:
    # Load input configuration.
    input_config = load_json(settings.input_path / "input_parameters.json")

    # Setup clients.
    openrouter_client, qdrant_client = setup_clients(input_config)

    # Setup the router.
    router = setup_router(openrouter_client, input_config)

    # Process user query.
    query = load_txt(settings.input_path / "query.txt")
    classification = router.route_query(query)
    logger.info(
        "Queried has been classified by the Router.", classification=classification
    )

    if classification == "ANSWER":
        df_docs = pd.read_csv(settings.data_path / "docs.csv", delimiter=",")
        logger.info("Loaded CSV Data.", num_rows=len(df_docs))

        # Retrieve docs
        retriever = setup_retriever(
            qdrant_client,
            input_config,
            df_docs,
            collection_name="docs_collection",
        )
        retrieved_docs = retriever.semantic_search(query, top_k=5)
        logger.info("Docs have been retrieved.")

        # Prepare answer
        responder = setup_responder(openrouter_client, input_config)
        answer = responder.generate_response(query, retrieved_docs)
        logger.info("Response has been generated.", answer=answer)

        # Save answer
        output_file = settings.data_path / "rag_answer.json"
        save_json(
            {
                "query": query,
                "answer": answer,
            },
            output_file,
        )

    elif classification == "CLARIFY":
        logger.info("Your query needs clarification. Please provide more details.")
    elif classification == "REJECT":
        logger.info("Your query has been rejected as it is out of scope.")
    else:
        logger.info("Unexpected classification.", classification=classification)


if __name__ == "__main__":
    main()
