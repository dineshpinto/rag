from dataclasses import dataclass


@dataclass(frozen=True)
class QdrantConfig:
    """Configuration for the embedding model used in the retriever."""

    embedding_model: str
    collection_name: str
    vector_size: int
    host: str
    port: int

    @staticmethod
    def load(retriever_config: dict) -> "QdrantConfig":
        return QdrantConfig(
            embedding_model=retriever_config["embedding_model"],
            collection_name=retriever_config["collection_name"],
            vector_size=retriever_config["vector_size"],
            host=retriever_config["host"],
            port=retriever_config["port"],
        )
