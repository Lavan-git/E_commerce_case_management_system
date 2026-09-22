from abc import ABC, abstractmethod
from pathlib import Path


class BaseSourceAdapter(ABC):
    """
    Common interface for source readers.

    Each adapter knows how to read one source format and
    return records in that source's native structure.

    Standardization is intentionally handled separately.
    """

    source_name: str

    def __init__(self, path: Path) -> None:
        self.path = path

    @abstractmethod
    def read_raw(self) -> list[dict]:
        """Read records in the source's native structure."""
        raise NotImplementedError