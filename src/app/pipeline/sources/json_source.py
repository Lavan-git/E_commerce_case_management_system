import json

from app.pipeline.sources.base import BaseSourceAdapter


class JSONCaseAdapter(BaseSourceAdapter):
    source_name = "json"

    def read_raw(self) -> list[dict]:
        with self.path.open(
            mode="r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(
                "JSON source must contain a list of records."
            )

        return data