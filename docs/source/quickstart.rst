Quick Start
===========

This guide will get you up and running with the AI Academy Report Generator in under 10 minutes.

Prerequisites
-------------

Before starting, ensure you have:

- Python 3.10+ installed
- `uv <https://docs.astral.sh/uv/>`_ package manager (install with: ``pip install uv``)
- Azure OpenAI Service access
- **Qdrant vector database server** running and accessible
- Internet connection

Qdrant Server Setup
-------------------

The system requires a Qdrant vector database server for RAG (Retrieval-Augmented Generation) functionality.

**Option 1: Qdrant Cloud** (Recommended)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Visit `Qdrant Cloud <https://cloud.qdrant.io/>`_
2. Sign up for a free account
3. Create a new cluster
4. Note your cluster URL and API key

**Option 2: Local Qdrant Server**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Install and run Qdrant locally:

.. code-block:: bash

   # Using Docker (if you have Docker installed)
   docker run -p 6333:6333 qdrant/qdrant
   
   # Or download and run Qdrant binary directly
   # Visit: https://github.com/qdrant/qdrant/releases

**Option 3: Remote Qdrant Server**
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have access to a remote Qdrant server, ensure it's accessible and you have the connection details.

Basic Setup
-----------

1. **Install the system**:

   .. code-block:: bash

      git clone https://github.com/alessio-buda/AI-Academy-Final-Project.git
      cd AI-Academy-Final-Project/report_generator
      uv sync

2. **Set up environment**:

   Copy the example environment file and configure it:

   .. code-block:: bash

      cp .env.example .env

   Then edit the `.env` file with your API keys:

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
      QDRANT_URL=http://localhost:6333  # For local Qdrant
      # QDRANT_URL=https://your-cluster.qdrant.io  # For Qdrant Cloud
      # QDRANT_API_KEY=your_qdrant_api_key_here     # For Qdrant Cloud
      
      # Serper API for web search (Optional)
      SERPER_API_KEY=your_serper_api_key_here

3. **Run your first report**:

   .. code-block:: bash

      crewai run

That's it! The system will generate a sample report using the default configuration.

Understanding the Output
------------------------

After running the system, you'll find several files in the `output/` directory:

.. code-block:: text

   output/
   ├── final_report.md          # The main generated report
   ├── detailed_outline.json    # Structured outline of the report
   ├── project_analysis.json    # Analysis results from the Analysis Crew
   ├── sanitized_query.json     # Sanitized and validated input
   ├── security_check.json      # Security validation results
   ├── rag_search_results.md    # RAG search results (if enabled)
   └── generation_summary.md    # Summary of the generation process

Customizing Your First Report
------------------------------

To customize the report generation, modify the input in `src/report_generator/main.py`:

.. code-block:: python

   user_input = {
       "project_description": "Your project description here",
       "outline": "Custom outline topics",
       "audience": "technical",  # or "business", "general"
   }

Example: Generating a Technical Report
---------------------------------------

Here's a complete example for generating a technical report about a Python web application:

.. code-block:: python

   user_input = {
       "project_description": """
       A FastAPI-based REST API for managing a task management system.
       The application uses PostgreSQL for data persistence,
       Redis for caching, and implements JWT authentication.
       """,
       "outline": """
       Architecture Overview,
       API Design Patterns,
       Database Schema,
       Authentication & Security,
       Performance Considerations,
       Deployment Strategy
       """,
       "audience": "technical"
   }

Key Features in Action
----------------------

🔒 **Security & Sanitization**
   The Sanitize Crew automatically validates and cleans your input, checking for potential security issues.

🔍 **Intelligent Analysis**
   The Analysis Crew researches your topic and creates a detailed analysis using AI and RAG search.

✍️ **Professional Writing**
   The Writer Crew generates a well-structured, professional report based on the analysis.

Next Steps
----------

Now that you have a basic understanding:

1. **Explore the Architecture**: Read about the :doc:`system architecture <architecture/overview>`
2. **Customize Crews**: Learn how to :doc:`configure crews <usage>` for your specific needs
3. **Advanced Features**: Discover :doc:`advanced configuration options <examples/advanced_configuration>`
4. **API Reference**: Dive into the :doc:`complete API documentation <api/main>`

Common Use Cases
----------------

The system is particularly useful for:

- **Technical Documentation**: Generate comprehensive technical reports
- **Project Analysis**: Analyze and document software projects
- **Research Reports**: Create structured research documents
- **Business Analysis**: Generate business-focused project assessments

Troubleshooting
---------------

If you encounter issues:

- **No output generated**: Check your OpenAI API key and internet connection
- **Memory errors**: Ensure you have sufficient RAM (4GB+ recommended)
- **Import errors**: Verify installation with ``pip install -e .``

For more help, see the :doc:`installation guide <installation>` or :doc:`troubleshooting section <troubleshooting>`.
