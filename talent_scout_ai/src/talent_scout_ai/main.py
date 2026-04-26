import sys
import os
from talent_scout_ai.crew import TalentScoutAi

def run():
    """
    Run the crew to scout candidates based on a Job Description.
    """
    jd=input("Enter job description: ")
    count=int(input("How many candidates to shortlist?: "))
    inputs = {
        'job_description': jd,
        'limit': count
    }
    
    try:
        # This starts the agentic process
        result = TalentScoutAi().crew().kickoff(inputs=inputs)
        print("\n\n########################")
        print("## FINAL RANKED REPORT ##")
        print("########################\n")
        print(result)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()