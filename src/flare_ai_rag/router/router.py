from typing import override

from flare_ai_rag.openrouter.client import OpenRouterClient
from flare_ai_rag.router.base_router import BaseQueryRouter
from flare_ai_rag.router.config import RouterConfig
from flare_ai_rag.utils import parse_chat_response_as_json


class QueryRouter(BaseQueryRouter):
    """
    A simple query router that uses OpenRouter's chat completion endpoint to
    classify a query as ANSWER, CLARIFY, or REJECT.
    """

    def __init__(self, client: OpenRouterClient, config: RouterConfig) -> None:
        """
        Initialize the router with an API key and model name.
        :param api_key: Your OpenRouter API key.
        :param model: The model to use.
        """
        self.config = config
        self.client = client

    @override
    def route_query(self, query: str) -> str:
        """
        Analyze the query using the configured prompt and classify it.

        :param query: The user query.
        :return: One of the classification options defined in the config.
        """
        # Set the base prompt
        prompt = self.config.base_prompt + f"\nQuery: {query}"

        payload = {
            "model": self.config.model.model_id,
            "messages": [{"role": "user", "content": prompt}],
        }
        # Get response
        response = self.client.send_chat_completion(payload)
        classification = (
            parse_chat_response_as_json(response).get("classification", "").upper()
        )

        # Validate the classification.
        valid_options = {
            self.config.answer_option,
            self.config.clarify_option,
            self.config.reject_option,
        }
        if classification not in valid_options:
            classification = self.config.clarify_option

        return classification
