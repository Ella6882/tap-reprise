"""REST client handling, including RepriseStream base class."""

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from typing import Iterable

import requests

class RepriseStream(RESTStream):
    """Reprise stream class."""

    records_jsonpath = "$.data[*]"

    @property
    def url_base(self) -> str:
        url: str = self.config["api_url"]
        return f"{url}?"

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        yield from extract_jsonpath(self.records_jsonpath, input=response.json())