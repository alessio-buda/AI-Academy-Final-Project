from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class AnalysisCrew:
    """Analysis Crew for project analysis and structuring.
    
    This class implements a CrewAI-based system for analyzing project descriptions
    and creating structured outlines. It coordinates two specialized agents:
    a project analyzer and an outline creator, working sequentially to process
    user queries and generate comprehensive project documentation structures.
    
    The crew operates in two main phases:
    1. Project analysis: extracts key project details and determines target audience
    2. Outline creation: generates detailed hierarchical content structures
    
    Attributes:
        agents (List[BaseAgent]): List of AI agents involved in the analysis process.
        tasks (List[Task]): List of tasks to be executed by the agents.
        agents_config (str): Path to the YAML configuration file for agents.
        tasks_config (str): Path to the YAML configuration file for tasks.
    
    Example:
        >>> analysis_crew = AnalysisCrew()
        >>> crew_instance = analysis_crew.crew()
        >>> result = crew_instance.kickoff(inputs={"improved_query": "Project description"})
        >>> print(result)  # Output contains project analysis and outline
    """

    agents: List[BaseAgent]
    tasks: List[Task]

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def project_analyzer(self) -> Agent:
        """Creates and configures the project analysis agent.
        
        This method instantiates a specialized AI agent responsible for analyzing
        project descriptions and extracting key information such as objectives,
        components, target audience, and technical complexity.
        
        The agent is configured with:
        - Role: Project Analysis Specialist
        - Goal: Extract project details and determine target audience
        - LLM: Azure GPT-4o
        
        Returns:
            Agent: A configured CrewAI Agent instance specialized in project analysis.
                The agent can process improved user queries and generate structured
                JSON analysis containing project description, objectives, components,
                target audience, technical complexity, and application sector.
        
        Example:
            >>> crew = AnalysisCrew()
            >>> analyzer = crew.project_analyzer()
            >>> isinstance(analyzer, Agent)
            True
        """
        return Agent(
            config=self.agents_config["project_analyzer"],  # type: ignore[index]
        )

    @agent
    def outline_creator(self) -> Agent:
        """Creates and configures the content structure specialist agent.
        
        This method instantiates a specialized AI agent responsible for creating
        detailed hierarchical outlines based on project analysis results. The agent
        transforms project analysis into comprehensive content structures suitable
        for technical documentation.
        
        The agent is configured with:
        - Role: Content Structure Specialist
        - Goal: Create detailed outlines with subpoints based on project analysis
        - LLM: Azure GPT-4o
        
        Returns:
            Agent: A configured CrewAI Agent instance specialized in content structuring.
                The agent generates detailed outlines with 4-6 main sections, each
                containing 3-5 subpoints with descriptions, adapted for the target
                audience and technical complexity level.
        
        Example:
            >>> crew = AnalysisCrew()
            >>> creator = crew.outline_creator()
            >>> isinstance(creator, Agent)
            True
        """
        return Agent(
            config=self.agents_config["outline_creator"],  # type: ignore[index]
        )

    @task
    def analyze_project_task(self) -> Task:
        """Creates the project analysis task.
        
        This method defines a task that analyzes improved user queries to extract
        project details and create structured analysis. The task processes input
        queries and generates comprehensive project information including objectives,
        components, target audience classification, and technical complexity assessment.
        
        The task expects an 'improved_query' input parameter and outputs results to
        'output/project_analysis.json'.
        
        Returns:
            Task: A configured CrewAI Task instance for project analysis.
                The task generates a structured JSON output containing:
                - breve_descrizione_del_progetto: Concise Italian project description
                - obiettivi_principali: List of main objectives
                - componenti_chiave: List of key components
                - target_audience: Either "tecnico" or "non tecnico"
                - complessita_tecnica: "bassa", "media", or "alta"
                - settore_applicativo: Application sector
        
        Example:
            >>> crew = AnalysisCrew()
            >>> task = crew.analyze_project_task()
            >>> task.output_file
            'output/project_analysis.json'
        """
        return Task(
            config=self.tasks_config["analyze_project_task"],  # type: ignore[index]
            agent=self.project_analyzer(),
            output_file='output/project_analysis.json',
        )
        
    @task
    def create_outline_task(self) -> Task:
        """Creates the outline generation task.
        
        This method defines a task that creates comprehensive outlines with detailed
        subpoints based on project analysis results. The task takes the output from
        the analyze_project_task as context and generates a structured outline
        suitable for comprehensive technical or business documentation.
        
        The task outputs results to 'output/detailed_outline.json' and depends on
        the completion of the analyze_project_task.
        
        Returns:
            Task: A configured CrewAI Task instance for outline creation.
                The task generates a structured JSON output containing:
                - titolo_report: Italian report title
                - sezioni: List of main sections with titles, descriptions, and subsections
                - target_audience: Either "tecnico" or "non tecnico"
                - stile_comunicazione: Communication style ("formale", "informale", 
                  "tecnico", or "business")
        
        Example:
            >>> crew = AnalysisCrew()
            >>> task = crew.create_outline_task()
            >>> task.output_file
            'output/detailed_outline.json'
            >>> len(task.context)
            1
        """
        return Task(
            config=self.tasks_config["create_outline_task"],  # type: ignore[index]
            agent=self.outline_creator(),
            context=[self.analyze_project_task()],
            output_file='output/detailed_outline.json',
        )

    @crew
    def crew(self) -> Crew:
        """Creates and configures the Analysis Crew.
        
        This method assembles the complete CrewAI crew by combining the project
        analyzer and outline creator agents with their respective tasks. The crew
        is configured to execute tasks sequentially, ensuring that project analysis
        is completed before outline creation begins.
        
        The crew operates with:
        - Process: Sequential execution
        - Verbose mode: Enabled for detailed logging
        - Two agents: project_analyzer and outline_creator
        - Two tasks: analyze_project_task and create_outline_task
        
        Returns:
            Crew: A configured CrewAI Crew instance ready for execution.
                The crew processes improved user queries through a two-stage pipeline:
                1. Project analysis (outputs to 'output/project_analysis.json')
                2. Outline creation (outputs to 'output/detailed_outline.json')
        
        Example:
            >>> analysis_crew = AnalysisCrew()
            >>> crew_instance = analysis_crew.crew()
            >>> crew_instance.process == Process.sequential
            True
            >>> crew_instance.verbose
            True
            >>> len(crew_instance.agents)
            2
            >>> len(crew_instance.tasks)
            2
        """
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
