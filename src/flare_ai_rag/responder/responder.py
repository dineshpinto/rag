from typing import override

from flare_ai_rag.openrouter.client import OpenRouterClient
from flare_ai_rag.responder.base_responder import BaseResponder
from flare_ai_rag.responder.config import ResponderConfig
from flare_ai_rag.utils import parse_chat_response


class OpenRouterResponder(BaseResponder):
    def __init__(
        self, client: OpenRouterClient, responder_config: ResponderConfig
    ) -> None:
        """
        Initialize the responder with an OpenRouter client and the model to use.

        :param client: An instance of OpenRouterClient.
        :param model: The model identifier to be used by the API.
        """
        self.client = client
        self.responder_config = responder_config

    @override
    def generate_response(self, query: str, retrieved_documents: list[dict]) -> str:
        """
        Generate a final answer using the query and the retrieved context,
        and include citations.

        :param query: The input query.
        :param retrieved_documents: A list of dictionaries containing retrieved docs.
        :return: The generated answer as a string.
        """
        context = ""

        # Build context from the retrieved documents.
        for idx, doc in enumerate(retrieved_documents, start=1):
            identifier = doc.get("metadata", {}).get("filename", f"Doc{idx}")
            context += f"Document {identifier}:\n{doc.get('text', '')}\n\n"

        # Compose the prompt
        prompt = self.responder_config.base_prompt.format(query=query, context=context)
        # Prepare the payload for the completion endpoint.
        payload = {
            "model": self.responder_config.model.model_id,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": self.responder_config.model.max_tokens,
            "temperature": self.responder_config.model.temperature,
        }
        # Send the prompt to the OpenRouter API.
        response = self.client.send_chat_completion(payload)

        return parse_chat_response(response)
