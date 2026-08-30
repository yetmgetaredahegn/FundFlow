import json

import requests


API_BASE_URL = "http://127.0.0.1:8000"


def process_application(
    license_image,
    workshop_image,
):
    files = {
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


def start_interview():
    response = requests.post(
        f"{API_BASE_URL}/interview/start",
        timeout=120,
    )

    response.raise_for_status()

    return response.json()


def submit_interview_answer(
    state,
    audio_file,
):
    state_json = json.dumps(state)

    files = {
        "audio_file": (
            audio_file.name,
            audio_file.getvalue(),
            audio_file.type,
        ),
    }

    response = requests.post(
        f"{API_BASE_URL}/interview/answer",
        data={
            "state": state_json,
        },
        files=files,
        timeout=180,
    )

    response.raise_for_status()

    return response.json()


def get_audio_url(
    audio_url,
):
    if not audio_url:
        return None

    if (
        audio_url.startswith("http://")
        or audio_url.startswith("https://")
    ):
        return audio_url

    return f"{API_BASE_URL}{audio_url}"