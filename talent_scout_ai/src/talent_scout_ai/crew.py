from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool 
import pandas as pd
import os

@tool("candidate_search_tool")
def candidate_search_tool(query: str):
    """Searches the candidates.csv file and returns all candidate details."""
    # This is the path based on your GitHub structure
    target_file = 'talent_scout_ai/candidates.csv'
    # Fallback for local testing (in case you are already inside the folder)
    if not os.path.exists(target_file):
        target_file = 'candidates.csv'
    try:
        if os.path.exists(target_file):
            df = pd.read_csv(target_file)
            return df.to_string()
        else:
            # Debugging: This helps us see what Streamlit sees
            return f"Error: File not found at {target_file}. Current directory: {os.getcwd()}, Contents: {os.listdir()}"
    except Exception as e:
        return f"Error reading CSV: {e}"

@CrewBase
class TalentScoutAi():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        #selected_model="gemini/gemini-3.1-flash-lite"
        selected_model="gemini/gemma-4-31b-it"
        self.gemini_llm = LLM(
            model=selected_model,
            api_key=os.getenv("GOOGLE_API_KEY")
        )

    @agent
    def jd_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['jd_analyst'],
            llm=self.gemini_llm,
            verbose=True
        )

    @agent
    def candidate_scout(self) -> Agent:
        return Agent(
            config=self.agents_config['candidate_scout'],
            tools=[candidate_search_tool], # Use our new custom tool here
            llm=self.gemini_llm,
            verbose=True
        )

    @agent
    def engagement_recruiter(self) -> Agent:
        return Agent(
            config=self.agents_config['engagement_recruiter'],
            llm=self.gemini_llm,
            verbose=True
            max_iter=4,
        )

    @task
    def analyze_jd_task(self) -> Task:
        return Task(config=self.tasks_config['analyze_jd_task'])

    @task
    def scout_candidates_task(self) -> Task:
        return Task(config=self.tasks_config['scout_candidates_task'])

    @task
    def engage_candidates_task(self) -> Task:
        return Task(config=self.tasks_config['engage_candidates_task'])

    @task
    def final_ranking_task(self) -> Task:
        return Task(config=self.tasks_config['final_ranking_task'])

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
            max_rpm=10
        )