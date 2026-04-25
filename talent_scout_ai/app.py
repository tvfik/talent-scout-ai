import streamlit as st
from talent_scout_ai.crew import TalentScoutAi

st.set_page_config(page_title="AI Talent Scout", layout="wide")
st.title("🕵️‍♂️ AI-Powered Talent Scout & Engagement")

jd_input = st.text_area("Paste the Job Description here:")

if st.button("Start Scouting"):
    if jd_input:
        with st.spinner("Agents are scouting and engaging candidates..."):
            # This triggers your CrewAI logic
            result = TalentScoutAi().crew().kickoff(inputs={'job_description': jd_input})
            st.markdown("### 📊 Final Ranked Shortlist")
            st.markdown(result.raw)
    else:
        st.warning("Please paste a JD first!")