# AI-Academy-Final-Project

Per adesso ho diviso in 3 crew sotto consiglio di gpt, la rag non mi funziona va debaggata

















## Multi-Crew AI Report Generation System

This project implements a sophisticated multi-crew AI system for automated report generation using CrewAI framework. The system is designed with a modular architecture consisting of three specialized crews that work sequentially to produce comprehensive technical reports.

## System Architecture Overview

The system follows a **three-stage pipeline architecture**:

```
User Input → Sanitize Crew → Analysis Crew → Writer Crew → Generated Report + Artifacts
```

Each crew is completely independent and specialized for a specific phase of the report generation process.

## Detailed Flow Description

### 🚀 **Entry Point: Main Flow Controller**

**File**: `src/report_generator/main.py`

The system starts with a `ReportFlow` class that inherits from CrewAI's `Flow` framework:

1. **Flow State Management**: Uses `ReportState` Pydantic model to maintain state across the pipeline
2. **Input Collection**: The `get_user_input()` method currently uses hardcoded input (for testing):
   ```python
   user_input = {
       "project_description": "CrewAI is a framework to build AI applications with LLMs and generative AI.",
       "outline": "Scelte architetturali, Diagramma della crew, Esempi pratici, Analisi critica.",
       "audience": "technical",
   }
   ```
3. **Sequential Execution**: The `write()` method orchestrates the entire pipeline

---

### 🛡️ **Stage 1: Sanitize Crew** 
**Purpose**: Security validation and query improvement  
**Location**: `src/report_generator/crews/sanitize_crew/`

#### Crew Composition:
- **2 Agents** (as per requirement)
- **2 Sequential Tasks**
- **LLM**: `azure/o4-mini`

#### Agent 1: Security and Safety Validator
**File**: `sanitize_crew/config/agents.yaml`

**Role**: "Security and Safety Validator for Presentation Guide Generation"
- **Primary Function**: Detect prompt injection attacks, inappropriate content, and security threats
- **Specialized for**: Presentation guide generation context
- **Security Analysis**:
  - ✅ **Legitimate Content**: Project descriptions, technical terminology, business objectives
  - ❌ **Threats to Detect**: Prompt injection patterns, system prompt extraction, malicious code
- **Output**: Detailed security validation report in JSON format

**Task**: `check_input_task`
- **Input**: Raw user input
- **Process**: Comprehensive security analysis with risk categorization
- **Output File**: `output/security_check.json`
- **Expected Output**: JSON containing:
  ```json
  {
    "security_status": "SAFE|UNSAFE",
    "risk_level": "LOW|MEDIUM|HIGH",
    "threats_detected": [],
    "sanitized_input": "cleaned version",
    "security_details": {...},
    "recommendation": "PROCEED|SANITIZE_AND_PROCEED|STOP"
  }
  ```

#### Agent 2: Query Improvement Specialist
**Role**: "Query Improvement Specialist"
- **Primary Function**: Improve and clarify user queries for better processing
- **Decision Logic**:
  - If `security_status = "UNSAFE"` → **HALT PROCESS**
  - If `security_status = "SAFE"` → **IMPROVE QUERY**
- **Query Enhancement**:
  - Clarify ambiguous requests
  - Expand abbreviated descriptions
  - Standardize terminology and format
  - Preserve original intent

**Task**: `sanitize_input_task`
- **Context**: Depends on `check_input_task` output
- **Process**: Query optimization based on security validation
- **Output File**: `output/sanitized_query.json`
- **Expected Output**: JSON containing:
  ```json
  {
    "status": "APPROVED",
    "improved_query": "Enhanced and clarified query",
    "original_query": "Original user input",
    "improvements_made": "Description of improvements"
  }
  ```

---

### 🔍 **Stage 2: Analysis Crew**
**Purpose**: Project analysis and content structuring  
**Location**: `src/report_generator/crews/analysis_crew/`

#### Crew Composition:
- **2 Agents**
- **2 Sequential Tasks**
- **LLM**: `azure/o4-mini`

#### Agent 1: Project Analysis Specialist
**Role**: "Project Analysis Specialist"
- **Primary Function**: Analyze improved queries to extract project details
- **Expertise Areas**:
  - Technical vs business project identification
  - Key component extraction
  - Target audience determination
  - Complexity assessment

**Task**: `analyze_project_task`
- **Input**: `improved_query` from Sanitize Crew
- **Process**: Deep project analysis with Italian output
- **Output File**: `output/project_analysis.json`
- **Expected Output**: JSON containing:
  ```json
  {
    "breve_descrizione_del_progetto": "Italian project description",
    "obiettivi_principali": ["Objective 1", "Objective 2"],
    "componenti_chiave": ["Component 1", "Component 2"],
    "target_audience": "tecnico|non tecnico",
    "complessita_tecnica": "bassa|media|alta",
    "settore_applicativo": "Application sector"
  }
  ```

#### Agent 2: Content Structure Specialist
**Role**: "Content Structure Specialist"
- **Primary Function**: Create detailed outlines with subpoints
- **Structure Guidelines**:
  - 4-6 main sections
  - 3-5 subpoints per section
  - Brief descriptions for each subpoint
  - Logical flow and comprehensive coverage

**Task**: `create_outline_task`
- **Context**: Depends on `analyze_project_task` output
- **Process**: Hierarchical content structure creation
- **Output File**: `output/detailed_outline.json`
- **Expected Output**: JSON containing:
  ```json
  {
    "titolo_report": "Report title in Italian",
    "sezioni": [
      {
        "titolo": "Main section title",
        "descrizione": "Section description",
        "sottosezioni": [
          {
            "titolo": "Subsection title",
            "descrizione": "Detailed subsection description"
          }
        ]
      }
    ],
    "target_audience": "tecnico|non tecnico",
    "stile_comunicazione": "Communication style"
  }
  ```

---

### ✍️ **Stage 3: Writer Crew**
**Purpose**: Information retrieval and final report writing  
**Location**: `src/report_generator/crews/writer_crew/`

#### Crew Composition:
- **2 Agents**
- **2 Sequential Tasks**
- **LLM**: `azure/o4-mini`

#### Agent 1: RAG Information Retrieval Specialist
**File**: `writer_crew/config/agents.yaml`

**Role**: "RAG Information Retrieval Specialist"
- **Primary Function**: **MUST use RagTool** for all information retrieval
- **Critical Constraint**: Never generate fictional content or sources
- **Tool Integration**: Uses `RagTool` which integrates with:
  - **Qdrant Vector Database**: For semantic search
  - **Azure OpenAI Embeddings**: For text vectorization
  - **Document Loader**: Supports PDF, Markdown, HTML files
  
**Process Flow**:
1. **Document Loading**: Loads documents from `src/report_generator/tools/docs/`
2. **Chunking**: Splits documents using `RecursiveCharacterTextSplitter`
3. **Vectorization**: Creates embeddings using Azure OpenAI
4. **Vector Storage**: Stores in Qdrant collection
5. **Hybrid Search**: Combines semantic and keyword search
6. **Result Formatting**: Returns structured document references

**Task**: `rag_search_task`
- **Input**: Detailed outline from Analysis Crew
- **Tools Used**: `RagTool` (mandatory)
- **Process**: For each section/subsection, search relevant documents
- **Output File**: `output/rag_search_results.md`
- **Expected Output**: Markdown with real retrieved documents:
  ```markdown
  ## Section Title
  Description: Section description
  Documents:
  - source: [Real document source]
    document: "[Actual retrieved content]"
  ```

**Current Knowledge Base**:
- `Application Documentation Template - techops.html`
- `crewai_documentation.md` 
- `crewai_best_practices.md`

#### Agent 2: Report Writer
**Role**: "Report Writer"
- **Primary Function**: Transform outlines and sources into comprehensive content
- **Writing Capabilities**:
  - Technical and non-technical adaptation
  - Multi-source synthesis
  - Markdown formatting
  - Audience-appropriate styling

