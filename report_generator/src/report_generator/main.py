#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from report_generator.crews.sanitize_crew.sanitize_crew import SanitizeCrew
from report_generator.crews.writer_crew.writer_crew import WriterCrew


class ReportState(BaseModel):
    input: str = ""

class ReportFlow(Flow[ReportState]):

    """A flow that generates a report about CrewAI"""

    @start()
    def get_user_input(self) -> ReportState:
        """Get user input to generate the report."""
        
        print("Starting Report Generation Flow...")
        
        return "ciao"
    
    @listen(get_user_input)
    def write(self, state: ReportState) -> None:
        
        print("Starting WriterCrew...")
        
        result = WriterCrew().crew().kickoff(
                inputs={
                    "project_description": "CrewAI is a framework to build AI applications with LLMs and generative AI.",
                    "outline": "Scelte architetturali, Diagramma della crew, Esempi pratici, Analisi critica.",
                    "audience": "technical",
                }
            )
            
        print("WriterCrew result:", result.raw)
    
    


def kickoff():
    report_flow = ReportFlow()
    report_flow.kickoff()


def plot():
    report_flow = ReportFlow()
    report_flow.plot()


if __name__ == "__main__":
    kickoff()
