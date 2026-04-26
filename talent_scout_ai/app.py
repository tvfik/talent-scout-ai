import streamlit as st
import pandas as pd
import os
from talent_scout_ai.crew import TalentScoutAi

# 1. Page Config MUST be the very first Streamlit command
st.set_page_config(page_title="TalentScout AI", layout="wide", page_icon="🕵️‍♂️")

# 2. Comprehensive CSS Styling (Exact replication of Pinpoint aesthetics)
st.markdown("""
    <style>
    /* 1. Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Ovo&family=Inter:wght@400;600&display=swap');

    /* 2. Global Resets */
    .main {
        background-color: #f7f3e7 !important;
    }
    
    /* 3. Sidebar - Force Deep Green & Light Text */
    [data-testid="stSidebar"] {
        background-color: #2F5D4A !important;
    }
    
    /* Force ALL text in sidebar to be off-white */
    [data-testid="stSidebar"] *, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: #F8F4EF !important;
        font-family: 'Inter', sans-serif !important;
    }

    /* 4. Main Header - The Pinpoint Serif Style */
    .main-header {
        font-family: 'Ovo', serif !important;
        font-size: 3rem !important;
        color: #3D2D1B !important;
        margin-bottom: 1.5rem !important;
        padding-top: 1rem;
    }

    /* 5. Fix the File Uploader Overlap */
    /* We need to be careful not to squash the internal upload button */
    [data-testid="stFileUploader"] {
        background-color: #FFFFFF;
        border: 1px dashed #EAE0D3;
        border-radius: 8px;
        padding: 10px;
    }
    
    /* This fixes the 'upload upload' text bug */
    [data-testid="stFileUploader"] section {
        padding: 10px !important;
    }

    /* 6. Clean Card Containers */
    /* We use 'section' because Streamlit wraps columns in section tags */
    [data-testid="stVerticalBlock"] > div > div > div[data-testid="stVerticalBlock"] {
        background-color: #FAF8F5 !important;
        border: 1px solid #EAE0D3 !important;
        padding: 20px !important;
        border-radius: 4px !important;
    }

    /* 7. Subtle Modern Button */
    .stButton>button {
        width: 100%;
        border-radius: 25px !important;
        background-color: #EAE0D3 !important;
        color: #3D2D1B !important;
        font-weight: 600 !important;
        border: 1px solid #DCCFBF !important;
        height: 3.5em !important;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #3D2D1B !important;
        color: #FFFFFF !important;
        border: none !important;
    }

    /* 8. Text Area Styling */
    .stTextArea textarea {
        background-color: #FFFFFF !important;
        border: 1px solid #EAE0D3 !important;
        color: #3D2D1B !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Sidebar - Mimicking the Fixed Narrow Menu from Image
with st.sidebar:
    st.image("https://pinpoint.co/img/favicons/favicon-196x196.png", width=120)
    st.divider()
    # Using placeholder text instead of active components for style-only replication
    st.markdown("### **Menu**")
    st.markdown("Dashboard")
    st.markdown("Jobs")
    st.markdown("Candidates")
    st.markdown("Insights")
    st.markdown("&nbsp;&nbsp;Candidates")
    st.markdown("&nbsp;&nbsp;Team members")
    st.markdown("Company")
    st.markdown("Settings")

    st.divider()
    # User info capsule-style section (mimicking Taylor/Thomas)
    with st.container():
        cols = st.columns([1, 4])
        with cols[0]:
            st.markdown("🧑‍💻")
        with cols[1]:
            st.markdown("**Toufik Mondal**")
            st.markdown("Recruiter")
    
    st.info("System Status: Online (Gemma 4 31B)")

# 4. Main UI Layout
# Manually applying main header class for correct font
st.markdown('<div class="main-header">Candidate Survey Insights</div>', unsafe_allow_html=True)

# Main Card-style container replicating the overall page card in image
with st.container(border=True):
    st.subheader("Key Insights")
    
    # Optional subtle user capsules as in image header area (not functional, just visual)
    col_filters = st.columns([2,2,2,1])
    with col_filters[0]: st.caption("JOB: DESIGN LEAD X")
    with col_filters[1]: st.caption("HIRING MANAGER: TOM X")
    with col_filters[2]: st.caption("HIRING MANAGER: BILL X")
    with col_filters[3]: st.caption("CLEAR FILTERS")
    st.divider()

    # Layout for the main recruitment actions
    # Two main input sections side-by-side as in your previous v2 layout
    col1, col2 = st.columns([1, 1.3], gap="large")

    with col1:
        # Candidate Database Card
        with st.container(border=True):
            st.subheader("👥 Candidate Database")
            uploaded_file = st.file_uploader("Upload Candidates CSV", type="csv")

            if uploaded_file is not None:
                # Need explicit import for pandas if not already here,
                # though it was in your snippet
                import pandas as pd
                df = pd.read_csv(uploaded_file)
                st.success("Database Loaded!")
                # Applying custom card styling for the dataframe container is tough; 
                # keep default but correct width
                st.dataframe(df.head(5), use_container_width=True)
                
                # Save the file for the Crew agents to find
                # Create necessary folders first
                if not os.path.exists("talent_scout_ai"):
                    os.makedirs("talent_scout_ai")
                
                # IMPORTANT path handling for both local and deployed servers
                possible_paths = [
                    os.path.join("talent_scout_ai", "candidates.csv"),
                    os.path.join(os.getcwd(), "talent_scout_ai", "candidates.csv")
                ]
                save_path = possible_paths[0]
                df.to_csv(save_path, index=False)
                
            else:
                st.warning("Waiting for CSV upload...")

    with col2:
        # Job Requirements Card
        with st.container(border=True):
            st.subheader("📋 Job Requirements")
            jd_input = st.text_area("Paste the Job Description here:", height=300, 
                                   placeholder="Enter responsibilities, skills, and experience...",
                                   help="Analyze key skills like RTOS, Microcontrollers, VLSI, Verilog...")
            
            # The button gets our modern subtle cream styling
            run_button = st.button("🚀 Start Scouting & Ranking")

# 5. Execution Logic & Results Display
if run_button:
    if not uploaded_file:
        st.error("Please upload a candidate CSV first!")
    elif not jd_input:
        st.error("Please provide a Job Description!")
    else:
        # Replicating the intermediate logging section from Pinpoint's "LATEST COMMENTS" card
        with st.status("🕵️ Agents are working...", expanded=True) as status:
            log_area = st.empty()
            log_area.write("Initializing Agents...")
            
            try:
                # The CrewAI logic remains unchanged, only the visual container is styled
                log_area.write("Analyzing Job Description for embedded skills...")
                
                # The actual CrewAI execution (using your correct crew call)
                crew_instance = TalentScoutAi().crew()
                result = crew_instance.kickoff(inputs={'job_description': jd_input})
                
                status.update(label="Scouting Complete!", state="complete", expanded=False)
                
                # Display Results in a clean, isolated card as in the main image view
                st.divider()
                st.balloons()
                
                with st.container(border=True):
                    st.markdown("### 🏆 Final Ranked Shortlist")
                    st.markdown("Based on technical skills, interest, and simulated engagement.")
                    st.divider()
                    st.markdown(result.raw)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
                status.update(label="Execution Failed", state="error")