import streamlit as st

from src.screens.home_screen import home_screen
from src.screens.teacher_screen import teacher_screen
from src.screens.student_screen import student_screen

from src.components.dialog_auto_enroll import auto_enroll_dialog




# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Prenza Attendance",
    page_icon="🥈",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# MAIN
# =========================================================

def main():

    # =====================================================
    # INITIALIZE SESSION STATE
    # =====================================================

    if "login_type" not in st.session_state:
        st.session_state["login_type"] = None


    # =====================================================
    # READ JOIN CODE FROM URL
    # =====================================================

    join_code = st.query_params.get("join_code")


    # =====================================================
    # JOIN CODE FOUND
    # =====================================================

    if join_code:

        # Save the join code so it survives reruns
        st.session_state["join_code"] = join_code


        # If student is not already selected,
        # open the student screen
        if st.session_state["login_type"] != "student":

            st.session_state["login_type"] = "student"

            st.rerun()


    # =====================================================
    # SHOW CURRENT SCREEN
    # =====================================================

    match st.session_state["login_type"]:

        case "teacher":

            teacher_screen()


        case "student":

            student_screen()


        case None:

            home_screen()


    # =====================================================
    # AUTO ENROLL
    # =====================================================

    if (
        join_code
        and st.session_state.get("is_logged_in")
        and st.session_state.get("user_role") == "student"
    ):

        auto_enroll_dialog(join_code)


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":
    main()