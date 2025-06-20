"""Stream type classes for tap-reprise."""

from __future__ import annotations

import typing as t
from importlib import resources
import sys
from datetime import datetime, timezone

from tap_reprise.client import RepriseStream

if sys.version_info >= (3, 9):
    import importlib.resources as importlib_resources
else:
    import importlib_resources

SCHEMAS_DIR = importlib_resources.files(__package__) / "schemas"


class ReplaySessionActivityDailyStream(RepriseStream):
    """Replay Session Activity stream from the Replay Data API."""

    name = "replay_session_activity_daily"
    path = ""
    primary_keys = ["activity_id"]
    replication_key = "create_at"
    schema_filepath = SCHEMAS_DIR / "replay_session_activity.json"

    def get_url_params(
        self,
        context: dict | None,
        next_page_token: Any | None,
    ) -> dict[str, Any]:

        params = {}
        date_end = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

        start_date = self.get_starting_timestamp(context)

        if start_date is None:
            start_date_str = self.config.get("start_timestamp")
        else:
            start_date_str = start_date.strftime('%Y-%m-%d %H:%M:%S')

        params.update({
            "client_id": self.config["client_id"],
            "start_timestamp": start_date_str,
            "end_timestamp": date_end,
            "visitor_company": 1,
            "token": self.config["token"]
        })
            
        return params