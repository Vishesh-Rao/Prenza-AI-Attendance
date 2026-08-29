import streamlit as st
from PIL import Image


@st.dialog("Capture or upload photos")
def add_photos_dialog():

    st.write(
        "Add classroom photos to scan for attendance"
    )

    # =========================================
    # INITIALIZE PHOTO TAB
    # =========================================

    if "photo_tab" not in st.session_state:
        st.session_state.photo_tab = "camera"

    # =========================================
    # INITIALIZE ATTENDANCE IMAGES
    # =========================================

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    # =========================================
    # TAB BUTTONS
    # =========================================

    t1, t2 = st.columns(2)

    # =========================================
    # CAMERA TAB
    # =========================================

    with t1:

        type_camera = (
            "primary"
            if st.session_state.photo_tab == "camera"
            else "tertiary"
        )

        if st.button(
            "Camera",
            type=type_camera,
            width="stretch"
        ):
            st.session_state.photo_tab = "camera"
            st.rerun()

    # =========================================
    # UPLOAD TAB
    # =========================================

    with t2:

        type_upload = (
            "primary"
            if st.session_state.photo_tab == "upload"
            else "tertiary"
        )

        if st.button(
            "Upload Photos",
            type=type_upload,
            width="stretch"
        ):
            st.session_state.photo_tab = "upload"
            st.rerun()

    # =========================================
    # CAMERA
    # =========================================

    if st.session_state.photo_tab == "camera":

        cam_photo = st.camera_input(
            "Take Snapshot",
            key="dialog_cam"
        )

        if cam_photo:

            image = Image.open(cam_photo)

            st.session_state.attendance_images.append(
                image
            )

            st.toast("Photo Captured")

            st.rerun()

    # =========================================
    # UPLOAD PHOTOS
    # =========================================

    elif st.session_state.photo_tab == "upload":

        uploaded_files = st.file_uploader(
            "Choose Image Files",
            type=["jpg", "png", "jpeg"],
            accept_multiple_files=True,
            key="dialog_upload"
        )

        if uploaded_files:

            for uploaded_file in uploaded_files:

                image = Image.open(uploaded_file)

                st.session_state.attendance_images.append(
                    image
                )

            st.toast("Photo(s) Uploaded Successfully")

            st.rerun()

    # =========================================
    # DONE
    # =========================================

    st.divider()

    if st.button(
        "Done",
        width="stretch"
    ):
        st.rerun()