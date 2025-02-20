import json
from typing import Any


def parse_chat_response(response: dict) -> str:
    """Parse response from chat completion endpoint"""
    return response.get("choices", [])[0].get("message", {}).get("content", "")


def extract_author(model_id: str) -> tuple[str, str]:
    """
    Extract the author and slug from a model_id.

    :param model_id: The model ID string.
    :return: A tuple (author, slug).
    """
    author, slug = model_id.split("/", 1)
    return author, slug


def parse_chat_response_as_json(response: dict) -> dict[str, Any]:
    """Parse response from chat completion endpoint"""
    json_data = parse_chat_response(response)
    return json.loads(json_data)
