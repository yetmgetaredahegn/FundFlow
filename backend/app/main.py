from fastapi import FastAPI

from app.routes import applications


app = FastAPI(
    title="FundFlow API",
    version="0.1.0",
)


app.include_router(applications.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}