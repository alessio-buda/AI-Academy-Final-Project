from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from src.report_generator.tools.rag_tool import RagTool

@CrewBase
class WriterCrew():
    """WriterCrew crew - Simplified for RAG search and writing"""

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
        
    @agent
    def rag_searcher(self) -> Agent:
        return Agent(
            config=self.agents_config['rag_searcher'], # type: ignore[index]
            verbose=True,
            tools=[RagTool()],
            allow_delegation=False,
            max_iter=5
        )
        
    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'], # type: ignore[index]
            verbose=True
        )

    @task
    def rag_search_task(self) -> Task:
        return Task(
            config=self.tasks_config['rag_search_task'], # type: ignore[index]
            agent=self.rag_searcher(),
            tools=[RagTool()],
            output_file='output/rag_search_results.md',
        )
        
    @task
    def write_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['write_report_task'], # type: ignore[index]
            agent=self.writer(),
            output_file='output/final_report.md',
            context=[self.rag_search_task()],
        )
        
    @crew
    def crew(self) -> Crew:
        """Creates the WriterCrew crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
