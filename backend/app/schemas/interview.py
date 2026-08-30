from app.schemas.application import ApplicationData
from app.schemas.evidence import TranscriptionResult

from pydantic import BaseModel, Field


class InterviewQuestion(BaseModel):
    field: str
    question: str


class InterviewState(BaseModel):
    application: ApplicationData = Field(
        default_factory=ApplicationData
    )
    current_question: InterviewQuestion | None = None
    completed_fields: list[str] = Field(
        default_factory=list
    )
    audio_url: str | None = None


class InterviewAnswerResponse(BaseModel):
    state: InterviewState
    transcript: TranscriptionResult