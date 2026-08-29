import streamlit as st

from src.ui.base_layout import style_background_teacher

from src.database.db import (
    check_teacher_exists,
    create_teacher,
    teacher_login,
    get_teacher_subject,
    get_attendance_for_teacher
)

from src.components.dialog_create_subject import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.dialog_share_subject import share_subject_dialog
from src.components.dialog_add_photo import add_photos_dialog
from src.components.dialog_attendence_result import attendence_result_dialog

from src.pipelines.face_pipeline import predict_Attendece

import numpy as np
from src.database.config import supabase

from datetime import datetime
import pandas as pd

from src.components.dialog_voice_attendance import voice_attendance_dialog


# =========================================
# TEACHER SCREEN
# =========================================

def teacher_screen():

    style_background_teacher()

    if "teacher_data" in st.session_state:

        teacher_dashboard()

    elif (
        "teacher_login_type" not in st.session_state
        or st.session_state.teacher_login_type == "login"
    ):

        teacher_screen_login()

    elif st.session_state.teacher_login_type == "register":

        teacher_screen_register()


# =========================================
# TEACHER DASHBOARD
# =========================================

def teacher_dashboard():

    teacher_data = st.session_state.teacher_data

    st.subheader(
        f"Welcome Back, {teacher_data['name']}"
    )

    # =========================================
    # TOP RIGHT LOGOUT
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
            ← Logout
        </a>
        """
    )

    # =========================================
    # HANDLE LOGOUT
    # =========================================

    if st.query_params.get("go_home") == "true":

        st.session_state["is_logged_in"] = False

        st.session_state.pop(
            "teacher_data",
            None
        )

        st.session_state["teacher_login_type"] = "login"

        st.query_params.clear()

        st.rerun()

    # =========================================
    # TABS
    # =========================================

    st.space()

    if "current_teacher_tab" not in st.session_state:

        st.session_state.current_teacher_tab = "take_attendence"

    tab1, tab2, tab3 = st.columns(3)

    with tab1:

        if st.button(
            "Take Attendence",
            width="stretch"
        ):

            st.session_state.current_teacher_tab = "take_attendence"

            st.rerun()

    with tab2:

        if st.button(
            "Manage Subjects",
            width="stretch"
        ):

            st.session_state.current_teacher_tab = "manage_subjects"

            st.rerun()

    with tab3:

        if st.button(
            "Attendence Records",
            width="stretch"
        ):

            st.session_state.current_teacher_tab = "attendence_records"

            st.rerun()

    st.divider()

    # =========================================
    # LOAD SELECTED TAB
    # =========================================

    if st.session_state.current_teacher_tab == "take_attendence":

        teacher_tab_take_attendence()

    elif st.session_state.current_teacher_tab == "manage_subjects":

        teacher_tab_manage_subjects()

    elif st.session_state.current_teacher_tab == "attendence_records":

        teacher_tab_attendence_records()


# =========================================
# TAKE ATTENDANCE
# =========================================

def teacher_tab_take_attendence():

    teacher_id = st.session_state.teacher_data["teacher_id"]

    st.header("Take AI Attendence")

    # =========================================
    # ATTENDANCE IMAGES
    # =========================================

    if "attendance_images" not in st.session_state:

        st.session_state.attendance_images = []

    # =========================================
    # GET SUBJECTS
    # =========================================

    subjects = get_teacher_subject(teacher_id)

    if not subjects:

        st.warning(
            "You havent created any subjects yet! "
            "Please create one to begin"
        )

        return

    # =========================================
    # SUBJECT SELECTION
    # =========================================

    subjects_options = {
        f"{s['name']} - {s['subject_code']}":
        s["subject_id"]

        for s in subjects
    }

    col1, col2 = st.columns(
        [3, 1],
        vertical_alignment="bottom"
    )

    with col1:

        selected_subject_label = st.selectbox(
            "Select Subject",
            options=list(subjects_options.keys())
        )

    with col2:

        if st.button(
            "Add Photos",
            icon=":material/photo_prints:",
            width="stretch"
        ):

            add_photos_dialog()

    selected_subject_id = subjects_options[
        selected_subject_label
    ]

    st.divider()

    # =========================================
    # DISPLAY PHOTOS
    # =========================================

    if st.session_state.attendance_images:

        st.header("Added Photos")

        gallery_cols = st.columns(4)

        for idx, img in enumerate(
            st.session_state.attendance_images
        ):

            with gallery_cols[idx % 4]:

                st.image(
                    img,
                    width="stretch",
                    caption=f"Photo {idx + 1}"
                )

    # =========================================
    # PHOTO CONTROLS
    # =========================================

    has_photos = bool(
        st.session_state.attendance_images
    )

    c1, c2, c3 = st.columns(3)

    # =========================================
    # CLEAR PHOTOS
    # =========================================

    with c1:

        if st.button(
            "Clear all Photos",
            width="stretch",
            icon=":material/delete:",
            disabled=not has_photos
        ):

            st.session_state.attendance_images = []

            st.rerun()

    # =========================================
    # FACE ANALYSIS
    # =========================================

    with c2:

        if st.button(
            "Run Face Analysis",
            width="stretch",
            icon=":material/analytics:",
            disabled=not has_photos
        ):

            with st.spinner(
                "Deep Scanning classroom photos..."
            ):

                all_detected_ids = {}

                # =============================
                # PROCESS EVERY PHOTO
                # =============================

                for idx, img in enumerate(
                    st.session_state.attendance_images
                ):

                    img_np = np.array(
                        img.convert("RGB")
                    )

                    detected, _, _ = predict_Attendece(
                        img_np
                    )

                    if detected:

                        for sid in detected.keys():

                            student_id = int(sid)

                            all_detected_ids.setdefault(
                                student_id,
                                []
                            ).append(
                                f"photo {idx + 1}"
                            )

                # =============================
                # GET ENROLLED STUDENTS
                # =============================

                enrolled_res = (
                    supabase
                    .table("subject_students")
                    .select("*,students(*)")
                    .eq(
                        "subject_id",
                        selected_subject_id
                    )
                    .execute()
                )

                enrolled_students = enrolled_res.data

                if not enrolled_students:

                    st.warning(
                        "No students in this course"
                    )

                else:

                    results = []

                    attendance_to_log = []

                    current_timestamp = (
                        datetime.now()
                        .strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    )

                    # =========================
                    # BUILD ATTENDANCE RESULTS
                    # =========================

                    for node in enrolled_students:

                        student = node["students"]

                        sources = all_detected_ids.get(
                            int(student["student_id"]),
                            []
                        )

                        is_present = len(sources) > 0

                        results.append(
                            {
                                "Name": student["name"],

                                "ID": student["student_id"],

                                "Source": (
                                    ", ".join(sources)
                                    if is_present
                                    else "_"
                                ),

                                "Status": (
                                    "✅ Present"
                                    if is_present
                                    else "❌ Absent"
                                )
                            }
                        )

                        attendance_to_log.append(
                            {
                                "student_id":
                                    student["student_id"],

                                "subject_id":
                                    selected_subject_id,

                                "timestamp":
                                    current_timestamp,

                                "is_present":
                                    bool(is_present)
                            }
                        )

                    # =========================
                    # SHOW RESULT
                    # =========================

                    attendence_result_dialog(
                        pd.DataFrame(results),
                        attendance_to_log
                    )

    # =========================================
    # VOICE ATTENDANCE
    # =========================================

    with c3:

        if st.button(
            "Use Voice Attendance",
            width="stretch",
            icon=":material/mic:"
        ):

            voice_attendance_dialog(
                selected_subject_id
            )


# =========================================
# MANAGE SUBJECTS
# =========================================

def teacher_tab_manage_subjects():

    teacher_id = st.session_state.teacher_data[
        "teacher_id"
    ]

    col1, col2 = st.columns(2)

    with col1:

        st.header("Manage Subject")

    with col2:

        if st.button(
            "Create New Subject",
            width="stretch"
        ):

            create_subject_dialog(
                teacher_id
            )

    # =========================================
    # GET SUBJECTS
    # =========================================

    subjects = get_teacher_subject(
        teacher_id
    )

    if subjects:

        for sub in subjects:

            stats = [
                (
                    "👥",
                    "Students",
                    sub["total_students"]
                ),

                (
                    "🕛",
                    "Classes",
                    sub["total_classes"]
                )
            ]

            # =============================
            # SHARE BUTTON
            # =============================

            def share_btn(
                subject=sub
            ):

                if st.button(
                    f"Share Code: {subject['name']}",
                    key=f"share_{subject['subject_code']}",
                    icon=":material/share:",
                    width="stretch"
                ):

                    share_subject_dialog(
                        subject["name"],
                        subject["subject_code"]
                    )

            st.space()

            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=stats,
                footer_callback=share_btn
            )

    else:

        st.info(
            "NO SUBJECT FOUND"
        )


# =========================================
# ATTENDANCE RECORDS
# =========================================

def teacher_tab_attendence_records():

    st.header(
        "Attendence Records"
    )

    teacher_id = st.session_state.teacher_data[
        "teacher_id"
    ]

    records = get_attendance_for_teacher(
        teacher_id
    )

    if not records:

        st.info(
            "No attendance records found."
        )

        return

    data = []

    # =========================================
    # PREPARE RECORD DATA
    # =========================================

    for r in records:

        ts = r.get("timestamp")

        if ts:

            # Convert timestamp to string safely
            ts_string = str(ts)

            # Remove microseconds for grouping
            ts_group = ts_string.split(".")[0]

            try:

                formatted_time = (
                    datetime.fromisoformat(
                        ts_string.replace("Z", "+00:00")
                    )
                    .strftime(
                        "%Y-%m-%d %I:%M %p"
                    )
                )

            except ValueError:

                formatted_time = ts_string

        else:

            ts_group = None

            formatted_time = "N/A"

        subject = r.get("subjects") or {}

        data.append(
            {
                "ts_group": ts_group,

                "Time": formatted_time,

                "Subject": subject.get(
                    "name",
                    "Unknown"
                ),

                "Subject Code": subject.get(
                    "subject_code",
                    "N/A"
                ),

                "is_present": bool(
                    r.get(
                        "is_present",
                        False
                    )
                )
            }
        )

    # =========================================
    # CREATE DATAFRAME
    # =========================================

    df = pd.DataFrame(data)

    if df.empty:

        st.info(
            "No attendance records found."
        )

        return

    # =========================================
    # GROUP ATTENDANCE
    # =========================================

    summary = (
        df.groupby(
            [
                "ts_group",
                "Time",
                "Subject",
                "Subject Code"
            ],
            dropna=False
        )
        .agg(
            Present_Count=(
                "is_present",
                "sum"
            ),

            Total_Count=(
                "is_present",
                "count"
            )
        )
        .reset_index()
    )

    # =========================================
    # ATTENDANCE STATS
    # =========================================

    summary["Attendance Stats"] = (
        "✅ "
        + summary["Present_Count"].astype(str)
        + " / "
        + summary["Total_Count"].astype(str)
        + " Students"
    )

    # =========================================
    # DISPLAY DATA
    # =========================================

    display_df = summary.sort_values(
        by="ts_group",
        ascending=False
    )[
        [
            "Time",
            "Subject",
            "Subject Code",
            "Attendance Stats"
        ]
    ]

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True
    )


# =========================================
# REGISTER TEACHER
# =========================================

def register_teacher(
    teacher_username,
    teacher_name,
    teacher_password,
    teacher_confirm_password
):

    if (
        not teacher_username
        or not teacher_name
        or not teacher_password
    ):

        return (
            False,
            "All fields are required!"
        )

    if check_teacher_exists(
        teacher_username
    ):

        return (
            False,
            "Username already taken"
        )

    if (
        teacher_password
        != teacher_confirm_password
    ):

        return (
            False,
            "Password doesn't match"
        )

    try:

        create_teacher(
            teacher_username,
            teacher_password,
            teacher_name
        )

        return (
            True,
            "Successfully created! Login Now"
        )

    except Exception:

        return (
            False,
            "Unexpected Error"
        )


# =========================================
# LOGIN TEACHER
# =========================================

def login_teacher(
    username,
    password
):

    if not username or not password:

        return False

    teacher = teacher_login(
        username,
        password
    )

    if teacher:

        st.session_state.user_role = "teacher"

        st.session_state.teacher_data = teacher

        st.session_state.is_logged_in = True

        st.session_state.teacher_login_type = "login"

        return True

    return False


# =========================================
# TEACHER LOGIN SCREEN
# =========================================

def teacher_screen_login():

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

    if st.query_params.get(
        "go_home"
    ) == "true":

        st.session_state["login_type"] = None

        st.session_state["teacher_login_type"] = "login"

        st.query_params.clear()

        st.rerun()

    # =========================================
    # LOGIN TITLE
    # =========================================

    st.markdown(
        """
        <div class="teacher-register-title">
            Login using <span>Password</span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================================
    # LOGIN FORM
    # =========================================

    left, center, right = st.columns(
        [1, 2.2, 1]
    )

    with center:

        teacher_username = st.text_input(
            "Enter Username",
            placeholder="ananyaroy",
            key="teacher_username"
        )

        teacher_password = st.text_input(
            "Enter Password",
            type="password",
            placeholder="Enter Password",
            key="teacher_password"
        )

        st.divider()

        # =====================================
        # LOGIN / REGISTER
        # =====================================

        btnc1, btnc2 = st.columns(
            2,
            gap="medium"
        )

        with btnc1:

            if st.button(
                "Login",
                key="teacher_login",
                use_container_width=True
            ):

                if login_teacher(
                    teacher_username,
                    teacher_password
                ):

                    st.toast(
                        "Welcome back!"
                    )

                    import time

                    time.sleep(1)

                    st.rerun()

                else:

                    st.error(
                        "Invalid Username and Password"
                    )

        with btnc2:

            if st.button(
                "Register",
                key="teacher_register",
                use_container_width=True
            ):

                st.session_state.teacher_login_type = "register"

                st.rerun()


