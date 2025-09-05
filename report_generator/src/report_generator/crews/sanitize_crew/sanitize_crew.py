from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class SanitizeCrew:
    """Sanitize Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]


    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"


    @agent
    def input_checker(self) -> Agent:
        return Agent(
            config=self.agents_config["input_checker"],  # type: ignore[index]

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
            agent=self.input_checker(),  # Assign to input_checker agent
        )
        
    @task
    def sanitize_input_task(self) -> Task:
        return Task(
            config=self.tasks_config["sanitize_input_task"],  # type: ignore[index]
            agent=self.input_sanitizer(),  # Assign to input_sanitizer agent
            context=[self.check_input_task()],  # Depends on check_input_task output
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
