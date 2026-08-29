import streamlit as st
import time
from PIL import Image
import numpy as np

from src.ui.base_layout import style_background_teacher

from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_all_students,
    create_student,
    get_student_subjects,
    get_Student_attendence,
    unenroll_student_to_subject

)

from src.components.dialog_enroll import enroll_dialog

from src.pipelines.face_pipeline import (
    predict_Attendece,
    get_face_embeddings,
    train_classifier
)

from src.pipelines.voice_pipeline import (
    get_voice_embedding
)
from src.components.subject_card import subject_card




def student_dashboard(): 
        

        student_data=st.session_state.student_data
        student_id=student_data['student_id']
   
        st.subheader(f""""Welcome Back, {student_data['name']}""")
        st.html(
           """
           <style>
   
           .home-text-link {
               position: fixed;
               top: 24px;
               right: 35px;
   
               z-index: 999999;
   
               color: #B9CACB !important;
   
               font-family: 'Inter', sans-serif;
               font-size: 14px;
               font-weight: 500;
   
               text-decoration: none !important;
   
               cursor: pointer;
   
               transition:
                   color 0.2s ease,
                   text-shadow 0.2s ease;
           }
   
           .home-text-link:hover {
               color: #12d8e8 !important;
   
               text-shadow:
                   0 0 10px rgba(18, 216, 232, 0.35);
           }
   
           </style>
   
           <a
               class="home-text-link"
               href="?go_home=true"
           >
               ← Logout
           </a>
           """
       )
   
       # =========================================
       # HANDLE HOME CLICK
       # =========================================
   
        if st.query_params.get("go_home") == "true":
   
           st.session_state["is_logged_in"] = False
   
           del st.session_state.student_data
   
           st.query_params.clear()
   
           st.rerun()

        st.space()

        c1,c2=st.columns(2)

        with c1:
            st.header('Your Enrolled Subjects')

        with c2:
            if st.button('Enroll in Subjects', width='stretch'):
                enroll_dialog()

        st.divider()

        with st.spinner("Loading your subjects"):

            subjects = get_student_subjects(student_id)

            logs = get_Student_attendence(student_id)

        stats_map={}

        for log in logs:
            sid=log['student_id']

            if sid not in stats_map:
                stats_map[sid]= {"total":0,"attended":0}

            stats_map[sid]['total']+= 1

            if logs.get('is_present'):
                stats_map[sid]['attended']+=1


        cols=st.columns(2)
        for i, sub_node in enumerate(subjects):
            sub = sub_node['subjects']
            sid = sub['subject_id']

            stats=stats_map.get(sid,{"total":0,"attended":0})
            def unroll_button():
                if st.button('Unenroll from this Course', width='stretch'):
                    unenroll_student_to_subject(student_id,sid)
                    st.toast(f"Unenrolled from {sub['name']} successfully!")
                    st.rerun()
                    

                    
            
            with cols[i%2]:
                subject_card(
                    name=sub['name'],
                    code=sub['subject_code'],
                    section=sub['section'],
                    stats=[
                        ('📆','Total',stats['total']),
                        ('✅','Attended', stats['attended']),

                    ],
                    footer_callback=unroll_button
                )










