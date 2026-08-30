from fastapi import APIRouter, File, UploadFile

from app.schemas import ApplicationResponse
from app.services.application_service import process_application


router = APIRouter(
    prefix="/applications",
    tags=["applications"],
)


@router.post(
    "/process",
    response_model=ApplicationResponse,
)
async def process_application_route(
    license_image: UploadFile = File(...),
    workshop_image: UploadFile = File(...),
) -> ApplicationResponse:
    return await process_application(
        license_image=license_image,
        workshop_image=workshop_image,
    )