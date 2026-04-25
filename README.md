🕵️‍♂️ TalentScout AI: Agentic Recruitment Pipeline

TalentScout AI is an autonomous multi-agent system designed to automate the grueling process of candidate discovery and engagement. Built for the 2026 Deccan AI Hackathon, it moves beyond simple keyword matching by using Generative AI to simulate candidate interactions and assess genuine interest.

🚀 The Problem
Recruiters spend roughly 60% of their time sifting through resumes and chasing passive candidates. Traditional ATS (Applicant Tracking Systems) often miss the "human" context within a profile.

💡 The Solution
Using CrewAI and Google Gemini 2.5 Flash, this project deploys a crew of three specialized agents that act as a virtual recruiting team:JD Analyst: Extracts technical requirements and "must-have" skills from raw Job Descriptions.Candidate Scout: Performs intelligent semantic matching against a candidate database (candidates.csv).Engagement Recruiter: Simulates a conversational outreach to gauge interest and provides a final ranked shortlist.

🏗️ Architecture & Logic
The system follows a sequential agentic workflow:Scoring DimensionsMatch Score (0-10): Calculated by the Scout agent based on skill overlap, experience level, and biographical relevance.Interest Score (0-10): Calculated by the Engagement agent via simulated persona-based outreach.

🛠️ Tech StackLLM: 
Google Gemini 2.5 FlashFramework: CrewAI (Agentic Orchestration)Frontend: StreamlitData Handling: PandasEnvironment: Python 3.12, UV (Package Manager)

📥 Local Setup
1. Clone the repository: git clone https://github.com/tvfik/talent-scout-ai.git
cd talent_scout_ai
2. Set up Environment Variables: Create a .env file in the root directory:GOOGLE_API_KEY=your_gemini_api_key_here
3. Install Dependencies:If using uv (recommended):uv sync
Or using pip: pip install -r requirements.txt
4. Run the App:Bashstreamlit run app.py

🎥 Demo & Submission
Live Prototype: [Insert your Streamlit Cloud Link Here]
Demo Video: [Insert your Loom/YouTube Link Here]
Developer: Toufik Jamal Mondal (BTech ECE, 2nd Year)

How to use this:
1. In Cursor, create/open README.md.
2. Delete everything currently inside it.
3. Paste the content above.
4. Edit the placeholders (like the GitHub URL and Demo Link) with your actual links.
5. Save, Commit, and Push.