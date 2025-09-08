.. Game Builder Crew documentation master file
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Game Builder Crew Documentation
===============================

.. image:: https://img.shields.io/badge/CrewAI-Framework-blue
   :alt: CrewAI Framework
   :target: https://crewai.com

.. image:: https://img.shields.io/badge/Python-3.8%2B-blue
   :alt: Python Version
   :target: https://python.org

.. image:: https://img.shields.io/badge/License-MIT-green
   :alt: License
   :target: https://opensource.org/licenses/MIT

Welcome to the Game Builder Crew documentation! This project demonstrates the use of the CrewAI framework to automate the creation of Python games using AI agents.

Overview
--------

The Game Builder Crew is an innovative AI-powered system that leverages multiple specialized agents to collaboratively create Python games. Using the CrewAI framework, this system orchestrates autonomous AI agents to work together in a structured, sequential process that mirrors professional software development practices.

.. note::
   This project uses GPT-4o by default. Make sure you have access to OpenAI's API to run the system.

Key Features
-----------

🤖 **Multi-Agent Collaboration**
   Three specialized AI agents work together to create, review, and finalize game code.

🎮 **Game Development Focus**
   Specifically designed for creating Python-based games with comprehensive specifications.

🔍 **Quality Assurance**
   Built-in code review and quality control through specialized QA agents.

⚡ **Automated Workflow**
   Streamlined process from game concept to executable Python code.

🛠️ **Extensible Architecture**
   Easy to extend with new agents, tasks, and game types.

Agent Architecture
-----------------

The system consists of three specialized agents working in sequence:

**Senior Engineer Agent**
   Creates the initial game code based on specifications

**QA Engineer Agent**
   Reviews code for errors, bugs, and improvements

**Chief QA Engineer Agent**
   Performs final quality assurance and completeness validation

Quick Start
----------

1. **Installation**

   .. code-block:: bash

      cd game-builder-crew
      poetry install

2. **Configuration**

   Copy `.env.example` to `.env` and configure your API keys:

   .. code-block:: bash

      cp .env.example .env
      # Edit .env with your OpenAI API key

3. **Run the Crew**

   .. code-block:: bash

      poetry run game_builder_crew

4. **View Results**

   The system will generate complete Python game code ready for execution.

Example Output
-------------

The Game Builder Crew can create various types of games:

- **Snake Game**: Classic snake game with collision detection and scoring
- **Pac-Man Game**: Maze-based game with ghost AI and power pellets  
- **Custom Games**: Any game type based on detailed specifications

.. code-block:: python

   from game_builder_crew.crew import GameBuilderCrew

   # Create crew instance
   crew = GameBuilderCrew()

   # Define game requirements
   inputs = {
       'game': 'Create a Snake game with arrow key controls'
   }

   # Execute crew and get results
   result = crew.crew().kickoff(inputs=inputs)
   print(result)  # Complete Python game code

Documentation Contents
---------------------

.. toctree::
   :maxdepth: 2
   :caption: User Guide:

   installation
   quickstart
   usage
   examples

.. toctree::
   :maxdepth: 2
   :caption: API Reference:

   api/modules
   api/crew
   api/main
   api/configuration

.. toctree::
   :maxdepth: 2
   :caption: Developer Guide:

   development/architecture
   development/extending
   development/testing
   development/troubleshooting

.. toctree::
   :maxdepth: 1
   :caption: Additional Resources:

   changelog
   contributing
   license

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

Support and Community
====================

- **GitHub Repository**: `crewAI-examples <https://github.com/crewAIInc/crewAI-examples>`_
- **CrewAI Framework**: `Official Documentation <https://docs.crewai.com>`_
- **Issues and Bug Reports**: `GitHub Issues <https://github.com/crewAIInc/crewAI-examples/issues>`_
- **Discussions**: `GitHub Discussions <https://github.com/crewAIInc/crewAI-examples/discussions>`_

License
=======

This project is released under the MIT License. See the LICENSE file for details.

---

*Built with ❤️ using CrewAI Framework*
