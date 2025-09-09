API Reference
=============

This section provides comprehensive API documentation for all modules, classes, and functions in the Game Builder Crew system.

.. toctree::
   :maxdepth: 2
   :caption: API Modules:

   crew
   main
   configuration

Module Overview
---------------

The Game Builder Crew consists of the following main modules:

**Core Modules:**

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - Module
     - Purpose
     - Key Components
   * - ``crew.py``
     - Main orchestration
     - GameBuilderCrew class, agents, tasks
   * - ``main.py``
     - Entry points
     - run(), train() functions
   * - ``__init__.py``
     - Package setup
     - Exports and version info

**Configuration Files:**

.. list-table::
   :header-rows: 1
   :widths: 20 30 50

   * - File
     - Purpose
     - Contents
   * - ``agents.yaml``
     - Agent definitions
     - Roles, goals, backstories
   * - ``tasks.yaml``
     - Task specifications
     - Descriptions, expected outputs
   * - ``gamedesign.yaml``
     - Game examples
     - Pre-built game specifications

Quick Reference
--------------

**Most Common Classes and Functions:**

.. py:class:: GameBuilderCrew

   Main orchestrator class for the game building process.

   .. py:method:: crew() -> Crew
      
      Returns the configured crew ready for execution.

.. py:function:: run() -> None

   Execute the game building process with default Snake game example.

.. py:function:: train(n_iterations: int, filename: str) -> None

   Train the crew using iterative learning.

**Configuration Access:**

.. code-block:: python

   from game_builder_crew.crew import GameBuilderCrew
   
   # Initialize crew
   crew = GameBuilderCrew()
   
   # Access individual agents
   senior_agent = crew.senior_engineer_agent()
   qa_agent = crew.qa_engineer_agent()
   chief_agent = crew.chief_qa_engineer_agent()
   
   # Access individual tasks
   code_task = crew.code_task()
   review_task = crew.review_task()
   evaluate_task = crew.evaluate_task()
   
   # Get complete crew
   complete_crew = crew.crew()

**Execution Patterns:**

.. code-block:: python

   # Basic execution
   from game_builder_crew.main import run
   run()
   
   # Custom execution
   from game_builder_crew.crew import GameBuilderCrew
   crew = GameBuilderCrew()
   inputs = {'game': 'Your game description here'}
   result = crew.crew().kickoff(inputs=inputs)
   
   # Training
   from game_builder_crew.main import train
   train(n_iterations=10, filename='trained_model.pkl')

Type Definitions
---------------

**Common Types:**

.. code-block:: python

   from typing import Dict, Any, Optional, List
   from crewai import Agent, Task, Crew
   
   # Input type for crew execution
   GameInputs = Dict[str, str]
   
   # Configuration dictionaries
   AgentConfig = Dict[str, Any]
   TaskConfig = Dict[str, Any]
   
   # Function signatures
   def crew_function() -> Crew: ...
   def agent_function() -> Agent: ...
   def task_function() -> Task: ...

Error Handling
--------------

**Exception Hierarchy:**

The system uses standard Python exceptions with specific handling:

.. code-block:: python

   # Configuration errors
   FileNotFoundError: Configuration files missing
   yaml.YAMLError: Invalid YAML syntax
   
   # Execution errors  
   Exception: General crew execution failures
   ValueError: Invalid parameter values
   IndexError: Missing command line arguments
   
   # API errors
   openai.error.APIError: OpenAI API issues
   openai.error.RateLimitError: API rate limiting
   openai.error.AuthenticationError: Invalid API keys

**Error Handling Example:**

.. code-block:: python

   from game_builder_crew.crew import GameBuilderCrew
   import yaml
   
   try:
       crew = GameBuilderCrew()
       inputs = {'game': 'Create a simple Snake game'}
       result = crew.crew().kickoff(inputs=inputs)
       
   except FileNotFoundError as e:
       print(f"Configuration file missing: {e}")
       
   except yaml.YAMLError as e:
       print(f"YAML parsing error: {e}")
       
   except Exception as e:
       print(f"Execution error: {e}")
       # Log full traceback for debugging
       import traceback
       traceback.print_exc()

Version Information
------------------

.. code-block:: python

   import game_builder_crew
   
   print(f"Version: {game_builder_crew.__version__}")
   print(f"Author: {game_builder_crew.__author__}")

**Compatibility:**

- Python: 3.8+
- CrewAI: 0.130.0+
- OpenAI: Latest
- Operating Systems: Windows, macOS, Linux

For detailed documentation of each module, see the respective pages in this section.
