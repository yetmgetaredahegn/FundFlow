import streamlit as st

from services.api_client import process_application


st.set_page_config(
    page_title="FundFlow",
    page_icon="💰",
)


st.title("FundFlow")

st.write(
    "Turn your voice and business documents into "
    "a structured funding application."
)


st.header("Your application")


audio_file = st.file_uploader(
    "Voice note",
    type=["mp3", "wav", "m4a", "ogg", "webm"],
)

license_image = st.file_uploader(
    "Business licence",
    type=["jpg", "jpeg", "png", "webp"],
)

workshop_image = st.file_uploader(
    "Workshop / business photo",
    type=["jpg", "jpeg", "png", "webp"],
)


if audio_file and license_image and workshop_image:
    st.success("All required files are ready.")

    if st.button(
        "Process application",
        type="primary",
    ):
        try:
            with st.spinner("Uploading application..."):
                result = process_application(
                    audio_file=audio_file,
                    license_image=license_image,
                    workshop_image=workshop_image,
                )

            st.success("Application received.")

            st.subheader("Application")

            st.json(result["application"])

            st.subheader("Evidence")

            st.json(result["files"])

            st.subheader("Information gaps")

            st.json(result["gaps"])

        except Exception as error:
            st.error(f"Could not process application: {error}")

else:
    st.info(
        "Upload your voice note, business licence, "
        "and workshop photo to continue."
    )