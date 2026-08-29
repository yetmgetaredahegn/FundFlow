from fastapi import HTTPException, UploadFile

from app.schemas import (
    ApplicationData,
    ApplicationFiles,
    ApplicationResponse,
    FileMetadata,
    Gap,
)


async def process_application(
    audio_file: UploadFile,
    license_image: UploadFile,
    workshop_image: UploadFile,
) -> ApplicationResponse:
    validate_file_types(
        audio_file=audio_file,
        license_image=license_image,
        workshop_image=workshop_image,
    )

    return ApplicationResponse(
        status="received",
        application=ApplicationData(),
        files=ApplicationFiles(
            audio=FileMetadata(
                filename=audio_file.filename or "unknown",
                content_type=audio_file.content_type or "unknown",
            ),
            license=FileMetadata(
                filename=license_image.filename or "unknown",
                content_type=license_image.content_type or "unknown",
            ),
            workshop=FileMetadata(
                filename=workshop_image.filename or "unknown",
                content_type=workshop_image.content_type or "unknown",
            ),
        ),
        gaps=[
            Gap(
                field="business_name",
                status="missing",
                reason="Business information has not been processed yet.",
            ),
            Gap(
                field="applicant_name",
                status="missing",
                reason="Applicant information has not been processed yet.",
            ),
            Gap(
                field="location",
                status="missing",
                reason="Business location has not been established yet.",
            ),
            Gap(
                field="sector",
                status="missing",
                reason="Business sector has not been established yet.",
            ),
            Gap(
                field="funding_target_etb",
                status="missing",
                reason="Funding target has not been established yet.",
            ),
        ],
    )


def validate_file_types(
    audio_file: UploadFile,
    license_image: UploadFile,
    workshop_image: UploadFile,
) -> None:
    if not audio_file.content_type or not audio_file.content_type.startswith(
        "audio/"
    ):
        raise HTTPException(
            status_code=400,
            detail="audio_file must be an audio file.",
        )

    if not license_image.content_type or not license_image.content_type.startswith(
        "image/"
    ):
        raise HTTPException(
            status_code=400,
            detail="license_image must be an image file.",
        )

    if not workshop_image.content_type or not workshop_image.content_type.startswith(
        "image/"
    ):
        raise HTTPException(
            status_code=400,
            detail="workshop_image must be an image file.",
        )