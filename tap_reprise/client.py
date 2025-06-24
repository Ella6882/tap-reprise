"""REST client handling, including RepriseStream base class."""

from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.streams import RESTStream
from typing import Iterable
from datetime import datetime, timedelta

import requests

def date_range(start_datetime: datetime, end_datetime: datetime, step: int = 1) -> Iterable[tuple[str, str]]:
    """Generate date ranges of 1 day within the given timeframe.
    """
    start = datetime.strptime(start_datetime, "%Y-%m-%d %H:%M:%S")
    end = datetime.strptime(end_datetime, "%Y-%m-%d %H:%M:%S")

    while start < end:
        next_end = min(start + timedelta(days=step), end)
        yield start.strftime("%Y-%m-%d %H:%M:%S"), next_end.strftime("%Y-%m-%d %H:%M:%S")
        start = next_end

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

    def get_records(self, context: dict) -> Iterable[dict]:
        """Override to fetch records for each 31-day period."""
        
        for start, end in date_range(self.start_date, self.end_date):
            self.start_date = start
            self.end_date = end
            for record in self.request_records(context):
                transformed_record = self.post_process(record, context)

                if transformed_record is None:
                    continue

                yield transformed_record

    def parse_response(self, response: requests.Response) -> Iterable[dict]:
        """Parse the response and return an iterator of result records.

        Args:
            response: The HTTP ``requests.Response`` object.

        Yields:
            Each record from the source.
        """

        yield from extract_jsonpath(self.records_jsonpath, input=response.json())