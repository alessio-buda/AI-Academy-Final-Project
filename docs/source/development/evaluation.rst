Evaluation Framework
====================

The AI Academy Report Generator includes a comprehensive evaluation framework to assess the performance and quality of different system components using MLflow tracking and Azure OpenAI-based evaluation.

Overview
--------

The evaluation system focuses on three main areas:

1. **Sanitize Crew Evaluation**: Security detection and input sanitization quality
2. **Analysis Crew Evaluation**: Content quality and analysis accuracy  
3. **RAG Tool Testing**: Retrieval-Augmented Generation functionality

All evaluations use MLflow for experiment tracking, metrics collection, and result visualization.

Sanitize Crew Evaluation
-------------------------

**Location**: ``src/report_generator/evaluation/sanitizecrew_evaluation.py``

This comprehensive evaluation system assesses the security validation and input sanitization processes.

**Key Features:**

- **Agent-specific evaluation**: Separate scoring for input checker and sanitizer agents
- **Weighted scoring**: Security detection (70%) prioritized over query improvement (30%)  
- **Enhanced security metrics**: F2-score favoring recall with graduated risk penalties
- **Context-aware evaluation**: Halt decisions evaluated based on security context
- **False negative penalties**: Missing high-risk threats heavily penalized

**Running the Evaluation:**

.. code-block:: bash

   cd report_generator/src/report_generator/evaluation
   python sanitizecrew_evaluation.py

**Metrics Tracked:**

- **Security Detection Accuracy**: How well the system identifies threats
- **Risk Assessment Precision**: Accuracy of threat level classification
- **Sanitization Quality**: Effectiveness of input cleaning and improvement
- **False Positive/Negative Rates**: Balance between security and usability
- **Agent Performance**: Individual scoring for each crew agent

**Example Output:**

.. code-block:: python

   {
       "overall_score": 0.85,
       "security_detection_score": 0.92,
       "sanitization_score": 0.78,
       "weighted_score": 0.87,
       "security_metrics": {
           "precision": 0.89,
           "recall": 0.94,
           "f2_score": 0.92
       }
   }

Analysis Crew Evaluation
-------------------------

**Location**: ``test_analysis_crew_mlflow.py``

Evaluates the quality and relevance of content analysis and outline generation using LLM-as-a-Judge methodology.

**Key Features:**

- **Performance metrics**: Execution time and resource usage tracking
- **Content quality assessment**: LLM-based evaluation of generated outlines  
- **Azure OpenAI integration**: Consistent with production environment
- **Automated MLflow tracking**: Comprehensive experiment logging

**Running the Evaluation:**

.. code-block:: bash

   cd report_generator
   python test_analysis_crew_mlflow.py

**Evaluation Criteria:**

- **Relevance**: How well the analysis matches the project description
- **Completeness**: Coverage of important project aspects
- **Structure**: Logical organization and flow
- **Technical Accuracy**: Correctness of technical assessments
- **Actionability**: Usefulness of insights and recommendations

**MLflow Integration:**

.. code-block:: python

   # Automatic tracking of:
   - Execution time
   - Token usage
   - Content quality scores
   - Error rates
   - Model performance metrics

RAG Tool Testing
----------------

**Location**: ``test_rag.py``

Simple functionality test for the Retrieval-Augmented Generation tool.

**Running the Test:**

.. code-block:: bash

   cd report_generator
   python test_rag.py

**Test Coverage:**

- **Tool initialization**: Verify RAG tool loads correctly
- **Basic functionality**: Test search and retrieval operations
- **Error handling**: Ensure graceful failure for invalid inputs
- **Integration**: Compatibility with Qdrant vector database

**Example Test Output:**

.. code-block:: text

   Testing RAG tool...
   Tool name: RAG Search Tool
   Tool description: Search for relevant information using vector similarity
   RAG tool result: [Retrieved relevant content about CrewAI architecture]
   Result type: <class 'str'>

Component Testing
-----------------

**Location**: ``test_sanitize_only.py``

Focused testing of individual sanitization components.

**Running Component Tests:**

.. code-block:: bash

   cd report_generator
   python test_sanitize_only.py

**Test Scope:**

- **Input validation**: Security check functionality
- **Sanitization logic**: Query cleaning and improvement
- **Edge cases**: Handling of malformed or malicious inputs
- **Performance**: Response time and resource usage

MLflow Setup and Usage
-----------------------

**Starting MLflow Server:**

.. code-block:: bash

   # Start MLflow tracking server
   mlflow server --host 127.0.0.1 --port 5000
   
   # Access MLflow UI at: http://127.0.0.1:5000

**Environment Configuration:**

Add to your ``.env`` file:

.. code-block:: bash

   # MLflow Configuration (Optional)
   MLFLOW_TRACKING_URI=http://127.0.0.1:5000

**Viewing Results:**

1. Start the MLflow server
2. Run evaluation scripts
3. Open ``http://127.0.0.1:5000`` in your browser
4. Navigate to the relevant experiment
5. Compare runs and analyze metrics

Evaluation Best Practices
--------------------------

**Regular Evaluation Schedule:**

.. code-block:: bash

   # Weekly comprehensive evaluation
   python sanitizecrew_evaluation.py
   python test_analysis_crew_mlflow.py
   python test_rag.py

**Continuous Integration:**

Integrate evaluations into your development workflow:

.. code-block:: bash

   # Before deployment
   ./run_all_evaluations.sh
   
   # Automated testing in CI/CD
   python -m pytest evaluation/

**Performance Monitoring:**

- **Track metrics over time**: Monitor degradation or improvement
- **A/B testing**: Compare different model configurations
- **Error analysis**: Identify common failure patterns  
- **Resource usage**: Monitor computational costs

**Quality Assurance:**

- **Baseline establishment**: Set minimum acceptable performance thresholds
- **Regression testing**: Ensure updates don't break existing functionality
- **Edge case testing**: Validate handling of unusual inputs
- **Security testing**: Verify threat detection capabilities

Custom Evaluation Scripts
--------------------------

You can create custom evaluation scripts for specific use cases:

.. code-block:: python

   import mlflow
   from your_crew import YourCrew
   
   def evaluate_custom_metrics():
       """Custom evaluation function"""
       with mlflow.start_run():
           crew = YourCrew()
           result = crew.kickoff(inputs=test_data)
           
           # Log custom metrics
           mlflow.log_metric("custom_score", calculate_score(result))
           mlflow.log_artifact("output.json")
   
   if __name__ == "__main__":
       evaluate_custom_metrics()

Troubleshooting Evaluations
----------------------------

**Common Issues:**

**MLflow Connection Errors:**
   - Verify MLflow server is running
   - Check MLFLOW_TRACKING_URI configuration
   - Ensure port 5000 is available

**Azure OpenAI Errors:**
   - Validate API keys and endpoints
   - Check model deployment status
   - Monitor usage quotas and rate limits

**Qdrant Connection Issues:**
   - Ensure Qdrant server is running
   - Verify QDRANT_URL configuration
   - Check network connectivity

**Performance Issues:**
   - Monitor system resources during evaluation
   - Reduce batch sizes for large datasets
   - Use parallel processing where appropriate

**Getting Help:**

For evaluation-specific issues:

1. Check MLflow logs for detailed error messages
2. Verify all dependencies are installed correctly
3. Ensure environment variables are properly configured
4. Review the evaluation dataset for data quality issues

The evaluation framework provides comprehensive insights into system performance and helps maintain high quality standards across all components of the report generation system.
