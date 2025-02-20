import pandas as pd
import structlog
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, PointStruct, VectorParams
from sentence_transformers import SentenceTransformer

from flare_ai_rag.retriever.config import QdrantConfig

logger = structlog.get_logger(__name__)


def _create_collection(
    client: QdrantClient, collection_name: str, vector_size: int
) -> None:
    """
    Creates a Qdrant collection with the given parameters.

    :param collection_name: Name of the collection.
    :param vector_size: Dimension of the vectors.
    """
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
    )


def generate_collection(
    df_docs: pd.DataFrame,
    client: QdrantClient,
    qdrant_config: QdrantConfig,
    collection_name: str,
) -> None:
    """Routine for generating a Qdrant collection for a specific CSV file type."""
    # Create the collection.
    _create_collection(client, collection_name, qdrant_config.vector_size)
    logger.info("Created the collection.", collection_name=collection_name)

    # Load the embedding model.
    embedding_model = SentenceTransformer(qdrant_config.embedding_model)

    # For each document in the CSV, compute its embedding and prepare a Qdrant point.
    points = []
    for i, row in df_docs.iterrows():
        doc_id = i
        content = row["Contents"]

        # Check if content is missing or not a string.
        if not isinstance(content, str):
            logger.warning(
                "Skipping document due to missing or invalid content.",
                filename=row["Filename"],
            )
            continue

        try:
            # Compute the embedding for the document content.
            embedding = embedding_model.encode(content).tolist()
        except Exception as e:
            logger.exception(
                "Error encoding document.", filename=row["Filename"], error=str(e)
            )
            continue

        # Prepare the payload.
        payload = {
            "filename": row["Filename"],
            "metadata": row["Metadata"],
            "text": content,
        }

        # Create a Qdrant point.
        point = PointStruct(id=doc_id, vector=embedding, payload=payload)  # pyright: ignore [reportArgumentType]
        points.append(point)

    if points:
        # Upload the points into the Qdrant collection.
        client.upsert(collection_name=collection_name, points=points)
        logger.info(
            "Collection generated and documents inserted into Qdrant successfully.",
            collection_name=collection_name,
            num_points=len(points),
        )
    else:
        logger.warning("No valid documents found to insert.")
