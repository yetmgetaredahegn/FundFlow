from typing import Any

from pydantic import BaseModel


class ExtractionResult(BaseModel):
    value: Any | None = None
    ambiguous: bool = False