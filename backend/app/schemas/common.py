from typing import Literal

from pydantic import BaseModel, Field


class Gap(BaseModel):
    field: str
    status: Literal["missing", "unverified"]
    reason: str
    required_evidence: str | None = None
    provider: str | None = None