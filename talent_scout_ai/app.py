import streamlit as st
import pandas as pd
import os
import json
import re
from talent_scout_ai.crew import TalentScoutAi

# 1. Page Config (Must be first)
st.set_page_config(page_title="Talent Scouter", layout="wide", page_icon="🕵️‍♂️")

# 2. Session State Initialization
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "results" not in st.session_state:
    st.session_state.results = None

# 3. CSS Styling (Exact Pinpoint aesthetics + Sidebar Navigation + Overlap Fixes)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Ovo&family=Inter:wght@400;600;800&display=swap');

    :root {
        --bg-main: #FAF8F5;
        --sidebar-green: #2F5D4A;
        --text-dark: #3D2D1B;
        --border-cream: #EAE0D3;
    }

    .main { background-color: var(--bg-main) !important; }

    /* Sidebar Navigation Styling */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-green) !important;
        min-width: 250px !important;
    }
    
    /* Talent Scouter Logo Text */
    .sidebar-logo {
        font-family: 'Ovo', serif !important;
        color: #F8F4EF !important;
        font-size: 2.2rem;
        padding: 1rem 0;
        text-align: center;
        margin-bottom: 2rem;
    }

    /* Sidebar Buttons (Menu Items) */
    .stSidebar [data-testid="stVerticalBlock"] .stButton button {
        background-color: transparent !important;
        color: #F8F4EF !important;
        border: none !important;
        text-align: left !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1.1rem !important;
        padding: 0.5rem 1rem !important;
        width: 100% !important;
        display: block !important;
        transition: 0.2s;
    }
    
    .stSidebar [data-testid="stVerticalBlock"] .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #4CB5A6 !important;
    }

    /* Main Content Headers */
    .main-header {
        font-family: 'Ovo', serif !important;
        font-size: 3rem;
        color: var(--text-dark);
        margin-bottom: 2rem;
    }

    /* Fix File Uploader Overlap */
    [data-testid="stFileUploader"] {
        border: 1px solid var(--border-cream);
        border-radius: 8px;
        background: white;
        padding: 10px;
    }
    [data-testid="stFileUploaderContent"] { padding: 0 !important; }

    /* Cards and Containers */
    [data-testid="stExpander"] {
        background-color: white !important;
        border: 1px solid var(--border-cream) !important;
        border-radius: 8px !important;
        margin-bottom: 1rem !important;
    }

    /* LinkedIn Button Styling */
    .ln-button {
        display: inline-flex;
        align-items: center;
        padding: 8px 16px;
        background-color: #0077B5;
        color: white !important;
        border-radius: 4px;
        text-decoration: none;
        font-weight: 600;
        font-size: 0.9rem;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. Sidebar Navigation
with st.sidebar:
    st.markdown('<div class="sidebar-logo">Talent Scouter</div>', unsafe_allow_html=True)
    
    if st.button("📊 Dashboard"):
        st.session_state.page = "Dashboard"
    if st.button("👥 Candidates"):
        st.session_state.page = "Candidates"
    
    st.divider()
    st.caption("v2.5 Flash-Lite Engine")

# 5. Page: Dashboard (Main Scouting Interface)
if st.session_state.page == "Dashboard":
    st.markdown('<div class="main-header">Candidate Survey Insights</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.3], gap="large")

    with col1:
        with st.container(border=True):
            st.subheader("👥 Database Upload")
            uploaded_file = st.file_uploader("Upload CSV", type="csv")
            if uploaded_file:
                df = pd.read_csv(uploaded_file)
                st.success("Loaded")
                if not os.path.exists("talent_scout_ai"): os.makedirs("talent_scout_ai")
                df.to_csv("talent_scout_ai/candidates.csv", index=False)

    with col2:
        with st.container(border=True):
            st.subheader("📋 Job Requirements")
            jd_input = st.text_area("Paste JD here:", height=200)
            run_btn = st.button("🚀 Rank Candidates")

    if run_btn and jd_input and uploaded_file:
        with st.status("🔍 Analyzing...", expanded=True) as status:
            try:
                crew_instance = TalentScoutAi().crew()
                result = crew_instance.kickoff(inputs={'job_description': jd_input})
                
                # Attempt to parse JSON from the model's output
                raw_output = result.raw
                json_match = re.search(r'\[.*\]', raw_output, re.DOTALL)
                if json_match:
                    st.session_state.results = json.loads(json_match.group())
                else:
                    st.error("Model output was not in the expected format. Check tasks.yaml.")
                
                status.update(label="Complete!", state="complete")
            except Exception as e:
                st.error(f"Error: {e}")

    # Display Results
    if st.session_state.results:
        st.divider()
        st.markdown("### 🏆 Top Matches")
        st.info("Click a name to view detailed reasoning and LinkedIn profile.")
        
        for candidate in st.session_state.results:
            with st.expander(f"👤 {candidate['name']}"):
                c_col1, c_col2 = st.columns([2, 1])
                
                with c_col1:
                    st.markdown(f"**Overview:** {candidate['overview']}")
                    st.markdown(f"**Tech Skills:** {candidate['tech_skills']}")
                    st.markdown(f"**Experience:** {candidate['experience']}")
                    st.markdown(f"**Motivation:** {candidate['motivation']}")
                
                with c_col2:
                    # LinkedIn Button with Logo
                    ln_url = candidate.get('linkedin_url', '#')
                    st.markdown(f"""
                        <a href="{ln_url}" target="_blank" class="ln-button">
                            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="20" style="margin-right:8px;">
                            View LinkedIn Profile
                        </a>
                    """, unsafe_allow_html=True)

# 6. Page: Candidates (CSV Viewer)
elif st.session_state.page == "Candidates":
    st.markdown('<div class="main-header">Candidate Database</div>', unsafe_allow_html=True)
    if os.path.exists("talent_scout_ai/candidates.csv"):
        full_df = pd.read_csv("talent_scout_ai/candidates.csv")
        st.dataframe(full_df, use_container_width=True)
    else:
        st.warning("No database found. Please upload one in the Dashboard.")