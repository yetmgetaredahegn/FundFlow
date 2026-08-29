import requests


API_BASE_URL = "http://127.0.0.1:8000"


def check_backend_health():
    response = requests.get(
        f"{API_BASE_URL}/health",
        timeout=5,
    )

    response.raise_for_status()

    return response.json()


def process_application(
    audio_file,
    license_image,
    workshop_image,
):
    files = {
        "audio_file": (
            audio_file.name,
            audio_file.getvalue(),
            audio_file.type,
        ),
        "license_image": (
            license_image.name,
            license_image.getvalue(),
            license_image.type,
        ),
        "workshop_image": (
            workshop_image.name,
            workshop_image.getvalue(),
            workshop_image.type,
        ),
    }

    response = requests.post(
        f"{API_BASE_URL}/applications/process",
        files=files,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()