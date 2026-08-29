import requests
import streamlit as st

from services.api_client import process_application


st.set_page_config(
    page_title="FundFlow",
    page_icon="📄",
)


st.title("FundFlow")

st.write(
    "Turn your voice and business documents "
    "into a structured funding application."
)

st.subheader("Your application")

audio_file = st.file_uploader(
    "Voice note",
    type=["mp3", "wav", "m4a"],
)

license_image = st.file_uploader(
    "Business licence",
    type=["jpg", "jpeg", "png"],
)

workshop_image = st.file_uploader(
    "Workshop / business photo",
    type=["jpg", "jpeg", "png"],
)


if (
    audio_file
    and license_image
    and workshop_image
):
    st.success("All required files are ready.")

    if st.button("Process application"):
        try:
            with st.spinner(
                "Uploading application files..."
            ):
                result = process_application(
                    audio_file,
                    license_image,
                    workshop_image,
                )

                st.success("Application processed.")

                st.subheader("Application")
                st.json(result["application"])

                st.subheader("ImpactProtocol draft")
                st.json(result["impact_protocol"])

                st.subheader("Uploaded files")
                st.json(result["files"])

                st.subheader("Information gaps")
                st.json(result["gaps"])
                
        except requests.RequestException as error:
            st.error(
                f"Could not process application: {error}"
            )

else:
    st.info(
        "Please upload all three required files."
    )