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

    @start
    def start(self) -> ReportState:
        return ReportState()


def kickoff():
    report_flow = ReportFlow()
    report_flow.kickoff()


def plot():
    report_flow = ReportFlow()
    report_flow.plot()


if __name__ == "__main__":
    kickoff()
