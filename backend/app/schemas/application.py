from pydantic import BaseModel

from app.schemas.common import Gap


class ApplicationData(BaseModel):
    business_name: str | None = None
    applicant_name: str | None = None
    location: str | None = None
    sector: str | None = None
    funding_target_etb: float | None = None


class FileMetadata(BaseModel):
    filename: str
    content_type: str


class ApplicationFiles(BaseModel):
    audio: FileMetadata
    license: FileMetadata
    workshop: FileMetadata


class ApplicationResponse(BaseModel):
    status: str
    application: ApplicationData
    files: ApplicationFiles
    gaps: list[Gap]