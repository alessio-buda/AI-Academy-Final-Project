AI Academy Final Project - Report Generator
============================================

Welcome to the AI Academy Final Project documentation. This project implements a sophisticated **Multi-Crew AI Report Generation System** using the CrewAI framework.

.. image:: https://img.shields.io/badge/Python-3.10%2B-blue
   :alt: Python Version

.. image:: https://img.shields.io/badge/CrewAI-0.177.0%2B-green
   :alt: CrewAI Version

.. image:: https://img.shields.io/badge/Status-In%20Development-yellow
   :alt: Project Status

Overview
--------

This system implements a **three-stage pipeline architecture** for automated report generation:

.. mermaid::

   graph LR
       A[User Input] --> B[Sanitize Crew]
       B --> C[Analysis Crew]
       C --> D[Writer Crew]
       D --> E[Generated Report + Artifacts]

Key Features
------------

- **Modular Architecture**: Three specialized crews working sequentially
- **AI-Powered Content Generation**: Using advanced LLMs for intelligent report creation  
- **RAG Integration**: Retrieval-Augmented Generation with Qdrant vector database
- **Security & Sanitization**: Input validation and security checks
- **MLflow Integration**: Experiment tracking and evaluation
- **Flexible Output**: Multiple output formats and detailed artifacts

System Components
-----------------

🔒 **Sanitize Crew**
   Input validation, security checks, and query sanitization

🔍 **Analysis Crew**  
   Project analysis, research, and content structuring with RAG support

✍️ **Writer Crew**
   Final report generation and formatting

Documentation Structure
-----------------------

.. toctree::
   :maxdepth: 2
   :caption: Getting Started:

   installation
   quickstart
   usage

.. toctree::
   :maxdepth: 2
   :caption: Architecture:

   architecture/overview
   architecture/flow
   architecture/crews

.. toctree::
   :maxdepth: 2
   :caption: Examples:

   examples/basic_usage

.. toctree::
   :maxdepth: 1
   :caption: Development:

   development/evaluation

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
