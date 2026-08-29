from pathlib import Path

from app.schemas import TranscriptionResult


def transcribe_audio(audio_path: Path) -> TranscriptionResult:
    """
    Transcribe an audio file into structured transcript data.

    The ASR implementation will be added in a later checkpoint.
    """
    raise NotImplementedError(
        "Speech transcription has not been configured yet."
    )