def student_screen():

    style_background_teacher()

    # =========================================
    # STUDENT ALREADY LOGGED IN
    # =========================================

    if "student_data" in st.session_state:

        student_dashboard()

        return


    # =========================================
    # INITIALIZE REGISTRATION STATE
    # =========================================

    if "show_student_registration" not in st.session_state:

        st.session_state["show_student_registration"] = False


    # =========================================
    # TOP RIGHT HOME TEXT
    # =========================================

    st.html(
        """
        <style>

        .home-text-link {
            position: fixed;
            top: 24px;
            right: 35px;

            z-index: 999999;

            color: #B9CACB !important;

            font-family: 'Inter', sans-serif;
            font-size: 14px;
            font-weight: 500;

            text-decoration: none !important;

            cursor: pointer;

            transition:
                color 0.2s ease,
                text-shadow 0.2s ease;
        }

        .home-text-link:hover {
            color: #12d8e8 !important;

            text-shadow:
                0 0 10px rgba(18, 216, 232, 0.35);
        }

        </style>

        <a
            class="home-text-link"
            href="?go_home=true"
        >
            ← Home
        </a>
        """
    )


    # =========================================
    # HANDLE HOME CLICK
    # =========================================

    if st.query_params.get("go_home") == "true":

        st.session_state["login_type"] = None

        st.session_state.pop(
            "show_student_registration",
            None
        )

        st.query_params.clear()

        st.rerun()


    # =========================================
    # TITLE
    # =========================================

    st.markdown(
        """
        <div class="teacher-register-title">
            Login using <span>Face-ID</span>
        </div>
        """,
        unsafe_allow_html=True
    )


    # =========================================
    # CAMERA
    # =========================================

    photo_source = st.camera_input(
        "Position your face in the center"
    )


    # =========================================
    # FACE SCANNING
    # =========================================

    if photo_source:

        img = np.array(
            Image.open(photo_source)
        )

        with st.spinner("AI is Scanning..."):

            detected, all_ids, num_faces = predict_Attendece(img)


        # =====================================
        # NO FACE
        # =====================================

        if num_faces == 0:

            st.warning("Face not found")

            st.session_state[
                "show_student_registration"
            ] = False


        # =====================================
        # MULTIPLE FACES
        # =====================================

        elif num_faces > 1:

            st.warning("Multiple Faces Found")

            st.session_state[
                "show_student_registration"
            ] = False


        # =====================================
        # ONE FACE
        # =====================================

        else:

            # =================================
            # FACE RECOGNIZED
            # =================================

            if detected:

                student_id = list(
                    detected.keys()
                )[0]

                all_students = get_all_students()

                student = next(
                    (
                        s for s in all_students
                        if s["student_id"] == student_id
                    ),
                    None
                )


                if student:

                    st.session_state["is_logged_in"] = True

                    st.session_state["user_role"] = "student"

                    st.session_state["student_data"] = student

                    st.session_state[
                        "show_student_registration"
                    ] = False

                    st.toast(
                        f"Welcome Back {student['name']}"
                    )

                    time.sleep(1)

                    st.rerun()


            # =================================
            # FACE NOT RECOGNIZED
            # =================================

            else:

                st.info(
                    "Face not recognised! "
                    "You might be a new student."
                )

                st.session_state[
                    "show_student_registration"
                ] = True


    # =========================================
    # REGISTRATION FORM
    # =========================================

    if st.session_state.get(
        "show_student_registration",
        False
    ):

        with st.container(border=True):

            st.header(
                "Register New Profile"
            )


            # =================================
            # NAME
            # =================================

            new_name = st.text_input(
                "Enter Your Name",
                placeholder="eg: Adam",
                key="student_registration_name"
            )


            # =================================
            # VOICE ENROLLMENT
            # =================================

            st.subheader(
                "Optional: Voice Enrollment"
            )

            st.info(
                "Enroll your voice for "
                "voice-only attendance."
            )


            audio_data = None


            try:

                audio_data = st.audio_input(
                    "Record a short phrase like "
                    "'I am present. My name is Adam.'"
                )

            except Exception:

                st.error(
                    "Audio Data failed!"
                )


            # =================================
            # CREATE ACCOUNT
            # =================================

            if st.button(
                "Create Account",
                type="primary",
                key="create_student_account"
            ):

                if not new_name:

                    st.warning(
                        "Please enter your name!"
                    )

                elif photo_source is None:

                    st.warning(
                        "Please capture your face first."
                    )

                else:

                    with st.spinner(
                        "Creating Profile..."
                    ):

                        img = np.array(
                            Image.open(
                                photo_source
                            )
                        )


                        # =========================
                        # FACE EMBEDDING
                        # =========================

                        encodings = get_face_embeddings(
                            img
                        )


                        if encodings:

                            face_emb = encodings[
                                0
                            ].tolist()


                            # =====================
                            # VOICE EMBEDDING
                            # =====================

                            voice_emb = None


                            if audio_data:

                                voice_emb = (
                                    get_voice_embedding(
                                        audio_data.read()
                                    )
                                )


                            # =====================
                            # CREATE STUDENT
                            # =====================

                            response_data = create_student(
                                new_name,
                                face_embedding=face_emb,
                                voice_embedding=voice_emb
                            )


                            if response_data:

                                train_classifier()


                                st.session_state[
                                    "is_logged_in"
                                ] = True


                                st.session_state[
                                    "user_role"
                                ] = "student"


                                st.session_state[
                                    "student_data"
                                ] = response_data[0]


                                st.session_state[
                                    "show_student_registration"
                                ] = False


                                st.toast(
                                    f"Profile Created! "
                                    f"Hi, {new_name}"
                                )


                                time.sleep(1)

                                st.rerun()


                            else:

                                st.error(
                                    "Could not create "
                                    "your student profile."
                                )


                        else:

                            st.error(
                                "Couldn't capture your "
                                "facial features for registration."
                            )