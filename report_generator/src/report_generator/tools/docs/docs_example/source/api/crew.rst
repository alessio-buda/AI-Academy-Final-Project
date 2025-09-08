crew module
===========

.. automodule:: game_builder_crew.crew
   :members:
   :undoc-members:
   :show-inheritance:

GameBuilderCrew Class
--------------------

.. autoclass:: game_builder_crew.crew.GameBuilderCrew
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

   The GameBuilderCrew class is the main orchestrator for the game building process. It coordinates three specialized AI agents to collaboratively create, review, and finalize Python game code.

   **Architecture Overview:**

   The class uses CrewAI's decorator pattern to define agents and tasks:

   - ``@agent`` decorator: Registers agent creation methods
   - ``@task`` decorator: Registers task definition methods  
   - ``@crew`` decorator: Defines the final crew assembly

   **Process Flow:**

   1. **Code Creation**: Senior Engineer Agent creates initial game code
   2. **Code Review**: QA Engineer Agent reviews and fixes issues
   3. **Final Evaluation**: Chief QA Engineer Agent ensures quality and completeness

Agent Methods
~~~~~~~~~~~~~

.. automethod:: game_builder_crew.crew.GameBuilderCrew.senior_engineer_agent

   Creates the Senior Software Engineer agent responsible for initial code creation.

   **Agent Configuration:**
      - **Role**: Senior Software Engineer
      - **Goal**: Create software as needed  
      - **Delegation**: Disabled (works independently)
      - **Verbose**: Enabled for detailed output

   **Responsibilities:**
      - Generate initial Python game code
      - Follow provided specifications
      - Implement core game mechanics
      - Include necessary imports and structure

   **Example Usage:**

   .. code-block:: python

      crew = GameBuilderCrew()
      senior_agent = crew.senior_engineer_agent()
      print(f"Agent role: {senior_agent.role}")

.. automethod:: game_builder_crew.crew.GameBuilderCrew.qa_engineer_agent

   Creates the QA Engineer agent for code review and error detection.

   **Agent Configuration:**
      - **Role**: Software Quality Control Engineer
      - **Goal**: Create perfect code by analyzing for errors
      - **Delegation**: Disabled (works independently)
      - **Verbose**: Enabled for detailed output

   **Responsibilities:**
      - Review code for syntax errors
      - Identify logic problems
      - Check for missing imports
      - Detect security vulnerabilities
      - Verify variable declarations
      - Check bracket matching

   **Example Usage:**

   .. code-block:: python

      crew = GameBuilderCrew()
      qa_agent = crew.qa_engineer_agent()
      print(f"Agent goal: {qa_agent.goal}")

.. automethod:: game_builder_crew.crew.GameBuilderCrew.chief_qa_engineer_agent

   Creates the Chief QA Engineer agent for final quality assurance.

   **Agent Configuration:**
      - **Role**: Chief Software Quality Control Engineer
      - **Goal**: Ensure code does the job it's supposed to do
      - **Delegation**: Enabled (can delegate to other agents)
      - **Verbose**: Enabled for detailed output

   **Responsibilities:**
      - Final code quality validation
      - Completeness verification
      - Functional testing consideration
      - Overall quality assurance
      - Code optimization suggestions

   **Example Usage:**

   .. code-block:: python

      crew = GameBuilderCrew()
      chief_agent = crew.chief_qa_engineer_agent()
      print(f"Delegation allowed: {chief_agent.allow_delegation}")

Task Methods
~~~~~~~~~~~~

.. automethod:: game_builder_crew.crew.GameBuilderCrew.code_task

   Defines the initial code creation task assigned to the Senior Engineer Agent.

   **Task Configuration:**
      - **Agent**: Senior Engineer Agent
      - **Input Variable**: ``{game}`` - Game specification
      - **Expected Output**: Complete Python code only

   **Process:**
      1. Receives game specifications via ``{game}`` variable
      2. Creates initial Python game implementation
      3. Includes all necessary imports and structure
      4. Outputs raw Python code without explanations

   **Example Task Input:**

   .. code-block:: python

      inputs = {
          'game': '''
          Create a Snake game with:
          - Arrow key controls
          - Growing snake mechanics
          - Food spawning
          - Collision detection
          '''
      }