# =========================================
# TEACHER REGISTER SCREEN
# =========================================

def teacher_screen_register():

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

    if st.query_params.get(
        "go_home"
    ) == "true":

        st.session_state["login_type"] = None

        st.session_state["teacher_login_type"] = "login"

        st.query_params.clear()

        st.rerun()

    # =========================================
    # REGISTER TITLE
    # =========================================

    st.markdown(
        """
        <div class="teacher-register-title">
            Register your <span>Teacher</span> Profile
        </div>
        """,
        unsafe_allow_html=True
    )

    # =========================================
    # REGISTER FORM
    # =========================================

    left, center, right = st.columns(
        [1, 2.2, 1]
    )

    with center:

        teacher_username = st.text_input(
            "Enter Username",
            placeholder="Username",
            key="register_teacher_username"
        )

        teacher_name = st.text_input(
            "Enter Name",
            placeholder="Name",
            key="register_teacher_name"
        )

        teacher_password = st.text_input(
            "Enter Password",
            type="password",
            placeholder="Enter Password",
            key="register_teacher_password"
        )

        teacher_confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Confirm Password",
            key="register_teacher_confirm_password"
        )

        st.divider()

        # =====================================
        # LOGIN / REGISTER
        # =====================================

        c1, c2 = st.columns(
            2,
            gap="medium"
        )

        with c1:

            if st.button(
                "Login Instead",
                key="register_login",
                use_container_width=True
            ):

                st.session_state.teacher_login_type = "login"

                st.rerun()

        with c2:

            if st.button(
                "Register",
                key="register_home",
                use_container_width=True
            ):

                success, message = register_teacher(
                    teacher_username,
                    teacher_name,
                    teacher_password,
                    teacher_confirm_password
                )

                if success:

                    st.success(
                        message
                    )

                    import time

                    time.sleep(2)

                    st.session_state.teacher_login_type = "login"

                    st.rerun()

                else:

                    st.error(
                        message
                    )