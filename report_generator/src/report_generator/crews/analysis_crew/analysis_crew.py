from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class AnalysisCrew:
    """Analysis Crew for project analysis and structuring"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def project_analyzer(self) -> Agent:
        return Agent(
            config=self.agents_config["project_analyzer"],  # type: ignore[index]
        )

    @agent
    def outline_creator(self) -> Agent:
        return Agent(
            config=self.agents_config["outline_creator"],  # type: ignore[index]
        )

    @task
    def analyze_project_task(self) -> Task:
        return Task(
            config=self.tasks_config["analyze_project_task"],  # type: ignore[index]
            agent=self.project_analyzer(),
            output_file='output/project_analysis.json',
        )
        
    @task
    def create_outline_task(self) -> Task:
        return Task(
            config=self.tasks_config["create_outline_task"],  # type: ignore[index]
            agent=self.outline_creator(),
            context=[self.analyze_project_task()],
            output_file='output/detailed_outline.json',
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Analysis Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
