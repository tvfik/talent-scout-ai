from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool 
import pandas as pd
import os

@tool("candidate_search_tool")
def candidate_search_tool(query: str):
    """Searches the candidates.csv file and returns all candidate details."""
    try:
        # Getting to the path to the current folder where THIS file lives
        current_dir = os.path.dirname(os.path.abspath(__file__))
        #Going up two levels to reach the root folder (where candidates.csv is)
        # From: talent_scout_ai/src/talent_scout_ai/crew.py
        # To: talent_scout_ai/candidates.csv
        root_dir = os.path.dirname(os.path.dirname(os.path.dirname(current_dir)))
        csv_path = os.path.join(root_dir, 'candidates.csv')
        if not os.path.exists(csv_path):
            csv_path = 'candidates.csv'
        df = pd.read_csv(csv_path)
        return df.to_string()
    except Exception as e:
        return f"Error reading CSV: {e}"

@CrewBase
class TalentScoutAi():
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self):
        self.gemini_llm = LLM(
            model="gemini/gemini-2.5-flash",
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
        )