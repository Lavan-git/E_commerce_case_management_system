import csv

from app.pipeline.sources.base import BaseSourceAdapter


class CSVCaseAdapter(BaseSourceAdapter):
    source_name = "csv"

    def read_raw(self) -> list[dict]:
        with self.path.open(
            mode="r",
            encoding="utf-8",
            newline="",
        ) as file:
            return list(csv.DictReader(file))