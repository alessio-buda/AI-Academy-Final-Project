Quick Start
===========

This guide will get you up and running with the AI Academy Report Generator in under 10 minutes.

Prerequisites
-------------

Before starting, ensure you have:

- Python 3.10+ installed
- OpenAI API key
- Internet connection

Basic Setup
-----------

1. **Install the system**:

   .. code-block:: bash

      git clone https://github.com/alessio-buda/AI-Academy-Final-Project.git
      cd AI-Academy-Final-Project/report_generator
      pip install -e .

2. **Set up environment**:

   Create a `.env` file:

   .. code-block:: bash

      OPENAI_API_KEY=your_api_key_here

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
