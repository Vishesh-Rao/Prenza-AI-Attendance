import streamlit as st
import base64
from pathlib import Path


def header_home():

    # =====================================================
    # PROJECT ROOT
    # =====================================================

    project_root = Path(__file__).resolve().parents[2]

    logo_path = project_root / "assets" / "graduation-cap.png"


    # =====================================================
    # READ LOGO
    # =====================================================

    with open(logo_path, "rb") as f:
        logo = base64.b64encode(f.read()).decode()


    # =====================================================
    # HEADER
    # =====================================================

    st.html(
        f"""
        <style>

        .prenza-header {{

            position: fixed;

            top: 0;
            left: 0;
            right: 0;

            height: 44px;

            background: #071020;

            border-bottom:
                1px solid #24344c;

            display: flex;

            align-items: center;

            padding-left: 16px;

            box-sizing: border-box;

            z-index: 999999;
        }}


        .prenza-header-content {{

            display: flex;

            align-items: center;

            gap: 9px;
        }}


        .prenza-logo {{

            width: 20px;

            height: 20px;

            object-fit: contain;
        }}


        .prenza-title {{

            color: #67e8f9;

            font-family:
                Inter,
                Arial,
                sans-serif;

            font-size: 16px;

            font-weight: 600;

            white-space: nowrap;
        }}

        </style>


        <div class="prenza-header">

            <div class="prenza-header-content">

                <img
                    class="prenza-logo"
                    src="data:image/png;base64,{logo}"
                >

                <span class="prenza-title">
                    Prenza Attendance
                </span>

            </div>

        </div>
        """
    )