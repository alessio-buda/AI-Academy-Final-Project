from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from src.report_generator.tools.security_tools import (
    SecurityValidationTool,
    PromptInjectionDetectorTool,
    ContentFilterTool
)


@CrewBase
class SanitizeCrew:
    """Sanitize Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]


    agents_config = "config/prompt_protection_agents.yaml"
    tasks_config = "config/prompt_protection_tasks.yaml"


    @agent
    def input_checker(self) -> Agent:
        return Agent(
            config=self.agents_config["input_checker"],  # type: ignore[index]
            tools=[
                SecurityValidationTool(),
                PromptInjectionDetectorTool(),
                ContentFilterTool()
            ],
        )

        
    @agent
    def input_sanitizer(self) -> Agent:
        return Agent(
            config=self.agents_config["input_sanitizer"],  # type: ignore[index]
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def check_input_task(self) -> Task:
        return Task(
            config=self.tasks_config["check_input_task"],  # type: ignore[index]
        )
        
    @task
    def sanitize_input_task(self) -> Task:
        return Task(
            config=self.tasks_config["sanitize_input_task"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Sanitize Crew"""


        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
