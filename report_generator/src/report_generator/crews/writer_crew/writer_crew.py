from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List

from src.report_generator.tools.rag_tool import RagTool

@CrewBase
class WriterCrew():
    """WriterCrew crew - Simplified for RAG search and writing.
    
    A CrewAI-based crew that orchestrates RAG (Retrieval-Augmented Generation) 
    search and report writing tasks. The crew consists of two agents: a RAG 
    searcher that retrieves information from a knowledge base, and a writer 
    that creates comprehensive reports based on the retrieved information.
    
    Attributes:
        agents (List[BaseAgent]): List of agents in the crew (rag_searcher, writer).
        tasks (List[Task]): List of tasks to be executed (rag_search_task, write_report_task).
        agents_config (str): Path to the agents configuration YAML file.
        tasks_config (str): Path to the tasks configuration YAML file.
    
    Example:
        >>> crew = WriterCrew()
        >>> result = crew.crew().kickoff(inputs={'outline_structure': 'Introduction\\n1. Overview'})
        >>> print(result)  # doctest: +SKIP
        Crew execution completed with report generation
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"
        
    @agent
    def rag_searcher(self) -> Agent:
        """Create a RAG searcher agent for information retrieval.
        
        Creates an agent specialized in retrieving information from a knowledge 
        base using the RAG (Retrieval-Augmented Generation) tool. The agent is 
        configured to only use factual information retrieved from the RAG tool 
        and never generate fictional content.
        
        Returns:
            Agent: A configured RAG searcher agent with the following properties:
                - Uses RagTool for information retrieval
                - Maximum 5 iterations per task
                - No delegation allowed
                - Verbose output enabled
        
        Example:
            >>> crew = WriterCrew()
            >>> searcher = crew.rag_searcher()
            >>> searcher.role  # doctest: +SKIP
            'RAG Information Retrieval Specialist'
        """
        return Agent(
            config=self.agents_config['rag_searcher'], # type: ignore[index]
            verbose=True,
            tools=[RagTool()],
            allow_delegation=False,
            max_iter=5
        )
        
    @agent
    def writer(self) -> Agent:
        """Create a report writer agent for content generation.
        
        Creates an agent specialized in transforming outlines and source materials 
        into well-structured, engaging content. The agent adapts writing style to 
        suit both technical and non-technical audiences while maintaining accuracy 
        and clarity.
        
        Returns:
            Agent: A configured writer agent with the following properties:
                - Specializes in technical writing
                - Adapts to target audience and communication style
                - Outputs content in markdown format
                - Verbose output enabled
        
        Example:
            >>> crew = WriterCrew()
            >>> writer = crew.writer()
            >>> writer.role  # doctest: +SKIP
            'Report Writer'
        """
        return Agent(
            config=self.agents_config['writer'], # type: ignore[index]
            verbose=True
        )

    @task
    def rag_search_task(self) -> Task:
        """Create a RAG search task for information retrieval.
        
        Creates a task that uses the RAG searcher agent to retrieve information 
        for each section in a provided outline. The task ensures only factual, 
        tool-retrieved information is used and never generates fictional content.
        
        Returns:
            Task: A configured RAG search task with the following properties:
                - Uses rag_searcher agent
                - Equipped with RagTool
                - Outputs results to 'output/rag_search_results.md'
                - Reports errors and empty results clearly
        
        Example:
            >>> crew = WriterCrew()
            >>> task = crew.rag_search_task()
            >>> task.output_file  # doctest: +SKIP
            'output/rag_search_results.md'
        """
        return Task(
            config=self.tasks_config['rag_search_task'], # type: ignore[index]
            agent=self.rag_searcher(),
            tools=[RagTool()],
            output_file='output/rag_search_results.md',
        )
        
    @task
    def write_report_task(self) -> Task:
        """Create a report writing task for content generation.
        
        Creates a task that uses the writer agent to generate comprehensive 
        content for each section based on the outline and retrieved documents 
        from the RAG search task. The content is adapted to the specified 
        target audience and communication style.
        
        Returns:
            Task: A configured report writing task with the following properties:
                - Uses writer agent
                - Depends on rag_search_task for context
                - Outputs final report to 'output/final_report.md'
                - Adapts content to target audience and communication style
        
        Example:
            >>> crew = WriterCrew()
            >>> task = crew.write_report_task()
            >>> task.output_file  # doctest: +SKIP
            'output/final_report.md'
        """
        return Task(
            config=self.tasks_config['write_report_task'], # type: ignore[index]
            agent=self.writer(),
            output_file='output/final_report.md',
            context=[self.rag_search_task()],
        )
        
    @crew
    def crew(self) -> Crew:
        """Creates the WriterCrew crew for orchestrated task execution.
        
        Creates and configures a CrewAI crew that orchestrates the sequential 
        execution of RAG search and report writing tasks. The crew executes 
        tasks in order: first retrieving information via RAG search, then 
        generating the final report based on the retrieved content.
        
        Returns:
            Crew: A configured crew with the following properties:
                - Contains rag_searcher and writer agents
                - Executes rag_search_task and write_report_task sequentially
                - Process.sequential execution order
                - Verbose output enabled
        
        Example:
            >>> crew = WriterCrew()
            >>> crew_instance = crew.crew()
            >>> crew_instance.process  # doctest: +SKIP
            <Process.sequential: 'sequential'>
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