**Task**: `write_report_task`
- **Context**: Depends on `rag_search_task` output
- **Input**: Outline + Retrieved documents + Target audience + Communication style
- **Process**: Comprehensive content writing based on retrieved sources
- **Output File**: `output/final_report.md`
- **Expected Output**: Full markdown report with sections and subsections

---

## 📁 **Output Files Structure**

Each execution generates **7 output files** in the `output/` directory:

1. **`security_check.json`**: Security validation results from Sanitize Crew Agent 1
2. **`sanitized_query.json`**: Improved query from Sanitize Crew Agent 2  
3. **`project_analysis.json`**: Project analysis from Analysis Crew Agent 1
4. **`detailed_outline.json`**: Structured outline from Analysis Crew Agent 2
5. **`rag_search_results.md`**: RAG search results from Writer Crew Agent 1
6. **`final_report.md`**: Complete final report from Writer Crew Agent 2
7. **`generation_summary.md`**: Process summary with metadata and status

## 🔧 **Technical Stack**

### Core Framework
- **CrewAI**: Multi-agent orchestration framework
- **Pydantic**: Data validation and state management
- **Python 3.8+**: Core runtime

### LLM Integration
- **Azure OpenAI**: Primary LLM provider (`azure/o4-mini`)
- **Model Used**: Consistent across all agents for cost optimization

### RAG System Components
- **Qdrant**: Vector database for semantic search
- **LangChain**: Document processing and splitting
- **Azure OpenAI Embeddings**: Text vectorization
- **Document Loaders**: PDF, Markdown, HTML support

### File I/O
- **JSON**: Structured data exchange between crews
- **Markdown**: Final report formatting
- **Multiple Format Support**: PDF, MD, HTML document ingestion

## 🚀 **Execution Process**

### Command Line Execution
```bash
cd report_generator
crewai run
```

### Detailed Execution Flow

1. **Flow Initialization**: `ReportFlow` instantiated with `ReportState`
2. **Input Processing**: Hardcoded input processed (currently for testing)
3. **Sanitize Crew Execution**:
   - Security validation with threat detection
   - Query improvement and standardization
   - JSON output validation and parsing
4. **Analysis Crew Execution**:
   - Project analysis with Italian output
   - Detailed outline creation with hierarchical structure
   - JSON output validation and parsing
5. **Writer Crew Execution**:
   - RAG search using Qdrant and Azure embeddings
   - Final report writing based on retrieved sources
   - Markdown report generation
6. **Output Generation**: 7 files created with complete traceability
7. **Summary Creation**: Process metadata and status report

### Error Handling
- **JSON Parsing**: Robust error handling with fallback mechanisms
- **LLM Failures**: Graceful degradation with error reporting
- **File I/O**: Directory creation and file validation
- **RAG Failures**: Clear error messaging when documents not found

## 🔍 **Current Issues and Improvements**

### Known Issues
1. **RAG Tool Integration**: Agent may not consistently use the RagTool despite configuration
2. **Hardcoded Input**: System uses fixed input for testing purposes
3. **Limited Document Base**: Small knowledge base in `docs/` directory

### Recent Improvements
1. **File Output**: All crew outputs now saved to separate files
2. **Modular Architecture**: Complete separation of crew responsibilities  
3. **Comprehensive Logging**: Detailed process tracking and status reporting
4. **Italian Support**: Proper localization for Analysis Crew outputs

## 📊 **Monitoring and Debugging**

### Output Traceability
Each stage produces traceable outputs:
- **Security**: Complete threat analysis and risk assessment
- **Analysis**: Structured project breakdown and outline
- **Retrieval**: Source documents with exact content matches
- **Writing**: Final comprehensive report

### Debug Information
- **Crew Execution Logs**: Detailed agent interaction logs
- **JSON Validation**: Parse success/failure for each stage
- **Tool Usage**: RAG tool call success/failure tracking
- **File Generation**: Complete file creation and status

This system provides a comprehensive, traceable, and modular approach to AI-powered report generation with strong security validation, intelligent analysis, and robust information retrieval capabilities.