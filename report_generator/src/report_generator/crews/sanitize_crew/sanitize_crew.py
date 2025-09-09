from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class SanitizeCrew:
    """A CrewAI-based crew for sanitizing and checking user inputs.
    
    This class implements a multi-agent system designed to validate and sanitize
    user inputs before processing. It consists of two agents: an input checker 
    that validates input security and an input sanitizer that cleans the input.
    
    Attributes:
        agents (List[BaseAgent]): List of agents automatically populated by 
            the @agent decorator.
        tasks (List[Task]): List of tasks automatically populated by the 
            @task decorator.
        agents_config (str): Path to the agents configuration YAML file.
        tasks_config (str): Path to the tasks configuration YAML file.
    
    Examples:
        >>> crew = SanitizeCrew()
        >>> result = crew.crew().kickoff(inputs={"user_input": "SELECT * FROM users"})
        >>> print(result)  # doctest: +SKIP
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"


    @agent
    def input_checker(self) -> Agent:
        """Creates an agent responsible for checking input security.
        
        This agent validates user inputs for potential security threats,
        malicious content, or unsafe patterns before processing.
        
        Returns:
            Agent: A CrewAI Agent configured for input security checking.
            
        Examples:
            >>> crew = SanitizeCrew()
            >>> checker = crew.input_checker()
            >>> isinstance(checker, Agent)
            True
        """
        return Agent(
            config=self.agents_config["input_checker"],  # type: ignore[index]

        )

        
    @agent
    def input_sanitizer(self) -> Agent:
        """Creates an agent responsible for sanitizing user inputs.
        
        This agent cleans and normalizes user inputs by removing or escaping
        potentially harmful characters and other
        malicious content patterns.
        
        Returns:
            Agent: A CrewAI Agent configured for input sanitization.
            
        Examples:
            >>> crew = SanitizeCrew()
            >>> sanitizer = crew.input_sanitizer()
            >>> isinstance(sanitizer, Agent)
            True
        """
        return Agent(
            config=self.agents_config["input_sanitizer"],  # type: ignore[index]
        )


    @task
    def check_input_task(self) -> Task:
        """Creates a task for checking input security and validity.
        
        This task performs security validation on user inputs, identifying
        potential threats, malicious patterns, or unsafe content. The results
        are saved to a JSON file for further processing.
        
        Returns:
            Task: A CrewAI Task configured for input security checking that
                outputs results to 'output/security_check.json'.
                
        Examples:
            >>> crew = SanitizeCrew()
            >>> task = crew.check_input_task()
            >>> isinstance(task, Task)
            True
            >>> task.output_file
            'output/security_check.json'
        """
        return Task(
            config=self.tasks_config["check_input_task"],  # type: ignore[index]
            agent=self.input_checker(),  # Assign to input_checker agent
            output_file='output/security_check.json',
        )
        
    @task
    def sanitize_input_task(self) -> Task:
        """Creates a task for sanitizing user inputs based on security check results.
        
        This task processes user inputs to remove or neutralize potentially
        harmful content. It depends on the check_input_task output and saves
        the sanitized results to a JSON file.
        
        Returns:
            Task: A CrewAI Task configured for input sanitization that
                outputs results to 'output/sanitized_query.json' and depends
                on the check_input_task completion.
                
        Examples:
            >>> crew = SanitizeCrew()
            >>> task = crew.sanitize_input_task()
            >>> isinstance(task, Task)
            True
            >>> task.output_file
            'output/sanitized_query.json'
            >>> len(task.context)
            1
        """
        return Task(
            config=self.tasks_config["sanitize_input_task"],  # type: ignore[index]
            agent=self.input_sanitizer(),  # Assign to input_sanitizer agent
            context=[self.check_input_task()],  # Depends on check_input_task output
            output_file='output/sanitized_query.json',
        )

    @crew
    def crew(self) -> Crew:
        """Creates and configures the complete sanitization crew.
        
        This method assembles all agents and tasks into a functional CrewAI
        crew that processes inputs sequentially through security checking
        and sanitization steps.
        
        Returns:
            Crew: A configured CrewAI Crew instance with sequential processing,
                verbose output enabled, containing input_checker and 
                input_sanitizer agents with their respective tasks.
                
        Examples:
            >>> crew_instance = SanitizeCrew()
            >>> sanitize_crew = crew_instance.crew()
            >>> isinstance(sanitize_crew, Crew)
            True
            >>> sanitize_crew.process == Process.sequential
            True
            >>> sanitize_crew.verbose
            True
        """
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )
