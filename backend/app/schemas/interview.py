from pydantic import BaseModel, Field

from app.schemas.application import ApplicationData


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