.. automethod:: game_builder_crew.crew.GameBuilderCrew.review_task

   Defines the code review task assigned to the QA Engineer Agent.

   **Task Configuration:**
      - **Agent**: QA Engineer Agent
      - **Input**: Code from code_task + original game specification
      - **Expected Output**: Reviewed and corrected Python code

   **Review Checklist:**
      - Syntax errors
      - Logic errors  
      - Missing imports
      - Variable declarations
      - Bracket matching
      - Security vulnerabilities

   **Process:**
      1. Receives code from previous task
      2. Performs comprehensive code review
      3. Fixes identified issues
      4. Outputs corrected Python code

.. automethod:: game_builder_crew.crew.GameBuilderCrew.evaluate_task

   Defines the final evaluation task assigned to the Chief QA Engineer Agent.

   **Task Configuration:**
      - **Agent**: Chief QA Engineer Agent
      - **Input**: Reviewed code + original specifications
      - **Expected Output**: Final polished Python code

   **Evaluation Criteria:**
      - Code completeness
      - Requirement fulfillment
      - Code quality standards
      - Performance considerations
      - User experience factors

   **Process:**
      1. Receives reviewed code from previous task
      2. Validates against original requirements
      3. Ensures completeness and quality
      4. Outputs final game code

Crew Assembly
~~~~~~~~~~~~~

.. automethod:: game_builder_crew.crew.GameBuilderCrew.crew

   Assembles all agents and tasks into a complete crew for execution.

   **Configuration:**
      - **Process**: Sequential execution
      - **Agents**: All defined agents (auto-populated)
      - **Tasks**: All defined tasks (auto-populated)
      - **Verbose**: Enabled for detailed logging

   **Execution Flow:**

   .. mermaid::

      sequenceDiagram
          participant U as User
          participant C as Crew
          participant SE as Senior Engineer
          participant QA as QA Engineer
          participant CQA as Chief QA
          
          U->>C: kickoff(inputs)
          C->>SE: Execute code_task
          SE->>C: Initial code
          C->>QA: Execute review_task
          QA->>C: Reviewed code
          C->>CQA: Execute evaluate_task
          CQA->>C: Final code
          C->>U: Complete game

   **Usage Example:**

   .. code-block:: python

      from game_builder_crew.crew import GameBuilderCrew

      # Initialize crew
      crew_instance = GameBuilderCrew()
      
      # Get assembled crew
      game_crew = crew_instance.crew()
      
      # Execute with inputs
      inputs = {'game': 'Create a Pong game'}
      result = game_crew.kickoff(inputs=inputs)
      
      print("Generated game code:")
      print(result)

Configuration Attributes
~~~~~~~~~~~~~~~~~~~~~~~~

.. py:attribute:: GameBuilderCrew.agents_config

   Path to the agents configuration YAML file.

   :type: str
   :value: 'config/agents.yaml'

   Contains agent definitions including roles, goals, and backstories.

.. py:attribute:: GameBuilderCrew.tasks_config

   Path to the tasks configuration YAML file.

   :type: str  
   :value: 'config/tasks.yaml'

   Contains task descriptions and expected output specifications.

Advanced Usage
~~~~~~~~~~~~~

**Custom Configuration:**

.. code-block:: python

   class CustomGameBuilderCrew(GameBuilderCrew):
       agents_config = 'custom/agents.yaml'
       tasks_config = 'custom/tasks.yaml'
       
       @agent
       def custom_agent(self) -> Agent:
           return Agent(
               config=self.agents_config['custom_agent'],
               allow_delegation=True,
               verbose=True
           )

**Performance Monitoring:**

.. code-block:: python

   import time
   from game_builder_crew.crew import GameBuilderCrew

   crew = GameBuilderCrew()
   
   start_time = time.time()
   inputs = {'game': 'Create a simple game'}
   result = crew.crew().kickoff(inputs=inputs)
   end_time = time.time()
   
   print(f"Execution time: {end_time - start_time:.2f} seconds")
   print(f"Generated code length: {len(result)} characters")

**Error Handling:**

.. code-block:: python

   from game_builder_crew.crew import GameBuilderCrew
   import logging

   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   try:
       crew = GameBuilderCrew()
       inputs = {'game': 'Invalid or unclear game description'}
       result = crew.crew().kickoff(inputs=inputs)
       
   except Exception as e:
       logger.error(f"Crew execution failed: {e}")
       # Handle failure gracefully

See Also
--------

- :doc:`main`: Entry point functions
- :doc:`configuration`: Configuration file details
- :doc:`../usage`: Comprehensive usage guide
- :doc:`../examples`: Example implementations
