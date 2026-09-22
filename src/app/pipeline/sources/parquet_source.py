import pandas as pd

from app.pipeline.sources.base import BaseSourceAdapter


class ParquetCaseAdapter(BaseSourceAdapter):
    source_name = "parquet"

    def read_raw(self) -> list[dict]:
        dataframe = pd.read_parquet(self.path)

        return dataframe.to_dict(
            orient="records"
        )