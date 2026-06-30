TalentScout AI: 

TalentScout AI is an autonomous multi-agent system designed to automate the grueling process of candidate discovery and engagement. Built for the 2026 Deccan AI Hackathon, it moves beyond simple keyword matching by using Generative AI to simulate candidate interactions and assess genuine interest.

The Problem:  
Recruiters spend roughly 60% of their time sifting through resumes and chasing passive candidates. Traditional ATS (Applicant Tracking Systems) often miss the "human" context within a profile.

💡 The Solution
Using CrewAI and Google Gemini 3.1 Flash, this project deploys a crew of three specialized agents that act as a virtual recruiting team:
JD Analyst: Extracts technical requirements and "must-have" skills from raw Job Descriptions.Candidate Scout: Performs intelligent semantic matching against a candidate database (candidates.csv).
Engagement Recruiter: Simulates a conversational outreach to gauge interest and provides a final ranked shortlist.

🏗️ Architecture & Logic
The system follows a sequential agentic workflow:
Scoring Dimensions:
Match Score (0-10): Calculated by the Scout agent based on skill overlap, experience level, and biographical relevance.
Interest Score (0-10): Calculated by the Engagement agent via simulated persona-based outreach.
Final Cumulative Score (0-20): Calculated by Engagement recruiter via a simple formula [Match score *0.7 + Interest Score *0.3]
MINIMUM ELIGIBILITY CRITERIA/THRESHOLD: Match score & Interest score must be 3/10 or more

🛠️ Tech StackLLM: 
Google Gemini 3.1 Flash Lite
Framework: CrewAI (Agentic Orchestration)
Frontend: StreamlitData 
Handling: PandasEnvironment: Python 3.12, 
UV (Package Manager)
Used Cursor as IDE and gemini AI for help in creating this application

📥 Local Setup
1. Clone the repository: git clone https://github.com/tvfik/talent-scout-ai.git
2. Set up Environment Variables: Create a .env file in the root directory: GOOGLE_API_KEY=your_gemini_api_key_here 
3. .env file is also provided in files, except gemini key is redacted. please use your own gemini key and run the code
4. open terminal/bash/shell
5. Install Dependencies:If using uv (recommended): uv sync
Or using pip: pip install -r requirements.txt
6. type: cd talent_scout_ai
7. then type: crewai run

! Online link ! (easy, no setup, instant execution): [The link has been hidden due to API usage limit restrictions]
