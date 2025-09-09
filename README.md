# AI Academy Final Project - DocuGen AI

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![CrewAI](https://img.shields.io/badge/CrewAI-0.177.0%2B-orange)](https://github.com/joaomdmoura/crewAI)
[![Azure OpenAI](https://img.shields.io/badge/Azure%20OpenAI-GPT--4-green)](https://azure.microsoft.com/en-us/products/ai-services/openai-service)
[![Qdrant](https://img.shields.io/badge/Qdrant-Vector%20DB-purple)](https://qdrant.tech)
[![MLflow](https://img.shields.io/badge/MLflow-Evaluation-yellow)](https://mlflow.org)

> **A multi-agent AI system for automated technical report generation with security validation, intelligent analysis, and RAG-enhanced content creation.**

---















## **Quick Start**

### Prerequisites
- Python 3.10+ 
- Azure OpenAI API access
- Qdrant server (local or cloud)

### Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/alessio-buda/AI-Academy-Final-Project.git
   cd AI-Academy-Final-Project/report_generator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   # or using uv
   uv sync
   ```

3. **Configure environment variables**
   ```bash
   # Create .env file
   AZURE_API_KEY=your_azure_api_key
   AZURE_API_BASE=your_azure_endpoint
   AZURE_API_VERSION=2024-02-15-preview
   MODEL=azure/gpt-4o-mini

   AZURE_OPENAI_EMBEDDING_DEPLOYMENT=your_embedding_deployment
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint

   AZURE_OPENAI_API_KEY=your_azure_api_key
   AZURE_OPENAI_ENDPOINT=your_azure_endpoint
   AZURE_OPENAI_API_VERSION=2024-02-15-preview
   ```

4. **Start Qdrant server**
   ```bash
   # Using Docker (recommended)
   docker run -p 6333:6333 qdrant/qdrant
   
   # Or install locally
   # Follow: https://qdrant.tech/documentation/guides/installation/
   ```

5. **Run the system**
   ```bash
   cd report_generator
   crewai run
   # or
   python -m src.report_generator.main
   ```

---

## **What This System Does**

This project implements a **three-stage AI pipeline** that transforms user queries into comprehensive technical reports through:

1. **Security Validation** - Detects prompt injection and sanitizes input
2. **Intelligent Analysis** - Extracts project details and creates structured outlines  
3. **RAG-Enhanced Writing** - Retrieves relevant documents and generates final reports

---

##  **System Architecture**

### **Multi-Crew Pipeline Architecture**

```
User Input → Security Validation → Project Analysis → Report Generation →  Output Files
     ↓              ↓                    ↓                   ↓               ↓
   Query        Sanitize              Analysis             Writer       Artifacts
               (2 Agents)            (2 Agents)          (2 Agents)
```

### **Technology Stack**

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Framework** | CrewAI + LangChain | Multi-agent orchestration |
| **LLM** | Azure OpenAI GPT-4o-mini | Content generation |
| **Vector DB** | Qdrant | Semantic search & retrieval |
| **Embeddings** | Azure text-embedding-ada-002 | Document vectorization |
| **Evaluation** | MLflow | Performance tracking |
| **Evaluation** | RAGAS | Performance tracking |
| **Documentation** | Sphinx | API & user documentation |

---

##  **Detailed Component Breakdown**

### **Stage 1:  Sanitize Crew** 
*Location*: `src/report_generator/crews/sanitize_crew/`

**Purpose**: Security validation and query improvement

#### **Agents & Tasks**:
- **Security Validator**: Detects prompt injection, inappropriate content, security threats
  - **Output**: `output/security_check.json` - Security validation results
- **Query Improver**: Enhances and clarifies user queries for better processing
  - **Output**: `output/sanitized_query.json` - Improved query data

#### **Security Features**:
-  Prompt injection detection
-  Content appropriateness validation  
- Context-aware security analysis
-  Risk level assessment (LOW/MEDIUM/HIGH)

---

### **Stage 2:  Analysis Crew**
*Location*: `src/report_generator/crews/analysis_crew/`

**Purpose**: Project analysis and content structuring

#### **Agents & Tasks**:
- **Project Analyzer**: Extracts project details, determines complexity and audience
  - **Output**: `output/project_analysis.json` - Project analysis in Italian
- **Content Structurer**: Creates hierarchical outlines with 4-6 main sections
  - **Output**: `output/detailed_outline.json` - Detailed report structure

#### **Analysis Features**:
-  Target audience detection (technical/non-technical)
-  Project complexity assessment  
-  Hierarchical outline generation

---

### **Stage 3:  Writer Crew**
*Location*: `src/report_generator/crews/writer_crew/`

**Purpose**: Information retrieval and final report writing

#### **Agents & Tasks**:
- **RAG Searcher**: **MUST use RagTool** for document retrieval
  - **Tools**: `RagTool` with Qdrant hybrid search
  - **Output**: `output/rag_search_results.md` - Retrieved documents with sources
- **Report Writer**: Synthesizes outline + sources into comprehensive content
  - **Output**: `output/final_report.md` - Complete markdown report

#### **RAG Features**:
-  Semantic + keyword hybrid search
-  MMR (Maximum Marginal Relevance) diversification
-  Multi-format document support (PDF, MD, HTML)
-  Source citation tracking

---

##  **Knowledge Base & RAG System**

### **Document Sources**
*Location*: `src/report_generator/tools/docs/`

- **Technical Documentation**: HTML templates, API references
- **Best Practices**: CrewAI methodology, implementation patterns
- **Examples**: Code samples, configuration templates

### **RAG Pipeline Features**

| Feature | Implementation | Benefit |
|---------|---------------|---------|
| **Vector Search** | Qdrant + Azure embeddings | Semantic similarity matching |
| **Keyword Search** | Text-based filtering | Exact term matching |
| **Hybrid Fusion** | Weighted score combination | Best of both approaches |
| **Result Diversity** | MMR algorithm | Avoids redundant content |
| **Source Tracking** | Metadata preservation | Complete citation trail |

### **Configuration Options**

```python
# Customizable search parameters
chunk_size = 700          # Text chunk size
top_n_semantic = 30       # Semantic search candidates  
top_n_text = 100         # Text search candidates
final_k = 5              # Final results returned
alpha = 0.75             # Semantic vs text weight
mmr_lambda = 0.6         # Diversity vs relevance balance
```

---

## **Output Structure**

Each execution generates **7 comprehensive files**:

```
output/
├──  security_check.json      # Security validation results
├──  sanitized_query.json     # Improved user query  
├──  project_analysis.json    # Project analysis (Italian)
├──  detailed_outline.json    # Hierarchical report structure
├──  rag_search_results.md    # Retrieved documents with citations
├──  final_report.md          # Complete generated report
└──  generation_summary.md    # Process metadata & status
```

### **File Details**

| File | Content | Format | Purpose |
|------|---------|--------|---------|
| `security_check.json` | Threat analysis, risk level, security status | JSON | Audit trail for security validation |
| `sanitized_query.json` | Improved query, original input, modifications | JSON | Query enhancement documentation |
| `project_analysis.json` | Project details, audience, complexity (Italian) | JSON | Structured analysis for outline creation |
| `detailed_outline.json` | Sections, subsections, descriptions (Italian) | JSON | Blueprint for report structure |
| `rag_search_results.md` | Retrieved documents with source citations | Markdown | Knowledge base search results |
| `final_report.md` | Complete report with sections and sources | Markdown | Final deliverable |
| `generation_summary.md` | Process flow, status, metadata, timestamps | Markdown | Execution summary and audit |

---

##  **Evaluation & Monitoring System**

### **MLflow Integration**
*Location*: `report_generator/evaluation/`

The system includes comprehensive evaluation capabilities:

#### **Evaluation Metrics**

**Security Metrics**:
- `security_completeness` - Thoroughness of security analysis
- `confidence_score` - Assessment confidence level
- `risk_classification` - Risk level accuracy
- `threats_detected` - Number of security threats found

**Quality Metrics**:
- `sanitization_success` - Query improvement effectiveness
- `length_improvement` - Query enhancement ratio
- `overall_score` - Combined performance metric
- `expectation_match` - Result vs expected outcome

### **RAGAS Integration**

*Location*: `report_generator/evaluation/`

The system includes comprehensive evaluation capabilities for RAG pipelines:

**Metrics**
- **Context Recall**: measures whether retrieved passages cover what is needed to answer the question
- **Faithfulness**: measures how much the answer is supported by the retrieved passages
- **Answer Relevancy**: measures how much the answer adheres to the question

All metrics consist of values in the 0-1 range. Evaluation is entrusted to an LLM that operates as a judge (LLM-as-a-judge).


#### **Evaluation Metrics**

#### **Usage Examples**

```bash
# Run simple evaluation
python example_evaluation.py

# View results in MLflow UI
mlflow ui
# Open: http://localhost:5000

# Batch evaluation
python test_analysis_crew_mlflow.py
```

#### **Performance Benchmarks**

- **Score > 0.8**: Excellent performance 
- **Score 0.6-0.8**: Good performance 
- **Score < 0.6**: Needs improvement 

---

##  **Documentation System**

### **Sphinx Documentation**
*Location*: `docs/`

Professional documentation with:

-  **API Reference** - Auto-generated from docstrings
-  **Quick Start Guide** - Installation and setup
-  **Architecture Guide** - System design and components
-  **Examples** - Usage patterns and code samples
-  **Development Guide** - Contributing and testing

#### **Build Documentation**

```bash
cd docs
python build_docs.py build    # Build HTML docs
python build_docs.py serve    # Serve locally
python build_docs.py watch    # Live reload development
```

---

##  **Development & Customization**

### **Project Structure**

```
AI-Academy-Final-Project/
├──  report_generator/           # Main application
│   ├──  pyproject.toml         # Dependencies & config
│   ├──  uv.lock                # Locked dependencies  
│   ├──  src/report_generator/
│   │   ├──  main.py            # Flow controller & entry point
│   │   ├──  crews/             # Three specialized crews
│   │   │   ├──  sanitize_crew/  # Security validation
│   │   │   ├──  analysis_crew/  # Project analysis  
│   │   │   └──  writer_crew/    # Report writing
│   │   ├──  tools/             # RAG system & utilities
│   │   │   ├──  rag_tool.py    # CrewAI RAG tool wrapper
│   │   │   ├──  rag_qdrant_hybrid.py # Hybrid search engine
│   │   │   └──  docs/          # Knowledge base documents
│   │   └──  evaluation/        # MLflow evaluation system
│   └──  output/               # Generated artifacts (7 files)
├──  docs/                     # Sphinx documentation
│   ├──  source/              # Documentation source files  
│   ├──  build_docs.py        # Build automation script
│   └──  _build/html/          # Generated documentation
└──  README.md                # This comprehensive guide
```


##  **Configuration & Customization**
```

#### **Crew Behavior**
```yaml
# In crews/*/config/agents.yaml
agents:
  specialist:
    role: "Custom Role"
    goal: "Custom objective"  
    backstory: "Detailed context and instructions"
    llm: azure/gpt-4o-mini    # Or different model
```

---

## **Troubleshooting Guide**

### **Common Issues**

#### **1. RAG Tool Not Working**
```bash
# Check Qdrant connection
curl http://localhost:6333/collections

# Verify document loading
python -c "from src.report_generator.tools.rag_qdrant_hybrid import load_docs_from_directory; print(len(load_docs_from_directory('src/report_generator/tools/docs')))"
```

#### **2. Azure OpenAI Errors**
```bash
# Test API connection
python -c "from langchain_openai import AzureOpenAIEmbeddings; e = AzureOpenAIEmbeddings(model='text-embedding-ada-002'); print(len(e.embed_query('test')))"
```

#### **3. Missing Output Files**
- Check crew execution logs for errors
- Verify JSON parsing in main.py
- Ensure output directory permissions

#### **4. Performance Issues**
- Reduce `chunk_size` for faster processing
- Lower `top_n_semantic` for quicker searches  
- Enable `use_cache` for embeddings
- Use smaller batch sizes in upsert_chunks()

### **Debug Mode**

```python
# Enable verbose logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Test individual components
from src.report_generator.crews.sanitize_crew.sanitize_crew import SanitizeCrew
crew = SanitizeCrew()
result = crew.crew().kickoff(inputs={"user_input": "test"})
```

---

##  **Contributing & Development**

### **Development Workflow**

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes** with proper documentation and tests
4. **Run evaluation**: `python test_analysis_crew_mlflow.py`  
5. **Build docs**: `cd docs && python build_docs.py build`
6. **Submit PR** with clear description

### **Code Standards**

- **Type hints**: Use for all function parameters and returns
- **Docstrings**: Google-style docstrings for all public methods
- **Testing**: Add evaluation cases for new features
- **Documentation**: Update relevant .rst files in docs/

### **Architecture Principles**

- **Modularity**: Each crew should be completely independent
- **Traceability**: All outputs must be saved to files
- **Security**: All inputs must pass through Sanitize Crew
- **Citations**: All generated content must reference sources

---

## **License & Credits**

### **License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### **Acknowledgments**

- **CrewAI Framework** - Multi-agent orchestration
- **Azure OpenAI** - Large language models and embeddings  
- **Qdrant** - Vector database and similarity search
- **LangChain** - Document processing and RAG utilities
- **MLflow** - Experiment tracking and evaluation
- **Sphinx** - Documentation generation

### **Contributors**

- **Developers**:
- [Tiziano Bardini](https://github.com/tiziano97)
- [Alessio Buda](https://github.com/alessio-buda)
- [Emanuela Rremilli](https://github.com/em-rg)
- [Danilo Santo](https://github.com/DaniloSanto01)
- **AI Academy** - Educational framework and guidance

---

##  **Support & Contact**

### **Getting Help**

1. **Check Documentation**: `docs/_build/html/index.html`
2. **Review Examples**: See `evaluation/` directory
3. **Open Issues**: Use GitHub Issues for bugs and feature requests
4. **Discussions**: Use GitHub Discussions for questions

### **Resources**

- **GitHub Repository**: https://github.com/alessio-buda/AI-Academy-Final-Project
- **Documentation**: Available in `docs/_build/html/`
- **CrewAI Documentation**: https://docs.crewai.com/
- **Qdrant Documentation**: https://qdrant.tech/documentation/
- **Azure OpenAI**: https://learn.microsoft.com/en-us/azure/cognitive-services/openai/

---

---

*This comprehensive guide represents a production-ready multi-agent AI system with security validation, intelligent analysis, and knowledge-enhanced report generation. The system demonstrates advanced AI orchestration, RAG implementation, and professional software development practices.*
