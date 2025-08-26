"""REST client handling, including RepriseStream base class."""

import backoff
from datetime import datetime, timezone
from typing import Callable, Any, Generator

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream

class RepriseStream(RESTStream):
    """Reprise stream class."""

    records_jsonpath = "$.data[*]"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.end_date = self.config.get("end_timestamp") if self.config.get("end_timestamp") else datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
        self.start_date = self.config.get("start_timestamp")

    @property
    def url_base(self) -> str:
        """Return the base URL for the API service."""
        url: str = self.config["api_url"]

        if self.name == "replay_session_activity_daily":
            extension: str = "replay_session_activity"
        elif self.name == "replicate_analytics_daily":
            extension: str = "api_replicate_analytics"
        else:
            extension: str = ""
        return f"{url}{extension}.json?"

    def backoff_wait_generator(self) -> Callable[..., Generator[float, Any, None]]:
        """Exponential backoff with a per-attempt cap of 300s."""
        return backoff.expo(base=2, factor=1, max_value=300)

    def backoff_jitter(self, value: float) -> float:
        return backoff.full_jitter(value)