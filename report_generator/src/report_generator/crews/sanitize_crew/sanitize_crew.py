from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
"""Sanitize Crew for input validation and sanitization.
This crew is responsible for checking and sanitizing user inputs to ensure
they meet security and quality standards before processing.
Classes:
    SanitizeCrew: Main crew class that orchestrates input sanitization workflow.
Attributes:
    agents (List[BaseAgent]): List of agents automatically created by @agent decorators.
    tasks (List[Task]): List of tasks automatically created by @task decorators.
    agents_config (str): Path to the agents configuration YAML file.
    tasks_config (str): Path to the tasks configuration YAML file.
Methods:
    input_checker() -> Agent:
        Creates an agent responsible for initial input validation.
        Returns:
            Agent: Configured input checker agent that validates incoming data.
    input_sanitizer() -> Agent:
        Creates an agent responsible for sanitizing validated inputs.
        Returns:
            Agent: Configured input sanitizer agent that cleans and formats data.
    check_input_task() -> Task:
        Creates a task for checking input validity and format.
        Returns:
            Task: Task that validates input data using the input_checker agent.
    sanitize_input_task() -> Task:
        Creates a task for sanitizing the checked input data.
        Returns:
            Task: Task that sanitizes input data using the input_sanitizer agent,
                  depends on the output of check_input_task.
    crew() -> Crew:
        Creates and configures the complete sanitization crew.
        Returns:
            Crew: Configured crew with agents and tasks for sequential input
                  sanitization process with verbose logging enabled.
Example:
    >>> sanitize_crew = SanitizeCrew()
    >>> crew = sanitize_crew.crew()
    >>> result = crew.kickoff(inputs={"user_input": "some data"})
"""
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
