from pydantic import BaseModel, Field

from app.schemas.company import ApplicantDescription
from app.schemas.evidence import Evidence, TranscriptionResult
from app.schemas.gaps import InformationGap
from app.schemas.impact import ImpactProtocolDraft
from app.schemas.intervention import InterventionRequest


class FileMetadata(BaseModel):
    filename: str
    content_type: str


class ApplicationFiles(BaseModel):
    audio: FileMetadata | None = None
    license: FileMetadata
    workshop: FileMetadata

class ApplicationData(BaseModel):
    applicant: ApplicantDescription = Field(
        default_factory=ApplicantDescription
    )

    intervention: InterventionRequest = Field(
        default_factory=InterventionRequest
    )

    evidence: list[Evidence] = Field(
        default_factory=list
    )


class ApplicationResponse(BaseModel):
    status: str

    application: ApplicationData

    impact_protocol: ImpactProtocolDraft

    transcript: TranscriptionResult | None = None

    files: ApplicationFiles

    gaps: list[InformationGap] = Field(
        default_factory=list
    )