Installation
============

This guide will help you set up the AI Academy Report Generator system.

Requirements
------------

- Python 3.10 or higher
- `uv <https://docs.astral.sh/uv/>`_ package manager (recommended) or pip
- Git (for cloning the repository)
- Azure OpenAI Service access
- **Qdrant vector database server** (local or cloud)
- At least 4GB of available memory
- Internet connection (for downloading models and dependencies)

Installing uv
~~~~~~~~~~~~~

If you don't have `uv` installed, you can install it with:

.. code-block:: bash

   # On Windows (PowerShell)
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # On macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Using pip
   pip install uv

Qdrant Vector Database Setup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The system requires a Qdrant vector database for RAG functionality. Choose one of the following options:

**Option 1: Qdrant Cloud** (Recommended for production)
   1. Visit `Qdrant Cloud <https://cloud.qdrant.io/>`_
   2. Sign up for a free account  
   3. Create a new cluster
   4. Note your cluster URL and API key

**Option 2: Local Qdrant Server**
   .. code-block:: bash
   
      # Using Docker (if available)
      docker run -p 6333:6333 qdrant/qdrant
      
      # Or download Qdrant binary from:
      # https://github.com/qdrant/qdrant/releases

**Option 3: Remote Qdrant Instance**
   Use an existing Qdrant server with proper network access.

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

   Using uv (recommended):

   .. code-block:: bash

      uv sync

   Or using pip:

   .. code-block:: bash

      pip install -e .

Environment Setup
-----------------

The system requires several environment variables to be configured:

Required Environment Variables
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Copy the example environment file and configure it:

.. code-block:: bash

   cp .env.example .env

Edit the `.env` file with your configuration:

.. code-block:: bash

   # Model Configuration
   MODEL=gpt-4

   # Azure API Configuration
   AZURE_API_KEY=your_azure_api_key_here
   AZURE_API_BASE=https://your-resource.openai.azure.com/
   AZURE_API_VERSION=2024-02-15-preview
   AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/

   # Azure OpenAI Configuration (Required)
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_VERSION=2024-02-15-preview

   # Qdrant Vector Database Configuration (Required)
   QDRANT_URL=http://localhost:6333        # For local Qdrant
   # QDRANT_URL=https://your-cluster.qdrant.io  # For Qdrant Cloud
   # QDRANT_API_KEY=your_qdrant_api_key_here     # For Qdrant Cloud only

   # Serper API for web search (Optional)
   SERPER_API_KEY=your_serper_api_key_here

Getting API Keys
~~~~~~~~~~~~~~~~

**Azure OpenAI API Key** (Required):
   1. Visit `Azure Portal <https://portal.azure.com/>`_
   2. Create or access your Azure OpenAI Service resource
   3. Go to "Keys and Endpoint" section
   4. Copy the API key and endpoint URL
   5. Note your API version (typically 2024-02-15-preview)

**Model Deployments**:
   Ensure you have deployed the following models in your Azure OpenAI resource:
   
   - **GPT-4** or **GPT-3.5-turbo** for text generation
   - **text-embedding-ada-002** for embeddings

**Serper API Key** (Optional):
   For enhanced web search capabilities:
   
   1. Visit `Serper.dev <https://serper.dev/>`_
   2. Sign up for a free account
   3. Get your API key from the dashboard

**Qdrant Setup** (Required):
   For vector database functionality:
   
   **Qdrant Cloud**:
      1. Visit `Qdrant Cloud <https://cloud.qdrant.io/>`_
      2. Create a free account and cluster
      3. Get your cluster URL and API key
   
   **Local Qdrant**:
      - Run ``docker run -p 6333:6333 qdrant/qdrant``
      - Or download from `Qdrant releases <https://github.com/qdrant/qdrant/releases>`_
      - Use ``http://localhost:6333`` as QDRANT_URL

Verification
------------

To verify your installation:

.. code-block:: bash

   # Test the main application
   crewai run

If everything is set up correctly, the system should start generating a sample report. You'll see output indicating the crews are working through their tasks.

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
   Verify your Azure OpenAI configuration:
   
   - Check that your Azure OpenAI service is active
   - Ensure the endpoint URL is correct
   - Verify the API version matches your deployment
   - Confirm your models are properly deployed

**Memory Issues**:
   The system requires significant memory for LLM operations. Ensure you have at least 4GB available

**Qdrant Connection Issues**:
   If you encounter Qdrant-related errors:
   
   - **Local Qdrant**: Ensure Qdrant server is running on port 6333
   - **Qdrant Cloud**: Verify your cluster URL and API key are correct
   - **Network**: Check firewall settings and network connectivity
   - **Configuration**: Ensure QDRANT_URL is properly formatted

**Embedding Issues**:
   If you encounter embedding-related problems:
   
   - Verify your embedding deployment name matches AZURE_OPENAI_EMBEDDING_DEPLOYMENT
   - Check that the text-embedding-ada-002 model is deployed in your Azure resource

Getting Help
~~~~~~~~~~~~

If you encounter issues:

1. Check the :doc:`troubleshooting guide <troubleshooting>`
2. Review the :doc:`FAQ section <faq>`
3. Create an issue on the `GitHub repository <https://github.com/alessio-buda/AI-Academy-Final-Project/issues>`_
