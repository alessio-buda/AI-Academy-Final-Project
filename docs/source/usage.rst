Usage Guide
===========

This guide covers how to use the AI Academy Report Generator system effectively.

Basic Usage
-----------

Command Line Interface
~~~~~~~~~~~~~~~~~~~~~~

The simplest way to run the system:

.. code-block:: bash

   # Run with default configuration
   crewai run
   
   # Run specific crew flows
   python -m report_generator.main

Programmatic Usage
~~~~~~~~~~~~~~~~~~

You can also use the system programmatically:

.. code-block:: python

   from report_generator.main import ReportFlow
   
   # Create a flow instance
   flow = ReportFlow()
   
   # Define your input
   input_data = {
       "project_description": "Your project description",
       "outline": "Report structure outline", 
       "audience": "technical"
   }
   
   # Run the flow
   result = flow.kickoff(inputs=input_data)

Configuration
-------------

Input Parameters
~~~~~~~~~~~~~~~~

The system accepts the following input parameters:

.. list-table:: Input Parameters
   :widths: 20 20 60
   :header-rows: 1

   * - Parameter
     - Type
     - Description
   * - project_description
     - string
     - Detailed description of the project to analyze
   * - outline
     - string
     - Comma-separated topics to cover in the report
   * - audience
     - string
     - Target audience: "technical", "business", or "general"

Example Configurations
~~~~~~~~~~~~~~~~~~~~~~

**Technical Software Project**:

.. code-block:: python

   user_input = {
       "project_description": """
       A microservices-based e-commerce platform built with:
       - Node.js and Express for API services
       - React for frontend
       - MongoDB for product catalog
       - Redis for session management
       - Docker for containerization
       """,
       "outline": "Architecture, Microservices Design, Data Flow, Security, Scalability, Deployment",
       "audience": "technical"
   }

**Business Analysis**:

.. code-block:: python

   user_input = {
       "project_description": """
       Digital transformation initiative for a retail company.
       Implementing omnichannel customer experience with
       mobile app, web platform, and in-store integration.
       """,
       "outline": "Business Goals, Market Analysis, Implementation Strategy, ROI Analysis, Risk Assessment",
       "audience": "business"
   }

Crew Configuration
------------------

Each crew can be configured independently:

Sanitize Crew
~~~~~~~~~~~~~

The Sanitize Crew handles input validation and security:

.. code-block:: python

   # Configuration in crews/sanitize_crew/config/agents.yaml
   sanitizer_agent:
     role: "Input Sanitizer and Security Validator"
     goal: "Ensure all inputs are safe and properly formatted"
     backstory: "Expert in cybersecurity and input validation"

Analysis Crew
~~~~~~~~~~~~~

The Analysis Crew performs research and analysis:

.. code-block:: python

   # Configuration in crews/analysis_crew/config/agents.yaml
   analyst_agent:
     role: "Senior Technical Analyst"
     goal: "Conduct comprehensive project analysis"
     backstory: "Experienced system architect and analyst"

Writer Crew
~~~~~~~~~~~

The Writer Crew generates the final report:

.. code-block:: python

   # Configuration in crews/writer_crew/config/agents.yaml
   writer_agent:
     role: "Technical Writer"
     goal: "Create clear, comprehensive documentation"
     backstory: "Skilled technical writer with domain expertise"

Advanced Features
-----------------

RAG Integration
~~~~~~~~~~~~~~~

The system includes Retrieval-Augmented Generation (RAG) capabilities:

.. code-block:: python

   # RAG is automatically used by the Analysis Crew
   # You can configure the RAG tool in tools/rag_tool.py
   
   # Custom RAG queries can be performed:
   from report_generator.tools.rag_tool import RagTool
   
   rag_tool = RagTool()
   results = rag_tool.search("your search query")

MLflow Integration
~~~~~~~~~~~~~~~~~~

Track experiments and evaluate performance:

.. code-block:: bash

   # Run evaluation
   python src/report_generator/evaluation/sanitizecrew_evaluation.py
   
   # View MLflow UI
   mlflow ui

Custom Tools
~~~~~~~~~~~~

You can extend the system with custom tools:

.. code-block:: python

   from crewai_tools import BaseTool
   
   class CustomAnalysisTool(BaseTool):
       name: str = "Custom Analysis Tool"
       description: str = "Performs custom analysis tasks"
       
       def _run(self, query: str) -> str:
           # Your custom logic here
           return "Analysis results"

Output Management
-----------------

Understanding Output Files
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The system generates several output files:

.. code-block:: text

   output/
   ├── final_report.md          # Main report (Markdown format)
   ├── detailed_outline.json    # Structured outline
   ├── project_analysis.json    # Analysis data
   ├── sanitized_query.json     # Sanitized input
   ├── security_check.json      # Security validation
   ├── rag_search_results.md    # RAG search results
   └── generation_summary.md    # Process summary

Customizing Output Format
~~~~~~~~~~~~~~~~~~~~~~~~~

You can modify the output format by editing the Writer Crew configuration:

.. code-block:: yaml

   # In crews/writer_crew/config/tasks.yaml
   writing_task:
     description: "Generate report in desired format"
     expected_output: "Well-structured report in Markdown format"

Best Practices
--------------

Input Preparation
~~~~~~~~~~~~~~~~~

1. **Be Specific**: Provide detailed project descriptions
2. **Structure Outline**: Use clear, logical topic organization  
3. **Define Audience**: Specify the target audience clearly
4. **Include Context**: Add relevant background information

Performance Optimization
~~~~~~~~~~~~~~~~~~~~~~~~

1. **Manage Token Usage**: Be mindful of API token consumption
2. **Cache Results**: Leverage RAG caching for repeated queries
3. **Monitor Memory**: Ensure sufficient system resources
4. **Batch Processing**: Process multiple reports efficiently

Error Handling
~~~~~~~~~~~~~~

The system includes comprehensive error handling:

.. code-block:: python

   try:
       result = flow.kickoff(inputs=input_data)
   except Exception as e:
       print(f"Error generating report: {e}")
       # Handle specific error types
       if "API key" in str(e):
           print("Check your OpenAI API key configuration")

Common Workflows
----------------

Standard Report Generation
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # 1. Prepare input
   # 2. Run the system
   crewai run
   # 3. Review output files
   # 4. Iterate if needed

Evaluation and Testing
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   # Run evaluation tests
   python test_analysis_crew_mlflow.py
   python test_rag.py
   python test_sanitize_only.py

Continuous Integration
~~~~~~~~~~~~~~~~~~~~~~

For automated report generation:

.. code-block:: python

   # Set up automated workflows
   # Configure scheduling
   # Monitor performance metrics
   # Handle failures gracefully

Next Steps
----------

- Explore :doc:`architecture details <architecture/overview>`
- Review :doc:`API reference <api/main>`
- Check out :doc:`advanced examples <examples/advanced_configuration>`
- Learn about :doc:`evaluation and testing <development/evaluation>`
