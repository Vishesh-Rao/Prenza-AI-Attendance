import streamlit as st

from src.database.config import supabase
from src.database.db import enroll_student_to_subject

import time


@st.dialog("Enroll in Subject")
def enroll_dialog():

    st.write(
        "Enter the subject code provided by your teacher to enroll"
    )

    join_code = st.text_input(
        "Subject Code",
        placeholder="Eg: CS2034"
    )

    if st.button(
        "Enroll Now",
        width="stretch"
    ):

        if join_code:

            # Find subject using subject code
            res = (
                supabase
                .table("subjects")
                .select(
                    "subject_id, name, subject_code"
                )
                .eq(
                    "subject_code",
                    join_code
                )
                .execute()
            )

            # Check whether subject exists
            if res.data:

                subject = res.data[0]

                student_id = (
                    st.session_state
                    .student_data["student_id"]
                )

                # Check whether student is already enrolled
                check = (
                    supabase
                    .table("subject_students")
                    .select("*")
                    .eq(
                        "subject_id",
                        subject["subject_id"]
                    )
                    .eq(
                        "student_id",
                        student_id
                    )
                    .execute()
                )

                if check.data:

                    st.warning(
                        "You are already enrolled in this program"
                    )

                else:

                    enroll_student_to_subject(
                        student_id,
                        subject["subject_id"]
                    )

                    st.success(
                        "Successfully enrolled"
                    )

                    time.sleep(1)

                    st.rerun()

            else:

                st.warning(
                    "Subject code not found"
                )

        else:

            st.warning(
                "Please enter a subject code"
            )