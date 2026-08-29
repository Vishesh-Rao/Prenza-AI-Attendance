import streamlit as st
import base64
from pathlib import Path

from src.components.header import header_home
from src.ui.base_layout import style_background_home


# =========================================================
# IMAGE TO BASE64
# =========================================================

def image_to_base64(path):

    with open(path, "rb") as image_file:

        return base64.b64encode(
            image_file.read()
        ).decode()


# =========================================================
# HOME SCREEN
# =========================================================

def home_screen():

    # =====================================================
    # BACKGROUND
    # =====================================================

    style_background_home()


    # =====================================================
    # HEADER
    # =====================================================

    header_home()


    # =====================================================
    # PROJECT ROOT
    # =====================================================

    project_root = Path(__file__).resolve().parents[2]


    # =====================================================
    # LOAD IMAGES
    # =====================================================

    student_logo = image_to_base64(
        project_root / "assets" / "graduation-cap.png"
    )


    teacher_logo = image_to_base64(
        project_root / "assets" / "shield-lock.png"
    )


    # =====================================================
    # PAGE CSS
    # =====================================================

    st.html(
        """
        <style>

        /* =================================================
           MAIN
        ================================================= */

        .prenza-home {

            width: 100%;

            text-align: center;

            font-family:
                Inter,
                Arial,
                sans-serif;
        }


        /* =================================================
           SYSTEM INITIALIZATION
        ================================================= */

        .system-initialization {

            text-align: center;

            font-family:
                'JetBrains Mono',
                monospace;

            font-size: 8px;

            font-weight: 500;

            letter-spacing: 3px;

            color: #35e6b2;

            margin: 0 0 10px 0;

            padding: 0;
        }


        /* =================================================
           TITLE
        ================================================= */

        .main-title {

            text-align: center;

            font-family:
                Inter,
                Arial,
                sans-serif;

            font-size: 30px;

            font-weight: 700;

            line-height: 1.2;

            color: #f0f4ff;

            margin: 0;

            padding: 0;
        }


        /* =================================================
           DESCRIPTION
        ================================================= */

        .main-description {

            max-width: 560px;

            margin:
                12px auto 48px auto;

            text-align: center;

            font-family:
                Inter,
                Arial,
                sans-serif;

            font-size: 9px;

            line-height: 1.6;

            color: #9aabc1;
        }


        /* =================================================
           PORTAL CARD
        ================================================= */

        .portal-card {

            position: relative;

            width: 100%;

            height: 225px;

            padding: 18px;

            box-sizing: border-box;

            background:
                linear-gradient(
                    145deg,
                    #101f34,
                    #09192c
                );

            border:
                1px solid #29415d;

            border-radius: 9px;

            box-shadow:
                0 8px 30px
                rgba(0, 0, 0, 0.18);

            text-align: left;
        }


        /* =================================================
           ID
        ================================================= */

        .portal-id {

            position: absolute;

            top: 18px;

            right: 18px;

            padding:
                5px 9px;

            background:
                #18273b;

            border:
                1px solid #31435a;

            border-radius: 10px;

            color:
                #a4b3c8;

            font-family:
                'JetBrains Mono',
                monospace;

            font-size: 6px;

            white-space: nowrap;
        }


        /* =================================================
           ICON
        ================================================= */

        .portal-icon-box {

            width: 36px;

            height: 36px;

            border-radius: 7px;

            background: #1c2b40;

            display: flex;

            align-items: center;

            justify-content: center;

            margin-bottom: 20px;
        }


        .portal-icon {

            width: 21px;

            height: 21px;

            object-fit: contain;

            filter: brightness(0) saturate(100%)
            invert(83%)
            sepia(8%)
            saturate(270%)
            hue-rotate(145deg)
            brightness(88%)
            contrast(88%);
        }


        /* =================================================
           TITLE
        ================================================= */

        .portal-card-title {

            font-family:
                Inter,
                Arial,
                sans-serif;

            font-size: 17px;

            font-weight: 600;

            color: #e5ebfa;

            margin:
                0 0 7px 0;
        }


        /* =================================================
           DESCRIPTION
        ================================================= */

        .portal-card-description {

            font-family:
                Inter,
                Arial,
                sans-serif;

            font-size: 8.5px;

            line-height: 1.65;

            color: #9caabd;

            max-width: 330px;

            min-height: 43px;
        }


        /* =================================================
           DIVIDER
        ================================================= */

        .card-divider {

            position: absolute;

            left: 18px;

            right: 18px;

            bottom: 42px;

            height: 1px;

            background: #304057;
        }


        /* =================================================
           STATUS
        ================================================= */

        .system-status-wrapper {

            width: 100%;

            display: flex;

            justify-content: center;

            margin-top: 70px;
        }


        .system-status {

            display: flex;

            align-items: center;

            justify-content: center;

            gap: 13px;

            padding:
                8px 17px;

            background:
                rgba(10, 24, 42, 0.85);

            border:
                1px solid #293b53;

            border-radius: 7px;

            color:
                #8798ae;

            font-family:
                'JetBrains Mono',
                monospace;

            font-size: 6.5px;

            white-space: nowrap;
        }


        .status-online {

            color:
                #36e5b1;
        }


        .separator {

            color:
                #3a4a60;
        }


        /* =================================================
           MOBILE
        ================================================= */

        @media (max-width: 768px) {

            .main-title {

                font-size: 26px;
            }


            .main-description {

                margin-bottom: 30px;
            }


            .portal-card {

                height: 225px;
            }


            .system-status {

                font-size: 5.5px;

                gap: 8px;

                padding:
                    7px 10px;
            }
        }

        </style>
        """
    )


    # =====================================================
    # PAGE HEADER
    # =====================================================

    st.html(
        """
        <div class="prenza-home">

            <div class="system-initialization">
                SYSTEM INITIALIZATION
            </div>

            <div class="main-title">
                Select Your Portal
            </div>

            <div class="main-description">
                Please choose your operational domain to access
                the appropriate biometric interface and
                attendance modules.
            </div>

        </div>
        """
    )


    # =====================================================
    # COLUMNS
    # =====================================================

    col1, col2 = st.columns(
        2,
        gap="medium"
    )


    # =====================================================
    # STUDENT PORTAL
    # =====================================================

    with col1:

        st.html(
            f"""
            <div class="portal-card">

                <div class="portal-id">
                    ID: STU-001
                </div>


                <div class="portal-icon-box">

                    <img
                        class="portal-icon"
                        src="data:image/png;base64,{student_logo}"
                    >

                </div>


                <div class="portal-card-title">
                    Student Portal
                </div>


                <div class="portal-card-description">
                    Access your personal attendance records,
                    view class schedules, and manage biometric
                    face registry settings.
                </div>


                <div class="card-divider"></div>

            </div>
            """
        )


        # Real Streamlit button

        if st.button(
            "ENTER STUDENT PORTAL  →",
            key="student_portal"
        ):

            st.session_state["login_type"] = "student"

            st.rerun()


    # =====================================================
    # TEACHER PORTAL
    # =====================================================

    with col2:

        st.html(
            f"""
            <div class="portal-card">

                <div class="portal-id">
                    ID: FAC-001
                </div>


                <div class="portal-icon-box">

                    <img
                        class="portal-icon"
                        src="data:image/png;base64,{teacher_logo}"
                    >

                </div>


                <div class="portal-card-title">
                    Teacher Portal
                </div>


                <div class="portal-card-description">
                    Manage live attendance feeds,
                    review class analytics, and oversee
                    student biometric verification logs.
                </div>


                <div class="card-divider"></div>

            </div>
            """
        )


        # Real Streamlit button

        if st.button(
            "ENTER TEACHER PORTAL  →",
            key="teacher_portal"
        ):

            st.session_state["login_type"] = "teacher"

            st.rerun()


   