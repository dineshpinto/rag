from abc import ABC, abstractmethod


class BaseQueryRouter(ABC):
    """
    An abstract base class defining the interface for query routings.
    """

    @abstractmethod
    def route_query(self, query: str) -> str:
        """
        Determine the type of the query: ANSWER, CLARIFY, or REJECT.
        """
