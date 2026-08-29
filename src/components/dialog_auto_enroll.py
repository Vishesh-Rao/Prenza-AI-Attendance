import streamlit as st
import time

from src.database.config import supabase
from src.database.db import enroll_student_to_subject


@st.dialog("Quick Enrollment")
def auto_enroll_dialog(subject_code):

    # =========================================
    # GET CURRENT STUDENT ID
    # =========================================

    student_id = st.session_state.student_data["student_id"]


    # =========================================
    # FIND SUBJECT
    # =========================================

    res = (
        supabase
        .table("subjects")
        .select("subject_id, name")
        .eq("subject_code", subject_code)
        .execute()
    )


    # =========================================
    # SUBJECT NOT FOUND
    # =========================================

    if not res.data:

        st.error("Subject Code not found!")

        if st.button("Close"):

            st.query_params.clear()
            st.rerun()

        return


    subject = res.data[0]


    # =========================================
    # CHECK WHETHER STUDENT IS ALREADY ENROLLED
    # =========================================

    check = (
        supabase
        .table("subject_students")
        .select("subject_id")
        .eq("subject_id", subject["subject_id"])
        .eq("student_id", student_id)
        .execute()
    )


    if check.data:

        st.info("You are already enrolled in this subject.")

        if st.button("Got it", width="stretch"):

            st.query_params.clear()
            st.rerun()

        


    # =========================================
    # CONFIRM ENROLLMENT
    # =========================================

    st.markdown(
        f"Would you like to enroll in **{subject['name']}**?"
    )


    col1, col2 = st.columns(2)


    # =========================================
    # NO THANKS
    # =========================================

    with col1:

        if st.button(
            "No Thanks",
            use_container_width=True
        ):

            st.query_params.clear()
            st.rerun()


    # =========================================
    # YES ENROLL
    # =========================================

    with col2:

        if st.button(
            "Yes Enroll Now",
            use_container_width=True
        ):

            enroll_student_to_subject(
                student_id,
                subject["subject_id"]
            )

            st.success("Joined Successfully!")

            st.query_params.clear()

            time.sleep(2)

            st.rerun()