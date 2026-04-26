import streamlit as st
import pandas as pd
import os
import json
import re
from talent_scout_ai.crew import TalentScoutAi

# 1. Page Config (Must be the very first command)
st.set_page_config(page_title="Talent Scouter", layout="wide", page_icon="🕵️‍♂️")

# 2. Session State Initialization
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "candidates_df" not in st.session_state:
    st.session_state.candidates_df = None
if "results" not in st.session_state:
    st.session_state.results = None

# 3. Enhanced Pinpoint CSS
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

    /* Sidebar Styles */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-green) !important;
        min-width: 280px !important;
    }
    
    .sidebar-logo {
        font-family: 'Ovo', serif !important;
        color: #F8F4EF !important;
        font-size: 2.2rem;
        padding: 2.5rem 0 1.5rem 1.5rem;
        text-align: left;
    }

    /* Sidebar Navigation Buttons */
    .stSidebar [data-testid="stVerticalBlock"] .stButton button {
        background-color: transparent !important;
        color: #F8F4EF !important;
        border: none !important;
        text-align: left !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 1.1rem !important;
        padding: 0.8rem 1.5rem !important;
        width: 100% !important;
        border-radius: 0px !important;
        transition: 0.3s ease;
    }
    
    .stSidebar [data-testid="stVerticalBlock"] .stButton button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: #4CB5A6 !important;
    }

    /* Headers */
    .main-header {
        font-family: 'Ovo', serif !important;
        font-size: 3rem;
        color: var(--text-dark);
        margin-bottom: 2rem;
    }

    /* Content Containers */
    [data-testid="stExpander"] {
        background-color: white !important;
        border: 1px solid var(--border-cream) !important;
        border-radius: 4px !important;
    }

    /* Static LinkedIn Badge (No Link) */
    .ln-badge-static {
        display: inline-flex;
        align-items: center;
        padding: 8px 16px;
        background-color: #E8F3F9; /* Light blue tint */
        color: #0077B5 !important;
        border-radius: 4px;
        border: 1px solid #B3D7E8;
        font-weight: 600;
        font-size: 0.85rem;
        cursor: default;
        margin-top: 10px;
    }

    /* Standard Button Styling (Subtle Cream) */
    .stButton>button {
        border-radius: 25px !important;
        background-color: #EAE0D3 !important;
        color: #3D2D1B !important;
        font-weight: 600 !important;
        border: none !important;
        height: 3.5em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important; /* Smooth lift */
    }
    .stButton>button:hover {
        background-color: #3D2D1B !important; /* Dark Chocolate */
        color: white !important;
        transform: translateY(-3px) !important; /* Lifts the button up */
        box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important; /* Adds depth shadow */
        border: none !important; }

    </style>
    """, unsafe_allow_html=True)

# 4. Shared File Upload Logic
def handle_upload(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state.candidates_df = df
        if not os.path.exists("talent_scout_ai"):
            os.makedirs("talent_scout_ai")
        df.to_csv("talent_scout_ai/candidates.csv", index=False)
        return True
    return False

# 5. Sidebar Navigation
with st.sidebar:
    st.markdown('<div class="sidebar-logo">Talent Scouter</div>', unsafe_allow_html=True)
    
    if st.button("📊 Dashboard"):
        st.session_state.page = "Dashboard"
    if st.button("👥 View Candidates"):
        st.session_state.page = "View Candidates"
    
    st.divider()
    st.caption("Developed by Toufik Jamal Mondal")
    st.caption("Model in use: Gemini/Gemma 4 31b")

# 6. Page: Dashboard
if st.session_state.page == "Dashboard":
    st.markdown('<div class="main-header">Talent Scouter AI Dashboard</div>', unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.3], gap="large")

    with col1:
        with st.container(border=True):
            st.subheader("Candidate Database")
            up_file = st.file_uploader("Upload CSV", type="csv", key="dash_upload")
            if handle_upload(up_file):
                st.success("Candidate Database Synced")
        st.divider()
        st.subheader("Specify number of Candidates")

        rank_mode=st.radio("Ranking Method: ",["Let me choose","Entire uploaded Database"], horizontal=True)
        if rank_mode=="Let me choose":
            rank_limit=st.number_input("Enter number of candidates to shortlist:", min_value=1,step=1,value=5)
        else:
            if st.session_state.candidates_df is not None:
                rank_limit=len(st.session_state.candidates_df)
                st.caption(f"System will rank all {rank_limit} candidates.")
            else:
                rank_limit=10
                st.caption("Upload a file to see total count.")

    with col2:
        with st.container(border=True):
            st.subheader("📋 Analysis Parameters")
            jd_input = st.text_area("Paste Job Description:", height=200, placeholder="Requirements and skills...")
            run_btn = st.button("Rank Candidates")

    if run_btn:
        if not st.session_state.candidates_df is not None:
            st.error("Please upload the database first.")
        elif not jd_input:
            st.error("Please provide a Job Description.")
        else:
            with st.status(f" Ranking top {rank_limit} Matches...", expanded=True) as status:
                try:
                    crew_instance = TalentScoutAi().crew()
                    result = crew_instance.kickoff(inputs={'job_description': jd_input, 'limit':rank_limit})
                    
                    # Clean the JSON output
                    json_match = re.search(r'\[.*\]', result.raw, re.DOTALL)
                    if json_match:
                        st.session_state.results = json.loads(json_match.group())
                        status.update(label="Analysis Complete", state="complete")
                    else:
                        st.error("Format Error: Ensure tasks.yaml is set to output raw JSON.")
                except Exception as e:
                    st.error(f"Execution Error: {e}")

    # Display Top 5 Rankings
    if st.session_state.results:
        st.divider()
        st.markdown("Top matches found: ")
        actual_count=len(st.session_state.results)
        if actual_count > 0: 
            st.markdown(f"Top {actual_count} matches found: ")
            if actual_count<rank_limit:
                st.warning(f"NOTE: You requested {rank_limit} candidates, but only {actual_count} met the required quality thresholds. The remaining profiles were excluded due to poor compatibility or skill mismatch.")
        else:
            st.info("⚠️ No candidates met the minimum compatibility criteria for this position.")
        for cand in st.session_state.results:
            with st.expander(f"👤 {cand['name']}"):
                c1, c2 = st.columns([2, 1])
                with c1:
                    st.markdown(f"**Overview:** {cand.get('overview', 'N/A')}")
                    st.markdown(f"**Tech Skills:** {cand.get('tech_skills', 'N/A')}")
                    st.markdown(f"**Experience:** {cand.get('experience', 'N/A')}")
                    st.markdown(f"**Motivation:** {cand.get('motivation', 'N/A')}")
                with c2:
                    st.markdown(f"""
                        <div class="ln-badge-static">
                            <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="18" style="margin-right:8px;">
                            Click to view LinkedIn Profile
                        </div>
                    """, unsafe_allow_html=True)

# 7. Page: View Candidates
elif st.session_state.page == "View Candidates":
    st.markdown('<div class="main-header">Candidate Management</div>', unsafe_allow_html=True)
    
    with st.container(border=True):
        st.subheader("📁 View your Candidates List")
        up_file_view = st.file_uploader("Upload CSV to view list", type="csv", key="view_upload")
        handle_upload(up_file_view)

        if st.session_state.candidates_df is not None:
            st.divider()
            st.dataframe(st.session_state.candidates_df, use_container_width=True)
        else:
            st.info("No data available. Please upload a CSV file to view the candidate list.")