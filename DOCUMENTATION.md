# AI Academy Report Generator - Complete Documentation

## Table of Contents

1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Installation Guide](#installation-guide)
4. [Quick Start](#quick-start)
5. [Usage Guide](#usage-guide)
6. [Configuration](#configuration)
7. [Architecture Details](#architecture-details)
8. [API Reference](#api-reference)
9. [Development Guide](#development-guide)
10. [Troubleshooting](#troubleshooting)
11. [Performance Optimization](#performance-optimization)
12. [Security Considerations](#security-considerations)

## Overview

The AI Academy Report Generator is a sophisticated multi-crew AI system designed for automated report generation using the CrewAI framework. The system implements a modular, three-stage pipeline architecture where specialized AI crews work sequentially to produce comprehensive, professional reports.

### Key Features

- **Modular Architecture**: Three specialized crews working sequentially for input sanitization, analysis, and report writing
- **AI-Powered Content Generation**: Leveraging advanced large language models for intelligent report creation
- **RAG Integration**: Retrieval-Augmented Generation with Qdrant vector database for enhanced knowledge capabilities
- **Security-First Design**: Comprehensive input validation and security checks before processing
- **MLflow Integration**: Built-in experiment tracking and evaluation capabilities
- **Flexible Output**: Multiple output formats with detailed artifacts and process summaries
- **Professional Quality**: Enterprise-grade documentation and reporting suitable for client deliverables

### System Requirements

- **Python**: 3.10 or higher
- **Memory**: Minimum 4GB RAM (8GB+ recommended for optimal performance)
- **Storage**: 2GB free disk space for dependencies and output files
- **Network**: Stable internet connection for API calls and model access
- **Dependencies**: UV package manager (recommended) or pip

## System Architecture

### High-Level Architecture

The system follows a three-stage pipeline architecture designed for maximum modularity and reliability:

```
User Input → Sanitize Crew → Analysis Crew → Writer Crew → Generated Report + Artifacts
```

### Core Components

#### 1. Flow Controller
**Location**: `src/report_generator/main.py`

The `ReportFlow` class orchestrates the entire pipeline using CrewAI's Flow framework:

- **State Management**: Maintains consistent data flow across all crews using Pydantic models
- **Sequential Execution**: Ensures proper order of operations and error handling
- **Output Coordination**: Manages artifact generation and final report compilation

#### 2. Sanitize Crew
**Purpose**: Security validation and input optimization
**Location**: `src/report_generator/crews/sanitize_crew/`

**Components**:
- **Security Validator Agent**: Detects security threats, prompt injection attacks, and inappropriate content
- **Query Improvement Specialist**: Enhances and clarifies user queries for optimal processing
- **Output**: Security validation report and sanitized input (`output/security_check.json`, `output/sanitized_query.json`)

#### 3. Analysis Crew
**Purpose**: Comprehensive project analysis and research
**Location**: `src/report_generator/crews/analysis_crew/`

**Components**:
- **Senior Technical Analyst**: Conducts in-depth project analysis and architectural assessment
- **RAG Tool Integration**: Leverages Qdrant vector database for knowledge retrieval
- **Research Capabilities**: Performs intelligent information gathering and synthesis
- **Output**: Detailed analysis report and structured outline (`output/project_analysis.json`, `output/detailed_outline.json`)

#### 4. Writer Crew
**Purpose**: Professional report generation and formatting
**Location**: `src/report_generator/crews/writer_crew/`

**Components**:
- **Technical Writer Agent**: Creates comprehensive, well-structured reports
- **Format Specialist**: Ensures proper formatting and professional presentation
- **Quality Assurance**: Validates content quality and completeness
- **Output**: Final report and generation summary (`output/final_report.md`, `output/generation_summary.md`)

### Technology Stack

**Core Framework**:
- CrewAI: Multi-agent orchestration framework
- LangChain: LLM integration and tooling
- Pydantic: Data validation and serialization
- Python 3.10+: Runtime environment

**AI & ML Components**:
- Azure OpenAI GPT Models: Primary language models for text generation
- Qdrant: Vector database for RAG implementation
- LangChain Tools: Integration with various AI services
- MLflow: Experiment tracking and model evaluation

**Infrastructure**:
- FastAPI: API framework (for future web interface)
- Docker: Containerization support
- UV/Poetry: Dependency management

## Installation Guide

### Prerequisites

Before installation, ensure you have:

- Python 3.10+ installed
- Access to Azure OpenAI Service
- Qdrant vector database server (local or cloud)
- Git for repository cloning
- Minimum 4GB RAM available
- Stable internet connection

### Step 1: Install UV Package Manager

If UV is not installed:

```powershell
# Windows PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Alternative: Using pip
pip install uv
```

### Step 2: Clone Repository

```bash
git clone https://github.com/alessio-buda/AI-Academy-Final-Project.git
cd AI-Academy-Final-Project/report_generator
```

### Step 3: Install Dependencies

```bash
# Using UV (recommended)
uv sync

# Alternative: Using pip
pip install -e .
```

### Step 4: Qdrant Database Setup

Choose one of the following options:

**Option A: Qdrant Cloud (Recommended for Production)**
1. Visit [Qdrant Cloud](https://cloud.qdrant.io/)
2. Create a free account
3. Create a new cluster
4. Note your cluster URL and API key

**Option B: Local Qdrant Server**
```bash
# Using Docker
docker run -p 6333:6333 qdrant/qdrant

# Or download binary from: https://github.com/qdrant/qdrant/releases
```

### Step 5: Environment Configuration

Create and configure the environment file:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# Model Configuration
MODEL=gpt-4

# Azure OpenAI Configuration (Required)
AZURE_OPENAI_API_KEY=your_azure_openai_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=text-embedding-ada-002

# Qdrant Vector Database Configuration (Required)
QDRANT_URL=http://localhost:6333  # For local Qdrant
# QDRANT_URL=https://your-cluster.qdrant.io  # For Qdrant Cloud
# QDRANT_API_KEY=your_qdrant_api_key_here     # For Qdrant Cloud only

# Serper API for web search (Optional)
SERPER_API_KEY=your_serper_api_key_here
```

### Step 6: Verification

Test the installation:

```bash
crewai run
```

If successful, the system will generate a sample report with output files in the `output/` directory.

## Quick Start

### Basic Report Generation

1. **Run with default configuration**:
   ```bash
   crewai run
   ```

2. **Review generated outputs**:
   ```
   output/
   ├── final_report.md          # Main generated report
   ├── detailed_outline.json    # Structured outline
   ├── project_analysis.json    # Analysis results
   ├── sanitized_query.json     # Sanitized input
   ├── security_check.json      # Security validation
   ├── rag_search_results.md    # RAG search results
   └── generation_summary.md    # Process summary
   ```

### Custom Report Generation

Modify the input in `src/report_generator/main.py`:

```python
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
```

## Usage Guide

### Command Line Interface

**Basic Usage**:
```bash
# Run with default configuration
crewai run

# Run specific components
python -m report_generator.main
```



### Programmatic Usage

```python
from report_generator.main import ReportFlow

# Create flow instance
flow = ReportFlow()

# Define input parameters
input_data = {
    "project_description": "Detailed project description",
    "outline": "Report structure outline",
    "audience": "technical"  # or "business", "general"
}

# Execute the flow
result = flow.kickoff(inputs=input_data)
```

### Input Parameters

| Parameter | Type | Description | Required |
|-----------|------|-------------|----------|
| project_description | string | Detailed description of the project to analyze | Yes |
| outline | string | Comma-separated topics to cover in the report | Yes |
| audience | string | Target audience: "technical", "business", or "general" | Yes |

### Example Configurations

**Technical Software Project**:
```python
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
```

**Business Analysis**:
```python
user_input = {
    "project_description": """
    Digital transformation initiative for a retail company.
    Implementing omnichannel customer experience with
    mobile app, web platform, and in-store integration.
    """,
    "outline": "Business Goals, Market Analysis, Implementation Strategy, ROI Analysis, Risk Assessment",
    "audience": "business"
}
```

## Configuration

### Crew Configuration

Each crew can be independently configured through YAML files:

**Sanitize Crew Configuration**:
```yaml
# crews/sanitize_crew/config/agents.yaml
sanitizer_agent:
  role: "Input Sanitizer and Security Validator"
  goal: "Ensure all inputs are safe and properly formatted"
  backstory: "Expert in cybersecurity and input validation"
  llm: azure/gpt-4-mini
```

**Analysis Crew Configuration**:
```yaml
# crews/analysis_crew/config/agents.yaml
analyst_agent:
  role: "Senior Technical Analyst"
  goal: "Conduct comprehensive project analysis"
  backstory: "Experienced system architect and analyst"
  llm: azure/gpt-4
```

**Writer Crew Configuration**:
```yaml
# crews/writer_crew/config/agents.yaml
writer_agent:
  role: "Technical Writer"
  goal: "Create clear, comprehensive documentation"
  backstory: "Skilled technical writer with domain expertise"
  llm: azure/gpt-4
```

### Advanced Configuration

**RAG Tool Configuration**:
```python
# Custom RAG queries
from report_generator.tools.rag_tool import RagTool

rag_tool = RagTool()
results = rag_tool.search("your search query")
```

**MLflow Tracking**:
```bash
# Run evaluation
python src/report_generator/evaluation/sanitizecrew_evaluation.py

# View MLflow UI
mlflow ui
```

## Architecture Details

### Data Flow Architecture

The system uses a Pydantic-based state model to maintain data consistency:

```python
class ReportState(BaseModel):
    """Shared state across all crews."""
    user_input: Dict[str, Any]
    sanitized_input: Optional[Dict[str, Any]] = None
    security_check: Optional[Dict[str, Any]] = None
    analysis_result: Optional[Dict[str, Any]] = None
    final_report: Optional[str] = None
```

### Communication Patterns

**Sequential Processing**: Each crew processes the output of the previous crew in a linear fashion.

**State Persistence**: All intermediate results are stored in the shared state for debugging and analysis.

**Error Propagation**: Errors are gracefully handled and propagated through the pipeline with appropriate fallback mechanisms.

### Scalability Considerations

**Horizontal Scaling**:
- Each crew can run on separate machines
- Multiple instances can handle concurrent requests
- Easy conversion to microservices architecture

**Performance Optimization**:
- RAG results and intermediate outputs are cached
- Non-blocking operations where possible
- Efficient handling of large language model operations
- Intelligent token usage to minimize costs

## API Reference

### Core Classes

#### ReportFlow
Main flow controller for the report generation pipeline.

**Methods**:
- `get_user_input()`: Initialize the flow with user input
- `sanitize_input(state)`: Sanitize and validate user input
- `analyze_project(state)`: Perform project analysis with RAG support
- `write_report(state)`: Generate the final report

#### ReportState
Shared state model across all crews.

**Attributes**:
- `user_input`: Original user input data
- `sanitized_input`: Sanitized and validated input
- `security_check`: Security validation results
- `analysis_result`: Project analysis data
- `final_report`: Generated report content

### Tool Integration

#### RagTool
Retrieval-Augmented Generation tool for knowledge enhancement.

**Methods**:
- `search(query)`: Perform semantic search in the vector database
- `add_documents(documents)`: Add new documents to the knowledge base

## Development Guide

### Project Structure

```
report_generator/
├── src/
│   └── report_generator/
│       ├── main.py                    # Main flow controller
│       ├── crews/                     # Crew implementations
│       │   ├── sanitize_crew/
│       │   ├── analysis_crew/
│       │   └── writer_crew/
│       ├── tools/                     # Custom tools
│       │   ├── rag_tool.py
│       │   └── ...
│       └── evaluation/                # Testing and evaluation
├── output/                           # Generated artifacts
├── pyproject.toml                    # Project configuration
└── README.md
```



### Testing Framework

**Unit Tests**:
```bash
# Test individual components
python test_sanitize_only.py
python test_rag.py
```

**Integration Tests**:
```bash
# Test full pipeline
python test_analysis_crew_mlflow.py
```

**Evaluation Tests**:
```bash
# Run evaluation suite
python src/report_generator/evaluation/sanitizecrew_evaluation.py
```

### Custom Tool Development

```python
from crewai_tools import BaseTool

class CustomAnalysisTool(BaseTool):
    name: str = "Custom Analysis Tool"
    description: str = "Performs custom analysis tasks"
    
    def _run(self, query: str) -> str:
        # Your custom logic here
        return "Analysis results"
```

## Troubleshooting

### Common Issues and Solutions

#### Installation Problems

**Import Errors**:
- Ensure the package is installed in editable mode: `pip install -e .`
- Check Python version compatibility (3.10+ required)
- Verify all dependencies are properly installed

**Memory Issues**:
- Ensure at least 4GB RAM is available
- Close unnecessary applications before running
- Consider using smaller models for development

#### Configuration Issues

**API Key Problems**:
- Verify Azure OpenAI service is active and accessible
- Check that the endpoint URL is correct
- Ensure the API version matches your deployment
- Confirm your models are properly deployed in Azure

**Qdrant Connection Issues**:
- **Local Qdrant**: Ensure server is running on port 6333
- **Qdrant Cloud**: Verify cluster URL and API key are correct
- **Network**: Check firewall settings and connectivity
- **Configuration**: Ensure QDRANT_URL is properly formatted

#### Runtime Errors

**Token Limit Exceeded**:
- Review input length and complexity
- Consider breaking large inputs into smaller chunks
- Monitor token usage in Azure OpenAI portal

**Generation Quality Issues**:
- Verify model deployments are using appropriate versions
- Check that the embedding model is properly configured
- Review and adjust agent prompts if necessary

### Debugging Tips

**Enable Verbose Logging**:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

**Check Output Files**:
- Review `output/security_check.json` for input validation issues
- Examine `output/generation_summary.md` for process details
- Analyze `output/project_analysis.json` for analysis problems

**Validate Environment**:
```bash
# Test Azure OpenAI connection
python -c "import openai; print('OpenAI library imported successfully')"

# Test Qdrant connection
curl http://localhost:6333/health  # For local Qdrant
```

### Getting Help

For additional support:

1. Review the troubleshooting logs in the `output/` directory
2. Check the project's GitHub issues page
3. Consult the CrewAI documentation for framework-specific issues
4. Verify Azure OpenAI service status and quotas

## Performance Optimization

### System Optimization

**Memory Management**:
- Monitor memory usage during report generation
- Close unnecessary applications to free up RAM
- Consider using pagination for large document processing

**Token Optimization**:
- Monitor Azure OpenAI token consumption
- Optimize prompts to reduce token usage
- Implement intelligent caching for repeated queries

**Processing Speed**:
- Use appropriate model sizes for your use case
- Implement parallel processing where possible
- Cache intermediate results to avoid recomputation

### Scalability Best Practices

**Horizontal Scaling**:
- Deploy crews on separate machines for large workloads
- Implement load balancing for concurrent requests
- Use message queues for asynchronous processing

**Resource Management**:
- Implement proper error handling and recovery
- Monitor system resources and API quotas
- Set up alerting for system failures

## Security Considerations

### Input Security

The Sanitize Crew implements comprehensive security measures:

**Security Validation**:
- Detection of prompt injection attacks
- Content filtering for inappropriate material
- Schema validation for input structure
- Risk assessment and categorization

**Data Privacy**:
- No permanent storage of user inputs
- Anonymization of personal information
- Secure transmission protocols (HTTPS)
- Access control mechanisms

### Operational Security

**API Security**:
- Secure storage of API keys and credentials
- Regular rotation of access tokens
- Monitoring of API usage and anomalies
- Rate limiting to prevent abuse

**Infrastructure Security**:
- Regular security updates for dependencies
- Secure container configurations
- Network security best practices
- Audit logging for all operations

### Best Practices

**Development Security**:
- Use environment variables for sensitive configuration
- Implement proper error handling without exposing internals
- Use HTTPS for all communications
- Implement proper authentication and authorization
- Regular security assessments and penetration testing
- Incident response procedures and monitoring

---

## Conclusion

The AI Academy Report Generator represents a sophisticated, enterprise-ready solution for automated report generation. Its modular architecture, comprehensive security features, and professional output quality make it suitable for client deliverables and production environments.

The system's design emphasizes reliability, scalability, and maintainability, ensuring it can adapt to evolving requirements while maintaining high standards of security and performance.

For additional support, detailed API documentation, or feature requests, please refer to the project's GitHub repository or contact the development team.

---

**Document Version**: 1.0  
**Last Updated**: September 8, 2025  
**Project Repository**: [AI-Academy-Final-Project](https://github.com/alessio-buda/AI-Academy-Final-Project)
