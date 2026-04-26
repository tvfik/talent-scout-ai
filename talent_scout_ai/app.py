import streamlit as st
import pandas as pd
import os
from talent_scout_ai.crew import TalentScoutAi

# 1. Page Config MUST be the very first Streamlit command
st.set_page_config(page_title="AI Talent Scout", layout="wide", page_icon="🕵️‍♂️")

# 2. Modern CSS Injection (Modern Buttons & Clean Cards)
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background-color: #007bff;
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #0056b3;
        color: white;
    }
    .main-header {
        font-size: 2.5rem;
        font-weight: 800;
        color: #1E1E1E;
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar - Project Info & Status
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1904/1904425.png", width=100)
    st.title("TalentScout v2.0")
    st.info("System Status: Online (Gemma 4 31B)")
    st.divider()
    st.markdown("Developed by: **Toufik Jamal Mondal**")

# 4. Main UI Layout
st.markdown('<div class="main-header">🕵️‍♂️ AI-Powered Talent Scout</div>', unsafe_allow_html=True)

# Use columns to separate Data Input and JD Input
col1, col2 = st.columns([1, 1.5], gap="large")

with col1:
    with st.container(border=True):
        st.subheader("👥 Candidate Database")
        uploaded_file = st.file_uploader("Upload Candidates CSV", type="csv")

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("Database Loaded!")
            st.dataframe(df.head(5), use_container_width=True)
            
            # Save the file for the Crew agents to find
            # Ensure the folder exists
            if not os.path.exists("talent_scout_ai"):
                os.makedirs("talent_scout_ai")
            
            save_path = os.path.join("talent_scout_ai", "candidates.csv")
            df.to_csv(save_path, index=False)
        else:
            st.warning("Waiting for CSV upload...")

with col2:
    with st.container(border=True):
        st.subheader("📋 Job Requirements")
        jd_input = st.text_area("Paste the Job Description here:", height=250, 
                               placeholder="Enter responsibilities, skills, and experience...")
        
        run_button = st.button("🚀 Start Scouting & Ranking")

# 5. Execution Logic
if run_button:
    if not uploaded_file:
        st.error("Please upload a candidate CSV first!")
    elif not jd_input:
        st.error("Please provide a Job Description!")
    else:
        # Using a nice status box for "Chain of Thought" visibility
        with st.status("🕵️ Agents are working...", expanded=True) as status:
            st.write("Analysing Job Description...")
            try:
                # The CrewAI logic
                crew_instance = TalentScoutAi().crew()
                result = crew_instance.kickoff(inputs={'job_description': jd_input})
                
                status.update(label="Scouting Complete!", state="complete", expanded=False)
                
                # Display Results in a clean card
                st.divider()
                st.balloons()
                st.markdown("### 🏆 Final Ranked Shortlist")
                st.markdown(result.raw)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
                status.update(label="Execution Failed", state="error")