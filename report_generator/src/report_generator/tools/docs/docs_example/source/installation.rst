Installation Guide
==================

This guide will help you install and set up the Game Builder Crew system on your machine.

System Requirements
------------------

Before installing the Game Builder Crew, ensure your system meets the following requirements:

**Python Version**
   - Python 3.8 or higher
   - pip package manager

**Operating Systems**
   - Windows 10/11
   - macOS 10.14 or later
   - Linux (Ubuntu 18.04+ or equivalent)

**API Access**
   - OpenAI API key (for GPT-4o access)
   - Optional: Serper API key (for web search capabilities)

**Memory Requirements**
   - Minimum: 4GB RAM
   - Recommended: 8GB RAM or higher

Installation Methods
-------------------

Method 1: Using Poetry (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Poetry is the recommended package manager for this project as it handles dependency management and virtual environments automatically.

1. **Install Poetry**

   If you don't have Poetry installed, install it first:

   .. tabs::

      .. group-tab:: Windows

         .. code-block:: powershell

            (Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -

      .. group-tab:: macOS/Linux

         .. code-block:: bash

            curl -sSL https://install.python-poetry.org | python3 -

2. **Clone the Repository**

   .. code-block:: bash

      git clone https://github.com/crewAIInc/crewAI-examples.git
      cd crewAI-examples/crews/game-builder-crew

3. **Install Dependencies**

   .. code-block:: bash

      poetry lock
      poetry install

4. **Activate Virtual Environment**

   .. code-block:: bash

      poetry shell

Method 2: Using pip and venv
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you prefer using pip and virtual environments:

1. **Clone the Repository**

   .. code-block:: bash

      git clone https://github.com/crewAIInc/crewAI-examples.git
      cd crewAI-examples/crews/game-builder-crew

2. **Create Virtual Environment**

   .. code-block:: bash

      python -m venv game-builder-env

3. **Activate Virtual Environment**

   .. tabs::

      .. group-tab:: Windows

         .. code-block:: cmd

            game-builder-env\Scripts\activate

      .. group-tab:: macOS/Linux

         .. code-block:: bash

            source game-builder-env/bin/activate

4. **Install Dependencies**

   .. code-block:: bash

      pip install -r requirements.txt

.. note::
   If requirements.txt doesn't exist, you can generate it from pyproject.toml:
   
   .. code-block:: bash
   
      poetry export -f requirements.txt --output requirements.txt

Environment Configuration
-------------------------

After installation, you need to configure environment variables for API access.

1. **Copy Environment Template**

   .. code-block:: bash

      cp .env.example .env

2. **Configure API Keys**

   Edit the `.env` file with your API credentials:

   .. code-block:: bash

      # OpenAI API Configuration
      OPENAI_API_KEY=your_openai_api_key_here
      OPENAI_MODEL=gpt-4o

      # Optional: Serper API for web search
      SERPER_API_KEY=your_serper_api_key_here

      # Logging Configuration
      LOG_LEVEL=INFO
      CREW_VERBOSE=true

3. **Obtain API Keys**

   **OpenAI API Key:**
      1. Visit `OpenAI Platform <https://platform.openai.com/api-keys>`_
      2. Sign up or log in to your account
      3. Navigate to API Keys section
      4. Create a new secret key
      5. Copy the key to your `.env` file

   **Serper API Key (Optional):**
      1. Visit `Serper.dev <https://serper.dev>`_
      2. Sign up for an account
      3. Get your API key from the dashboard
      4. Add it to your `.env` file

Verification
-----------

To verify your installation is working correctly:

1. **Test Import**

   .. code-block:: python

      python -c "from game_builder_crew.crew import GameBuilderCrew; print('Installation successful!')"

2. **Run Quick Test**

   .. code-block:: bash

      poetry run python -c "
      from game_builder_crew.crew import GameBuilderCrew
      crew = GameBuilderCrew()
      print('Game Builder Crew initialized successfully!')
      "

3. **Check Dependencies**

   .. code-block:: bash

      poetry show --tree

Troubleshooting
--------------

Common Installation Issues
~~~~~~~~~~~~~~~~~~~~~~~~~

**Poetry Not Found**
   If you get "poetry: command not found":

   .. code-block:: bash

      # Add Poetry to PATH (Linux/macOS)
      export PATH="$HOME/.local/bin:$PATH"

      # Restart your terminal or run:
      source ~/.bashrc  # or ~/.zshrc

**Python Version Issues**
   If you get Python version compatibility errors:

   .. code-block:: bash

      # Check Python version
      python --version

      # Use specific Python version with Poetry
      poetry env use python3.8

**Dependency Conflicts**
   If you encounter dependency conflicts:

   .. code-block:: bash

      # Clear Poetry cache
      poetry cache clear pypi --all

      # Reinstall dependencies
      poetry install --no-cache

**Permission Errors**
   On Unix systems, if you get permission errors:

   .. code-block:: bash

      # Install Poetry for user only
      curl -sSL https://install.python-poetry.org | python3 - --user

**API Key Issues**
   If you get authentication errors:

   1. Verify your API key is correct
   2. Check if you have sufficient API credits
   3. Ensure the key has proper permissions
   4. Test the key with a simple API call

Network Issues
~~~~~~~~~~~~~

If you're behind a corporate firewall:

.. code-block:: bash

   # Configure Poetry to use proxy
   poetry config http-basic.pypi username password
   poetry config repositories.pypi https://pypi.org/simple/

Development Installation
-----------------------

For development purposes, you may want additional tools:

1. **Install Development Dependencies**

   .. code-block:: bash

      poetry install --with dev

2. **Install Pre-commit Hooks**

   .. code-block:: bash

      pre-commit install

3. **Run Tests**

   .. code-block:: bash

      poetry run pytest

4. **Build Documentation**

   .. code-block:: bash

      cd docs/sphinx
      poetry run sphinx-build -b html source _build/html

Next Steps
---------

After successful installation:

1. Read the :doc:`quickstart` guide
2. Explore :doc:`usage` examples
3. Check out the :doc:`api/modules` reference
4. Join the community discussions

.. tip::
   Keep your dependencies updated regularly:
   
   .. code-block:: bash
   
      poetry update

For additional help, visit our `GitHub repository <https://github.com/crewAIInc/crewAI-examples>`_ or check the troubleshooting section.
