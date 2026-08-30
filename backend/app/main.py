from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routes.applications import (
    router as applications_router,
)
from app.routes.interview import (
    GENERATED_AUDIO_DIRECTORY,
    router as interview_router,
)


GENERATED_AUDIO_DIRECTORY.mkdir(
    parents=True,
    exist_ok=True,
)


app = FastAPI(
    title="FundFlow API",
    version="0.1.0",
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.mount(
    "/interview/audio",
    StaticFiles(
        directory=GENERATED_AUDIO_DIRECTORY,
    ),
    name="interview-audio",
)


app.include_router(applications_router)
app.include_router(interview_router)