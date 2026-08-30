import requests
import streamlit as st

from services.api_client import (
    get_audio_url,
    process_application,
    start_interview,
    submit_interview_answer,
)


st.set_page_config(
    page_title="FundFlow",
    page_icon="📄",
)


st.title("FundFlow")

st.write(
    "Turn your voice and business documents "
    "into a structured funding application."
)


# ---------------------------------------------------------------------------
# Application upload
# ---------------------------------------------------------------------------

st.subheader("Your application")

license_image = st.file_uploader(
    "Business licence",
    type=["jpg", "jpeg", "png"],
)

workshop_image = st.file_uploader(
    "Workshop / business photo",
    type=["jpg", "jpeg", "png"],
)


if license_image and workshop_image:
    st.success("All required files are ready.")

    if st.button("Build application"):
        try:
            with st.spinner(
                "Building your application..."
            ):
                result = process_application(
                    license_image,
                    workshop_image,
                )

            st.session_state["application_result"] = result

            # A newly built application starts a fresh interview.
            st.session_state.pop(
                "interview_state",
                None,
            )

            st.rerun()

        except requests.RequestException as error:
            st.error("Could not process application.")
            if error.response is not None:
                try:
                    error_data = error.response.json()
                    st.error(error_data.get("detail", str(error_data)))
                except ValueError:
                    st.error(error.response.text)


# ---------------------------------------------------------------------------
# Application result
# ---------------------------------------------------------------------------

application_result = st.session_state.get(
    "application_result"
)


if application_result:
    st.success("Your application draft is ready.")



# ---------------------------------------------------------------------------
# Interview start
# ---------------------------------------------------------------------------

if application_result:
    st.divider()

    st.subheader("Voice Interview")

    interview_state = st.session_state.get(
        "interview_state"
    )

    if interview_state is None:
        st.write(
            "Your application has been prepared. "
            "The interview will collect the missing "
            "information needed to complete it."
        )

        if st.button("Start interview"):
            try:
                with st.spinner(
                    "Preparing your interview..."
                ):
                    interview_state = start_interview()

                st.session_state[
                    "interview_state"
                ] = interview_state

                st.rerun()

            except requests.RequestException as error:
                st.error(
                    f"Could not start interview: {error}"
                )


# ---------------------------------------------------------------------------
# Active interview
# ---------------------------------------------------------------------------

interview_state = st.session_state.get(
    "interview_state"
)


if interview_state:
    current_question = interview_state.get(
        "current_question"
    )

    # -----------------------------------------------------------------------
    # Interview complete
    # -----------------------------------------------------------------------

    if current_question is None:
        st.success("Interview complete.")

        st.subheader("Completed application")

        st.json(
            interview_state["application"]
        )

    # -----------------------------------------------------------------------
    # Current question
    # -----------------------------------------------------------------------

    else:
        # -------------------------------------------------------------------
        # Chat History
        # -------------------------------------------------------------------
        history = interview_state.get("history", [])
        if history:
            st.markdown("### Interview Transcript")
            for i, turn in enumerate(history):
                with st.chat_message("assistant"):
                    st.write(turn["question"])
                with st.chat_message("user"):
                    st.write(turn["transcript"])
            st.divider()

        completed_fields = interview_state.get(
            "completed_fields",
            [],
        )

        question_number = (
            len(completed_fields) + 1
        )

        st.markdown(
            f"### Question {question_number}"
        )

        st.write(
            current_question["question"]
        )

        # -------------------------------------------------------------------
        # Question audio
        # -------------------------------------------------------------------

        audio_url = get_audio_url(
            interview_state.get("audio_url")
        )

        if audio_url:
            st.audio(
                audio_url,
                format="audio/wav",
            )

        # -------------------------------------------------------------------
        # Answer upload
        # -------------------------------------------------------------------

        answer_file = st.file_uploader(
            "Upload your answer",
            type=["mp3", "wav", "m4a"],
            key=(
                f"answer_"
                f"{current_question['field']}"
            ),
        )

        # -------------------------------------------------------------------
        # Submit answer
        # -------------------------------------------------------------------

        if answer_file:
            if st.button(
                "Submit answer",
                key=(
                    f"submit_"
                    f"{current_question['field']}"
                ),
            ):
                try:
                    with st.spinner(
                        "Processing your answer..."
                    ):
                        result = (
                            submit_interview_answer(
                                interview_state,
                                answer_file,
                            )
                        )

                    new_state = result["state"]

                    st.session_state[
                        "interview_state"
                    ] = new_state

                    st.rerun()

                except requests.RequestException as error:
                    st.error(
                        f"Could not submit answer: {error}"
                    )

                    if error.response is not None:
                        try:
                            st.json(
                                error.response.json()
                            )
                        except ValueError:
                            st.write(
                                error.response.text
                            )