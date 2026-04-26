import streamlit as st
import pandas as pd
import os
from talent_scout_ai.crew import TalentScoutAi

# 1. Page Config MUST be the very first Streamlit command
st.set_page_config(page_title="TalentScout AI", layout="wide", page_icon="🕵️‍♂️")

# 2. Comprehensive CSS Styling (Exact replication of Pinpoint aesthetics)
st.markdown("""
    <style>
    /* Google Fonts Injection - Serif for Headers, Sans-Serif for Everything else */
    @import url('https://fonts.googleapis.com/css2?family=Ovo&family=Inter:wght@400;600;800&display=swap');

    /* Color Palette */
    :root {
        --bg-color-main: #FAF8F5; /* Light Cream Main Background */
        --sidebar-bg-color: #2F5D4A; /* Deep Forest Green Sidebar */
        --sidebar-text-main: #F8F4EF; /* Off-white Sidebar Text */
        --main-text-color: #3D2D1B; /* Dark Brownish-Charcoal Headers */
        --body-text-color: #4A4A4A; /* Dark Grey Body Text */
        --button-bg-subtle: #EAE0D3; /* Deep Cream Subtle Button */
        --button-text-subtle: #3D2D1B; /* Dark Text for Subtle Button */
        --accent-teal: #4CB5A6; /* For later use: Progress bar teal */
        --accent-green: #3D8B6D; /* For later use: Promoter green */
        --accent-orange: #FF8F1F; /* For later use: Score orange */
    }

    /* Overall Application Background & Base Typography */
    .main {
        background-color: var(--bg-color-main);
        color: var(--body-text-color);
        font-family: 'Inter', sans-serif !important;
    }

    /* Streamlit's Main Container (including header) */
    [data-testid="stMain"] {
        padding: 4rem 5rem !important; /* Generous padding as seen in image */
    }

    /* Typography Overrides */
    h1, h2 {
        font-family: 'Ovo', serif !important; /* High-end serif for main headers */
        color: var(--main-text-color) !important;
        font-weight: 400 !important;
        margin-bottom: 2rem;
    }
    h3, h4, .subheader {
        font-family: 'Inter', sans-serif !important; /* Modern sans-serif for subheaders */
        color: var(--main-text-color) !important;
        font-weight: 600 !important;
        letter-spacing: 0.5px;
    }
    p, span, div, label {
        font-family: 'Inter', sans-serif !important;
        color: var(--body-text-color);
    }

    /* --- Sidebar Styling (Fixed narrow Green Sidebar) --- */
    [data-testid="stSidebar"] {
        background-color: var(--sidebar-bg-color) !important;
        padding-top: 4rem !important;
        color: var(--sidebar-text-main) !important;
    }

    [data-testid="stSidebarNav"] div[data-testid="stSidebarNavItems"] ul li div {
        color: var(--sidebar-text-main) !important;
    }

    /* Style for Sidebar Text and Items */
    .css-1v3wvcr {
        color: var(--sidebar-text-main);
        font-family: 'Inter', sans-serif;
    }
    [data-testid="stSidebarNav"] * {
        color: var(--sidebar-text-main) !important;
    }

    /* Highlighting active sidebar items (subtle effect) */
    [data-testid="stSidebarNavItems"] .active {
        background-color: #3B755D !important; /* Lighter Green Highlight */
        color: white !important;
        border-radius: 8px;
    }
    
    /* Sidebar user avatar capsule (subtle light grey) */
    [data-testid="stUserAvatarCapsule"] {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border-radius: 20px;
        color: white !important;
    }

    /* --- Main Content Section Styling --- */

    /* Containers (Card-style layout with subtle spacing and borders) */
    [data-testid="stBlock"] {
        background-color: #FAF8F5 !important;
        border-radius: 0px !important;
        border: 1px solid #EAE0D3 !important; /* Subtle border seen on metric cards */
        padding: 2.5rem !important; /* Generous spacing inside cards */
        margin-bottom: 3rem !important; /* Spacing between cards */
        box-shadow: none !important;
    }

    /* Override for nested blocks to prevent recursive borders */
    [data-testid="stBlock"] [data-testid="stBlock"] {
        border: none !important;
        padding: 0px !important;
        margin-bottom: 0px !important;
        background-color: transparent !important;
    }

    /* Text Area Input (Paste JD box) */
    .stTextArea>div>div {
        border: 1px solid #EAE0D3 !important;
        border-radius: 8px !important;
        font-family: 'Inter', sans-serif !important;
        color: var(--body-text-color) !important;
    }

    /* Modern Subtle Button (Rounded and deep cream) */
    .stButton>button {
        width: 100%;
        border-radius: 20px; /* High-end roundedness */
        height: 3.5em;
        background-color: var(--button-bg-subtle) !important; /* Deep cream bg */
        color: var(--button-text-subtle) !important; /* Dark brown text */
        font-family: 'Inter', sans-serif !important;
        font-weight: 600 !important;
        border: none !important;
        transition: 0.3s ease;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background-color: #DCCFBF !important; /* Slightly deeper hover cream */
        color: var(--button-text-subtle) !important;
    }

    /* Metric cards (e.g., matching text color for 43%) */
    [data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif !important;
        color: var(--main-text-color) !important;
        font-weight: 800 !important;
    }
    [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
        color: var(--body-text-color) !important;
    }

    /* Custom main header style to use serif Ovo font */
    .main-header {
        font-family: 'Ovo', serif !important;
        font-size: 3rem;
        font-weight: 400;
        color: var(--main-text-color);
        margin-bottom: 2rem;
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