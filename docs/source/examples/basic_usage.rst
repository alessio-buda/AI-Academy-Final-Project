Basic Usage Examples
====================

This section provides practical examples of using the AI Academy Report Generator for common scenarios.

Example 1: Technical Project Analysis
--------------------------------------

Generate a technical report for a web application project:

**Step 1: Prepare your environment**

Ensure you have completed the :doc:`../installation` and your `.env` file is configured.

**Step 2: Run the report generator**

.. code-block:: bash

   cd report_generator
   crewai run

The system will use the default configuration to generate a sample report.

**Step 3: Customize the input**

To customize for your project, edit ``src/report_generator/main.py``:

.. code-block:: python

   user_input = {
       "project_description": """
       A modern e-commerce web application built with React and Node.js.
       Features include user authentication, product catalog, shopping cart,
       payment processing with Stripe, and an admin dashboard.
       The backend uses Express.js with MongoDB for data storage.
       """,
       "outline": """
       Architecture Overview,
       Frontend Implementation,
       Backend Services,
       Database Design,
       Security Measures,
       Performance Optimization,
       Deployment Strategy
       """,
       "audience": "technical"
   }

Example 2: Business Analysis Report
-----------------------------------

Generate a business-focused analysis:

.. code-block:: python

   user_input = {
       "project_description": """
       Digital transformation initiative for a retail company.
       Implementing omnichannel customer experience with mobile app,
       web platform, inventory management system, and CRM integration.
       Target is to increase customer engagement and operational efficiency.
       """,
       "outline": """
       Business Objectives,
       Market Analysis,
       Technology Stack,
       Implementation Roadmap,
       Risk Assessment,
       Expected ROI,
       Success Metrics
       """,
       "audience": "business"
   }

Example 3: General Purpose Documentation
----------------------------------------

For a broader audience analysis:

.. code-block:: python

   user_input = {
       "project_description": """
       Open-source library for data visualization in Python.
       Provides simple APIs for creating interactive charts and graphs.
       Built on top of matplotlib with additional features for web integration.
       Suitable for data scientists, analysts, and developers.
       """,
       "outline": """
       Library Overview,
       Key Features,
       Installation Guide,
       Basic Examples,
       Advanced Usage,
       Community and Support
       """,
       "audience": "general"
   }

Understanding the Output
------------------------

After running any of these examples, you'll find generated files in the ``output/`` directory:

**Main Outputs:**

.. code-block:: text

   output/
   ├── final_report.md          # The complete generated report
   ├── detailed_outline.json    # Structured content outline  
   ├── project_analysis.json    # Analysis crew results
   └── generation_summary.md    # Process summary

**Analysis Files:**

.. code-block:: text

   output/
   ├── sanitized_query.json     # Cleaned and validated input
   ├── security_check.json      # Security validation results
   └── rag_search_results.md    # Research findings (if available)

Example Output Structure
------------------------

A typical generated report includes:

**Executive Summary**
   High-level overview of the project and key findings

**Detailed Analysis**
   In-depth examination based on your outline topics

**Technical Assessment** (for technical audience)
   Architecture review, code quality, performance considerations

**Business Impact** (for business audience)
   ROI analysis, market positioning, strategic recommendations

**Recommendations**
   Actionable insights and next steps

**Appendices**
   Supporting data, references, and additional resources

Customizing Reports
-------------------

**Audience Types:**

- ``"technical"``: Focuses on architecture, implementation, and technical details
- ``"business"``: Emphasizes ROI, market analysis, and strategic value  
- ``"general"``: Balanced approach suitable for mixed audiences

**Outline Customization:**

The outline parameter accepts comma-separated topics. Examples:

.. code-block:: python

   # For software projects
   "outline": "Architecture, Security, Performance, Scalability, Maintenance"
   
   # For business initiatives  
   "outline": "Strategy, Implementation, Costs, Benefits, Risks, Timeline"
   
   # For research projects
   "outline": "Background, Methodology, Results, Discussion, Conclusions"

**Project Description Tips:**

- Be specific about technologies, frameworks, and tools used
- Include business context and objectives
- Mention target users or stakeholders
- Describe key features and functionality
- Note any constraints or special requirements

Running Multiple Reports
------------------------

You can generate multiple reports by modifying the input and running the system again:

.. code-block:: bash

   # Generate first report
   crewai run
   
   # Copy outputs to a backup location
   mkdir backup_report_1
   copy output\* backup_report_1\
   
   # Modify input in main.py and generate second report
   crewai run

This allows you to compare different analyses or generate reports for different aspects of the same project.

Troubleshooting Common Issues
-----------------------------

**Empty or Generic Reports:**
   - Ensure your project description is detailed and specific
   - Check that your outline covers relevant topics
   - Verify your Azure OpenAI API is working correctly

**Slow Generation:**
   - Large projects may take several minutes to analyze
   - Check your internet connection for RAG searches
   - Monitor your Azure OpenAI usage quotas

**Missing RAG Results:**
   - Verify Qdrant server is running and accessible
   - Check your QDRANT_URL configuration
   - Ensure your embedding model is properly deployed

For more troubleshooting help, see the :doc:`../installation` guide.
