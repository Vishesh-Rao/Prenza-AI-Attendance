import streamlit as st


def style_background_home():

    st.html(
        """
        <style>

        /* =====================================================
           FONT
        ===================================================== */

        @import url(
            'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap'
        );


        /* =====================================================
           REMOVE STREAMLIT DEFAULT UI
        ===================================================== */

        #MainMenu,
        footer,
        header {

            display: none !important;

            visibility: hidden !important;
        }


        [data-testid="stHeader"] {

            display: none !important;
        }


        [data-testid="stToolbar"] {

            display: none !important;
        }


        [data-testid="stDecoration"] {

            display: none !important;
        }


        /* =====================================================
           BODY
        ===================================================== */

        html,
        body {

            margin: 0 !important;

            padding: 0 !important;

            background: #081224 !important;
        }


        [data-testid="stAppViewContainer"] {

            background: #081224 !important;
        }


        [data-testid="stApp"] {

            background: #081224 !important;
        }


        .stApp {

            background:

                radial-gradient(
                    circle at 50% 20%,
                    rgba(20, 50, 80, 0.30),
                    transparent 45%
                ),

                #081224 !important;

            min-height: 100vh;
        }


        


        /* =====================================================
           PURPLE BOTTOM LINE
        ===================================================== */

        .stApp::after {

            content: "";

            position: fixed;

            left: 0;

            right: 0;

            bottom: 0;

            height: 3px;

            background: #7657ff;

            box-shadow:

                0 0 12px
                rgba(118, 87, 255, 0.8),

                0 0 25px
                rgba(118, 87, 255, 0.3);

            z-index: 999999;
        }


        /* =====================================================
           MAIN CONTAINER
        ===================================================== */

        .block-container {

            max-width: 1040px !important;

            padding-top: 105px !important;

            padding-bottom: 80px !important;

            padding-left: 20px !important;

            padding-right: 20px !important;

            margin: 0 auto !important;
        }


        /* =====================================================
           STREAMLIT COLUMNS
        ===================================================== */

        [data-testid="column"] {

            overflow: visible !important;
        }


        /* =====================================================
           BUTTON WRAPPER
        ===================================================== */

        .stButton {

            width: auto !important;

            margin-top: 14px !important;

            margin-bottom: 0 !important;

            display: flex !important;

            justify-content: flex-start !important;
        }


        /* =====================================================
           BUTTON
        ===================================================== */

        .stButton > button {

            width: auto !important;

            min-width: 0 !important;

            height: 30px !important;

            min-height: 30px !important;

            padding:
                0 13px !important;

            background: #12d8e8 !important;

            color: #05212a !important;

            border: none !important;

            border-radius: 5px !important;

            font-family:
                'JetBrains Mono',
                monospace !important;

            font-size: 7px !important;

            font-weight: 600 !important;

            white-space: nowrap !important;

            box-shadow: none !important;

            transition:
                transform 0.2s ease,
                background 0.2s ease,
                box-shadow 0.2s ease !important;
        }


        .stButton > button:hover {

            background: #35e5f3 !important;

            color: #05212a !important;

            transform: translateY(-1px) !important;

            box-shadow:
                0 0 15px
                rgba(18, 216, 232, 0.35) !important;
        }


        /* =====================================================
           MOBILE
        ===================================================== */

        @media (max-width: 768px) {

            .block-container {

                padding-left: 16px !important;

                padding-right: 16px !important;

                padding-top: 90px !important;
            }

        }

        </style>
        """
    )

    





def style_background_teacher():

    st.markdown(
        """
        <style>

        @import url(
            'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap'
        );


        /* ==============================
           HIDE STREAMLIT UI
        ============================== */

        #MainMenu,
        footer,
        header {
            visibility: hidden !important;
        }

        [data-testid="stHeader"] {
            display: none !important;
        }

        [data-testid="stToolbar"] {
            display: none !important;
        }

        [data-testid="stDecoration"] {
            display: none !important;
        }


        /* ==============================
           BACKGROUND
        ============================== */

        .stApp {

            background:
                radial-gradient(
                    circle at 50% 20%,
                    rgba(20, 50, 80, 0.30),
                    transparent 45%
                ),
                #081224 !important;

            min-height: 100vh;
        }


       

        /* ==============================
           BOTTOM LINE
        ============================== */

        .stApp::after {

            content: "";

            position: fixed;

            left: 0;
            right: 0;
            bottom: 0;

            height: 3px;

            background: #7657ff;

            box-shadow:
                0 0 12px rgba(118, 87, 255, 0.8),
                0 0 25px rgba(118, 87, 255, 0.3);

            z-index: 999999;
        }


        /* ==============================
           MAIN CONTAINER
        ============================== */

        .block-container {

            max-width: 1200px !important;

            padding-top: 70px !important;

            padding-bottom: 60px !important;

            padding-left: 40px !important;

            padding-right: 40px !important;
        }


        /* ==============================
           LOGIN TITLE
        ============================== */

        .teacher-register-title {

            text-align: center;

            font-family: 'Inter', sans-serif;

            font-size: 34px;

            font-weight: 700;

            line-height: 1.2;

            color: #f0f4ff;

            margin-top: 5px;

            margin-bottom: 55px;
        }


        .teacher-register-title span {

            color: #12d8e8;
        }


        /* ==============================
           INPUT LABEL
        ============================== */

        .stTextInput label {

            font-family: 'Inter', sans-serif !important;

            font-size: 14px !important;

            font-weight: 500 !important;

            color: #f0f4ff !important;
        }


        /* ==============================
           INPUT
        ============================== */

        .stTextInput {

            width: 100% !important;

            margin-bottom: 18px !important;
        }


        .stTextInput input {

            width: 100% !important;

            height: 44px !important;

            min-height: 44px !important;

            background: #24252e !important;

            color: #f0f4ff !important;

            border: 1px solid #303849 !important;

            border-radius: 6px !important;

            padding: 0 14px !important;

            box-sizing: border-box !important;

            font-family: 'Inter', sans-serif !important;

            font-size: 14px !important;
        }


        .stTextInput input::placeholder {

            color: #9ba3b4 !important;

            opacity: 1 !important;
        }


        .stTextInput input:focus {

            border-color: #12d8e8 !important;

            box-shadow:
                0 0 0 1px #12d8e8 !important;
        }


        /* ==============================
           DIVIDER
        ============================== */

        hr {

            border-color: #29384d !important;

            margin-top: 30px !important;

            margin-bottom: 32px !important;
        }


        /* ==============================
           BUTTONS
        ============================== */

        .stButton {

            width: 100% !important;
        }


        .stButton > button {

            width: 100% !important;

            height: 44px !important;

            min-height: 44px !important;

            max-height: 44px !important;

            background: #12d8e8 !important;

            color: #05212a !important;

            border: none !important;

            border-radius: 6px !important;

            padding: 0 !important;

            margin: 0 !important;

            font-family: 'Inter', sans-serif !important;

            font-size: 14px !important;

            font-weight: 600 !important;

            box-sizing: border-box !important;
        }


        .stButton > button:hover {

            background: #35e5f3 !important;

            color: #05212a !important;

            transform: translateY(-1px) !important;

            box-shadow:
                0 0 15px rgba(18, 216, 232, 0.35) !important;
        }


        /* ==============================
           RESPONSIVE
        ============================== */

        @media (max-width: 768px) {

            .block-container {

                padding-left: 20px !important;

                padding-right: 20px !important;
            }

            .teacher-register-title {

                font-size: 28px;

                margin-bottom: 40px;
            }
        }

        </style>
        """,
        unsafe_allow_html=True
    )