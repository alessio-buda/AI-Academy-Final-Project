Installation
============

This guide will help you set up the AI Academy Report Generator system.

Requirements
------------

- Python 3.10 or higher
- Git (for cloning the repository)
- At least 4GB of available memory
- Internet connection (for downloading models and dependencies)

Quick Installation
------------------

1. **Clone the repository**:

   .. code-block:: bash

      git clone https://github.com/alessio-buda/AI-Academy-Final-Project.git
      cd AI-Academy-Final-Project

2. **Navigate to the project directory**:

   .. code-block:: bash

      cd report_generator

3. **Install dependencies**:

   Using pip:

   .. code-block:: bash

      pip install -e .

   Or using uv (recommended):

   .. code-block:: bash

      uv sync

Environment Setup
-----------------

The system requires several environment variables to be configured:

Required Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create a `.env` file in the project root with the following variables:

.. code-block:: bash

   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   
   # Qdrant Vector Database (if using cloud)
   QDRANT_URL=your_qdrant_url_here
   QDRANT_API_KEY=your_qdrant_api_key_here
   
   # MLflow Configuration (optional)
   MLFLOW_TRACKING_URI=your_mlflow_uri_here

Getting API Keys
~~~~~~~~~~~~~~~~

**OpenAI API Key**:
   1. Visit `OpenAI Platform <https://platform.openai.com/>`_
   2. Create an account or sign in
   3. Navigate to API Keys section
   4. Create a new secret key

**Qdrant Setup**:
   You can either:
   
   - Use Qdrant Cloud (recommended for production)
   - Run Qdrant locally using Docker:
   
   .. code-block:: bash

      docker run -p 6333:6333 qdrant/qdrant

Verification
------------

To verify your installation:

.. code-block:: bash

   # Test the main application
   python -m report_generator.main --help
   
   # Or using CrewAI
   crewai run

If everything is set up correctly, you should see the help output or the system should start running.

Development Installation
------------------------

For development work, install with development dependencies:

.. code-block:: bash

   # Install with development dependencies
   pip install -e ".[dev]"
   
   # Install pre-commit hooks
   pre-commit install

Docker Installation
-------------------

You can also run the system using Docker:

.. code-block:: bash

   # Build the Docker image
   docker build -t ai-report-generator .
   
   # Run the container
   docker run -it --env-file .env ai-report-generator

Troubleshooting
---------------

Common Issues
~~~~~~~~~~~~~

**Import Errors**:
   Make sure you've installed the package in editable mode with ``pip install -e .``

**API Key Issues**:
   Verify your environment variables are correctly set and the API keys are valid

**Memory Issues**:
   The system requires significant memory for LLM operations. Ensure you have at least 4GB available

**Qdrant Connection Issues**:
   If using local Qdrant, ensure Docker is running and the service is accessible on port 6333

Getting Help
~~~~~~~~~~~~

If you encounter issues:

1. Check the :doc:`troubleshooting guide <troubleshooting>`
2. Review the :doc:`FAQ section <faq>`
3. Create an issue on the `GitHub repository <https://github.com/alessio-buda/AI-Academy-Final-Project/issues>`_
