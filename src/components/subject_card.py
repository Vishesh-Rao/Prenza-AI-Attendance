import streamlit as st


def subject_card(name, code, section, stats=None, footer_callback=None):

    html = f"""
<div style="
    background: #1A2435;
    border-left: 8px solid #EB459E;
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #3f4654;
    margin-bottom: 20px;
">

    <h3 style="
        margin: 0;
        color: #f0f4ff;
        font-size: 1.5rem;
        font-family: 'Inter', sans-serif;
    ">
        {name}
    </h3>

    <p style="
        color: #f0f4ff;
        margin: 10px 0 20px 0;
        font-family: 'Inter', sans-serif;
        font-size: 14px;
    ">
        Code:
        <span style="
            background: #E0E3FF;
            color: #5865F2;
            padding: 2px 8px;
            border-radius: 5px;
        ">
            {code}
        </span>

        &nbsp; | &nbsp;

        Section: {section}
    </p>
"""

    if stats:

        html += """
    <div style="
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    ">
"""

        for icon, label, value in stats:

            html += f"""
        <div style="
            background: rgba(235, 69, 158, 0.10);
            padding: 10px 16px;
            border-radius: 12px;
            font-size: 14px;
            color: #f0f4ff;
            font-family: 'Inter', sans-serif;
        ">
            {icon}
            <strong>{value}</strong>
            {label}
        </div>
"""

        html += """
    </div>
"""

    html += """
</div>
"""

    # Render actual HTML
    st.html(html)

    # Render footer/button if provided
    if footer_callback:
        footer_callback()