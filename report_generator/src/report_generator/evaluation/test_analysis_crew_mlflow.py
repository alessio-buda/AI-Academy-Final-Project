"""
MLflow Testing Module for AnalysisCrew Evaluation

This module provides comprehensive testing and evaluation capabilities for CrewAI's AnalysisCrew
using MLflow tracking and automated batch testing. It implements both basic performance metrics 
and advanced LLM-as-a-Judge evaluation to assess the quality and relevance of generated content outlines.

The module integrates with Azure OpenAI services and provides automated tracking of:
- Execution performance metrics (timing, success rates)
- Content quality evaluation via LLM-based judging (1-10 relevance scoring)
- Keyword coverage analysis with intelligent extraction
- Error handling and comprehensive logging
- MLflow experiment tracking and artifact management
- Automated batch testing with multiple queries
- Structured output generation to text files for analysis

Key Features:
- **Single Test Mode**: Execute individual AnalysisCrew evaluations with detailed metrics
- **Batch Testing**: Automatically run multiple test queries and collect aggregated results
- **LLM-as-a-Judge**: Uses Azure OpenAI to evaluate outline relevance and quality
- **Keyword Coverage**: Intelligent extraction and matching of key concepts from queries
- **MLflow Integration**: Complete experiment tracking with metrics, parameters, and artifacts
- **File Output**: Structured summary files for manual analysis and comparison
- **Error Resilience**: Robust error handling that preserves partial results

Output Files:
- MLflow experiments: Detailed tracking in web UI (http://127.0.0.1:5000)
- test_results_summary.txt: Formatted text file with all test metrics and statistics
- generated_outline.json: Individual outline artifacts for each test

Example Usage:
    Run batch evaluation:
        $ python test_analysis_crew_mlflow.py
        
    Monitor results in MLflow UI:
        http://127.0.0.1:5000
        
    Review summary:
        Open test_results_summary.txt for formatted results
        
Test Metrics Tracked:
- execution_CrewAnalysis_time_seconds: Crew execution duration
- execution_crew_success: Binary success indicator (1/0)
- llm_relevance_score_outline_for_user_query: LLM-judged relevance (1-10)
- keyword_coverage_percentage: Percentage of key concepts covered (0-100%)
- judge_evaluation_time: Duration of LLM evaluation process
- keywords_total_count/found_count: Keyword extraction and matching statistics
- coverage_analysis_time: Duration of keyword analysis

Dependencies:
- MLflow server running on localhost:5000
- Azure OpenAI credentials configured in .env
- CrewAI AnalysisCrew properly configured
"""

import os
import time
import json
from datetime import datetime

import mlflow
from dotenv import load_dotenv
from openai import AzureOpenAI

from ..crews.analysis_crew.analysis_crew import AnalysisCrew

# Carica variabili d'ambiente
load_dotenv()

# Configurazione MLflow
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://127.0.0.1:5000")) # punta al server locale
mlflow.set_experiment("AnalysisCrewExperiment") # esperimento dedicato alla AnalysisCrew


def _get_azure_openai_client():
    """Initialize Azure OpenAI client using credentials in file .env.
    
    Creates an Azure OpenAI client instance by reusing the same configuration
    and credentials that CrewAI uses, ensuring consistency across the system.
    
    Returns:
        AzureOpenAI: Configured Azure OpenAI client instance ready for API calls.
        
    Raises:
        ValueError: If required environment variables are missing.
        ConnectionError: If Azure OpenAI endpoint is not reachable.
        
    Note:
        Requires the following environment variables to be set:
        - AZURE_API_KEY: Azure OpenAI API key
        - AZURE_API_VERSION: API version (e.g., "2024-12-01-preview")
        - AZURE_API_BASE: Azure endpoint URL
        - MODEL: Model deployment name (e.g., "gpt-4o-mini")
    """
    return AzureOpenAI(
        api_key=os.getenv("AZURE_API_KEY"),
        api_version=os.getenv("AZURE_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_API_BASE"),
        azure_deployment=os.getenv("MODEL")
    )


def _extract_keywords_from_query(query: str) -> list:
    """Extract important keywords from the original user query using LLM.
    
    Uses Azure OpenAI to intelligently identify the most important keywords,
    technologies, and concepts from the user's request that should be covered
    in the generated outline.
    
    Args:
        query (str): The original user query/request.
        
    Returns:
        list: List of important keywords that should appear in the outline.
        
    Example:
        >>> keywords = _extract_keywords_from_query(
        ...     "Crea docs per sistema inventario con API REST e React"
        ... )
        >>> print(keywords)
        ['sistema di inventario', 'API REST', 'React', 'documentazione', 'gestione prodotti']
    """
    try:
        client = _get_azure_openai_client()
        
        extraction_prompt = f"""
TASK: Extract the most important keywords and concepts from this user request.

USER REQUEST:
"{query}"

INSTRUCTIONS:
- Identify the main subject/domain (e.g., "inventory system", "e-commerce platform")
- Extract specific technologies mentioned (e.g., "API REST", "PostgreSQL", "React")
- Find key functional requirements (e.g., "user management", "order processing", "reporting")
- Include important technical concepts (e.g., "database", "web interface", "automation")
- Return 5-8 most important keywords/phrases
- Use the same language as the original request
- Be specific but not too granular

RESPONSE FORMAT: Return only a JSON array of strings
Example: ["inventory management", "API REST", "PostgreSQL", "React", "product tracking", "order processing", "automated reports"]
"""

        response = client.chat.completions.create(
            model=os.getenv("MODEL", "gpt-4o-mini"),
            messages=[
                {"role": "system", "content": "You are an expert at analyzing user requirements and extracting key concepts. Provide precise, relevant keywords."},
                {"role": "user", "content": extraction_prompt}
            ],
            temperature=0.1,  # Low temperature for consistency
            max_tokens=500    # Enough for keyword list
        )
        
        # Parse the JSON response
        keywords_text = response.choices[0].message.content.strip()
        
        # Clean up potential markdown wrapper
        if keywords_text.startswith('```json'):
            keywords_text = keywords_text.replace('```json', '').replace('```', '').strip()
        elif keywords_text.startswith('```'):
            keywords_text = keywords_text.replace('```', '').strip()
            
        # Parse JSON
        try:
            keywords = json.loads(keywords_text)
            if isinstance(keywords, list) and all(isinstance(k, str) for k in keywords):
                return keywords
            else:
                print(f"⚠️ LLM returned invalid format: {keywords_text}")
                return []
        except json.JSONDecodeError:
            print(f"⚠️ LLM response is not valid JSON: {keywords_text}")
            return []
            
    except Exception as e:
        print(f"❌ Error during keyword extraction: {e}")
        return []


def _calculate_keyword_coverage(original_query: str, outline_content: str) -> dict:
    """Calculate keyword coverage score between query and generated outline.
    
    Measures how well the generated outline covers the important keywords
    and concepts from the original user request. Provides both overall
    percentage and detailed breakdown of found/missing keywords.
    
    Args:
        original_query (str): The original user request/query.
        outline_content (str): The generated outline content as string.
        
    Returns:
        dict: Dictionary containing:
            - coverage_percentage (float): Overall coverage 0-100%
            - total_keywords (int): Total number of keywords to find
            - found_keywords (int): Number of keywords found
            - found_keywords_list (list): List of keywords found in outline
            - missing_keywords_list (list): List of keywords missing from outline
            
    Example:
        >>> result = _calculate_keyword_coverage(
        ...     "Crea sistema inventario con API REST",
        ...     '{"title": "Sistema Inventario", "sections": [...]}'
        ... )
        >>> print(f"Coverage: {result['coverage_percentage']}%")
        Coverage: 75.0%
    """
    # Estrai keywords dalla query originale
    keywords = _extract_keywords_from_query(original_query)
    
    if not keywords:
        return {
            'coverage_percentage': 0.0,
            'total_keywords': 0,
            'found_keywords': 0,
            'found_keywords_list': [],
            'missing_keywords_list': []
        }
    
    # Converti outline in lowercase per ricerca case-insensitive
    outline_lower = outline_content.lower()
    
    # Trova keywords presenti nell'outline
    found_keywords = []
    missing_keywords = []
    
    for keyword in keywords:
        if keyword.lower() in outline_lower:
            found_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)
    
    # Calcola percentuale di copertura
    coverage_percentage = (len(found_keywords) / len(keywords)) * 100
    
    return {
        'coverage_percentage': coverage_percentage,
        'total_keywords': len(keywords),
        'found_keywords': len(found_keywords),
        'found_keywords_list': found_keywords,
        'missing_keywords_list': missing_keywords
    }


def _evaluate_outline_relevance(original_query: str, outline_content: str) -> float:
    """Evaluate outline relevance using LLM-as-a-Judge methodology.
    
    Uses Azure OpenAI to assess how well the generated outline matches the original
    user query. The evaluation considers thematic coherence, technical completeness,
    logical structure, and content relevance.
    
    Args:
        original_query (str): The original user request/query that initiated the outline generation.
        outline_content (str): The generated outline content in JSON string format.
        
    Returns:
        float: Relevance score from 1.0 to 10.0 where:
            - 1.0-3.0: Completely off-topic or irrelevant
            - 4.0-6.0: Partially relevant, missing important elements  
            - 7.0-8.0: Good relevance, covers most aspects
            - 9.0-10.0: Perfectly relevant and comprehensive
            - 0.0: Error occurred during evaluation
            
    Raises:
        Exception: Captures and logs any errors during LLM evaluation, returns 0.0.
        
    Note:
        - Uses low temperature (0.1) for consistent scoring
        - Limited to 10 max tokens for efficient numeric responses
        - Includes fallback scoring (5.0) for invalid LLM responses
        - All errors are logged but don't interrupt the main evaluation flow
        
    Example:
        >>> score = _evaluate_outline_relevance(
        ...     "Create docs for inventory system with REST API",
        ...     '{"title": "Inventory Management System", "sections": [...]}' 
        ... )
        >>> print(f"Relevance: {score}/10")
        Relevance: 8.5/10
    """
    try:
        # Inizializza client Azure OpenAI
        client = _get_azure_openai_client()
        
        # Costruisce il prompt per la valutazione
        evaluation_prompt = f"""
TASK: Evaluate the relevance of this outline against the original request.

ORIGINAL REQUEST:
"{original_query}"

GENERATED OUTLINE:
{outline_content}

EVALUATION CRITERIA:
1. Thematic coherence: Does the outline effectively address the requested topic?
2. Technical completeness: Does it include the technologies and components mentioned in the request?
3. Logical structure: Do the sections and subsections have a logical flow?
4. Content relevance: Is each section useful for achieving the request's objective?

EVALUATION SCALE:
- 1-3: Completely off-topic or irrelevant
- 4-6: Partially relevant, missing important elements
- 7-8: Good relevance, covers most aspects
- 9-10: Perfectly relevant and comprehensive

RESPONSE: Provide ONLY a number from 1 to 10 (e.g.: 8)
"""

        # Chiama Azure OpenAI per la valutazione
        response = client.chat.completions.create(
            model=os.getenv("MODEL", "gpt-4o-mini"),  # Usa stesso modello di CrewAI
            messages=[
                {"role": "system", "content": "Sei un esperto valutatore di contenuti. Fornisci valutazioni precise e obiettive."},
                {"role": "user", "content": evaluation_prompt}
            ],
            temperature=0.1,  # Bassa temperatura per consistenza
            max_tokens=10     # Servono solo pochi token per un numero
        )
        
        # Estrae il punteggio dalla risposta
        score_text = response.choices[0].message.content.strip()
        
        # Converte in float, gestendo possibili errori
        try:
            score = float(score_text)
            # Assicura che sia nel range 1-10
            return max(1.0, min(10.0, score))
        except ValueError:
            print(f"⚠️ LLM ha risposto '{score_text}', non è un numero valido. Uso punteggio default 5.0")
            return 5.0
            
    except Exception as e:
        print(f"❌ Errore durante valutazione LLM-as-a-Judge: {e}")
        return 0.0  # Punteggio di errore


def test_analysis_crew_with_mlflow(query: str):
    """Execute comprehensive AnalysisCrew testing with MLflow tracking and LLM evaluation.
    
    Performs an isolated test of the AnalysisCrew by simulating input from SanitizeCrew
    and measuring both performance metrics and content quality through LLM-as-a-Judge
    evaluation. All metrics and artifacts are automatically tracked in MLflow.
    
    The test workflow includes:
    1. Crew execution with simulated input
    2. Performance metrics collection (execution time, success rate)
    3. LLM-based relevance evaluation of generated outline
    4. MLflow logging of all metrics and artifacts
    5. Comprehensive error handling and logging
    
    Args:
        query (str): The user query/request to be processed by AnalysisCrew.
            This will be passed as "improved_query" to simulate SanitizeCrew output.
    
    Tracked Metrics:
        execution_success (int): Binary success indicator (1=success, 0=failure)
        execution_time_seconds (float): Total crew execution duration
        llm_relevance_score (float): LLM-judged relevance score (1-10)
        judge_evaluation_time (float): Duration of LLM evaluation process
        keyword_coverage_percentage (float): Percentage of keywords covered (0-100%)
        keywords_total_count (int): Total number of keywords extracted from query
        keywords_found_count (int): Number of keywords found in outline
        coverage_analysis_time (float): Duration of keyword coverage analysis
        
    MLflow Artifacts:
        - Generated outline JSON files
        - Error logs (if any failures occur)
        - Execution metadata and timestamps
        
    Returns:
        dict: Comprehensive metrics dictionary containing all test results including:
            - query_input: Original user query
            - execution_CrewAnalysis_time_seconds: Crew execution time
            - execution_crew_success: Success/failure indicator (1/0)
            - llm_relevance_score_outline_for_user_query: LLM relevance score (1-10)
            - keyword_coverage_percentage: Coverage of important keywords (0-100%)
            - found_keywords/missing_keywords: Lists of matched/unmatched keywords
            - status: Overall test status ('success', 'failed', 'exception')
             
    Raises:
        Exception: Captures and logs any exceptions from crew execution but returns
                  error metrics dictionary instead of re-raising exceptions.
                  
    Note:
        - Requires MLflow server running on http://127.0.0.1:5000
        - Automatically handles markdown wrapper cleanup in JSON outputs
        - All errors are logged to MLflow and returned in metrics dictionary
        - Function designed for both single tests and batch processing
        
    Example:
        >>> metrics = test_analysis_crew_with_mlflow(
        ...     "Create docs for inventory system with REST API"
        ... )
        🔍 Avvio AnalysisCrew...
        🤖 Avvio valutazione LLM-as-a-Judge...
        📊 Valutazione LLM completata in 2.34s
        🎯 Punteggio rilevanza: 8.5/10
        ✅ AnalysisCrew completata in 15.67 secondi
        >>> print(f"Success: {metrics['execution_crew_success']}")
        Success: 1
    """
    
    # Input di test simulato (normalmente arriverebbe da SanitizeCrew)
    test_input = {
        "improved_query":  query
    }
    
    with mlflow.start_run(run_name="AnalysisCrew_Simple_Test"):
        # ==================== LOGGING SETUP ====================
        mlflow.set_tag("crew_name", "AnalysisCrew")
        mlflow.set_tag("test_type", "simple_test")
        mlflow.set_tag("timestamp", datetime.utcnow().isoformat())
        
        # Log della query utente come parametro
        mlflow.log_param("user_query", test_input["improved_query"])
        mlflow.log_param("query_length", len(test_input["improved_query"]))
        
        # ==================== ESECUZIONE CREW ====================
        print("🔍 Avvio AnalysisCrew...")
        start_time = time.perf_counter()
        
        try:
            # Inizializza e esegue la crew
            analysis_crew = AnalysisCrew()
            crew_instance = analysis_crew.crew()
            
            # Esegue la crew con l'input di test
            result = crew_instance.kickoff(inputs=test_input)
            
            execution_time = time.perf_counter() - start_time
            
            # ==================== METRICHE ESSENZIALI ====================
            mlflow.log_metric("execution_CrewAnalysis_time_seconds", execution_time)
            mlflow.log_metric("execution_crew_success", 1)
            
            # ==================== LLM-AS-A-JUDGE VALUTAZIONE ====================
            print("🤖 Avvio valutazione LLM-as-a-Judge...")
            judge_start_time = time.perf_counter()
            
            # Legge il file della scaletta generata
            outline_path = "output/detailed_outline.json"
            if os.path.exists(outline_path):
                try:
                    with open(outline_path, 'r', encoding='utf-8') as f:
                        outline_content = f.read().strip()
                    
                    # Rimuovi wrapper markdown se presente
                    if outline_content.startswith('````json'):
                        outline_content = outline_content.replace('````json', '').replace('```json', '').replace('````', '').replace('```', '').strip()
                    elif outline_content.startswith('```json'):
                        outline_content = outline_content.replace('```json', '').replace('```', '').strip()
                    
                    # Valuta la rilevanza usando LLM-as-a-Judge
                    relevance_score = _evaluate_outline_relevance(
                        original_query=test_input["improved_query"],
                        outline_content=outline_content
                    )
                    
                    judge_time = time.perf_counter() - judge_start_time
                    
                    # Registra le metriche LLM
                    mlflow.log_metric("llm_relevance_score_outline_for_user_query", relevance_score)
                    mlflow.log_metric("judge_evaluation_time", judge_time)
                    
                    # Salva la scaletta come artifact MLflow
                    mlflow.log_text(outline_content, "generated_outline.json")
                    
                    print(f"📊 Valutazione LLM completata in {judge_time:.2f}s")
                    print(f"🎯 Punteggio rilevanza: {relevance_score}/10")
                    
                    # ==================== KEYWORD COVERAGE ANALYSIS ====================
                    print("🔍 Avvio analisi copertura keywords...")
                    coverage_start_time = time.perf_counter()
                    
                    # Calcola copertura keywords
                    coverage_result = _calculate_keyword_coverage(
                        original_query=test_input["improved_query"],
                        outline_content=outline_content
                    )
                    
                    coverage_time = time.perf_counter() - coverage_start_time
                    
                    # Registra metriche di copertura
                    mlflow.log_metric("keywords_total_count", coverage_result['total_keywords'])
                    mlflow.log_metric("keywords_found_count", coverage_result['found_keywords'])
                    mlflow.log_metric("keyword_coverage_percentage", coverage_result['coverage_percentage'])
                    mlflow.log_metric("coverage_analysis_time", coverage_time)
                    
                    # Log dettagli come tags per analisi
                    if coverage_result['found_keywords_list']:
                        mlflow.set_tag("found_keywords", ", ".join(coverage_result['found_keywords_list']))
                    if coverage_result['missing_keywords_list']:
                        mlflow.set_tag("missing_keywords", ", ".join(coverage_result['missing_keywords_list']))
                    
                    print(f"📈 Analisi copertura completata in {coverage_time:.2f}s")
                    print(f"📊 Copertura keywords: {coverage_result['coverage_percentage']:.1f}% ({coverage_result['found_keywords']}/{coverage_result['total_keywords']})")
                    if coverage_result['found_keywords_list']:
                        print(f"   ✅ Trovate: {', '.join(coverage_result['found_keywords_list'])}")
                    if coverage_result['missing_keywords_list']:
                        print(f"   ❌ Mancanti: {', '.join(coverage_result['missing_keywords_list'])}")
                    
                except Exception as e:
                    print(f"❌ Errore durante valutazione: {e}")
                    mlflow.log_metric("llm_relevance_score", 0.0)
                    mlflow.log_metric("keyword_coverage_percentage", 0.0)
                    mlflow.set_tag("judge_error", str(e))
            else:
                print(f"❌ File scaletta non trovato: {outline_path}")
                mlflow.log_metric("llm_relevance_score", 0.0)
                mlflow.log_metric("keyword_coverage_percentage", 0.0)
                mlflow.set_tag("judge_error", "outline_file_missing")
            
            print(f"✅ AnalysisCrew completata in {execution_time:.2f} secondi")
            
            # Summary delle metriche registrate
            relevance_score = locals().get('relevance_score', 0.0)
            coverage_percentage = locals().get('coverage_result', {}).get('coverage_percentage', 0.0)
            print(f"📊 Metriche registrate:")
            print(f"   • execution_success: 1")
            print(f"   • execution_time: {execution_time:.2f}s")
            print(f"   • llm_relevance_score: {relevance_score}/10")
            print(f"   • keyword_coverage: {coverage_percentage:.1f}%")
            
            mlflow.set_tag("status", "success")
            
            # Prepara dizionario metriche per output file
            metrics_dict = {
                'query_input': test_input["improved_query"],
                'query_length': len(test_input["improved_query"]),
                'execution_CrewAnalysis_time_seconds': execution_time,
                'execution_crew_success': 1,
                'llm_relevance_score_outline_for_user_query': relevance_score,
                'judge_evaluation_time': locals().get('judge_time', 0.0),
                'keywords_total_count': locals().get('coverage_result', {}).get('total_keywords', 0),
                'keywords_found_count': locals().get('coverage_result', {}).get('found_keywords', 0),
                'keyword_coverage_percentage': coverage_percentage,
                'coverage_analysis_time': locals().get('coverage_time', 0.0),
                'found_keywords': locals().get('coverage_result', {}).get('found_keywords_list', []),
                'missing_keywords': locals().get('coverage_result', {}).get('missing_keywords_list', []),
                'status': 'success'
            }
            
            return metrics_dict
            
        except Exception as e:
            execution_time = time.perf_counter() - start_time
            
            # Log errore
            mlflow.log_metric("execution_CrewAnalysis_time_seconds", execution_time)
            mlflow.log_metric("execution_success", 0)
            mlflow.set_tag("status", "failed")
            mlflow.set_tag("error_type", type(e).__name__)
            
            print(f"❌ Errore durante l'esecuzione: {e}")
            print(f"📊 Metriche registrate: execution_success=0, execution_time={execution_time:.2f}s")
            
            # Prepara dizionario metriche per caso di errore
            metrics_dict = {
                'query_input': test_input["improved_query"],
                'query_length': len(test_input["improved_query"]),
                'execution_CrewAnalysis_time_seconds': execution_time,
                'execution_crew_success': 0,
                'llm_relevance_score_outline_for_user_query': 0.0,
                'judge_evaluation_time': 0.0,
                'keywords_total_count': 0,
                'keywords_found_count': 0,
                'keyword_coverage_percentage': 0.0,
                'coverage_analysis_time': 0.0,
                'found_keywords': [],
                'missing_keywords': [],
                'status': 'failed',
                'error': str(e)
            }
            
            return metrics_dict


def save_metrics_to_file(test_results: list, output_file: str = "evaluation_output/analysis_crew_test_results.txt"):
    """Save test metrics to a formatted text file with comprehensive analysis.
    
    Creates a structured summary file containing all test results, individual metrics,
    and aggregated statistics for AnalysisCrew evaluation. The output format matches
    the user's specified structure for manual analysis and comparison across test runs.
    
    Args:
        test_results (list): List of dictionaries containing test metrics from each
            test run. Each dictionary should include keys like 'query_input',
            'execution_CrewAnalysis_time_seconds', 'llm_relevance_score_outline_for_user_query',
            'keyword_coverage_percentage', etc.
        output_file (str, optional): Path to the output text file. 
            Defaults to "evaluation_output/analysis_crew_test_results.txt".
            
    Returns:
        None: Function saves results to file and prints confirmation message.
        
    Raises:
        IOError: If the output file cannot be created or written to.
        KeyError: If required metric keys are missing from test_results dictionaries.
        
    Note:
        - Creates a formatted text file with TEST 1), TEST 2), etc. sections
        - Includes summary statistics at the end (averages, success rates)
        - Handles both successful and failed test cases appropriately
        - File encoding is UTF-8 to support international characters in queries
        - Automatically creates the evaluation_output directory if it doesn't exist
        
    Example:
        >>> test_results = [
        ...     {'query_input': 'Create presentation...', 'execution_crew_success': 1, ...},
        ...     {'query_input': 'Help with project...', 'execution_crew_success': 1, ...}
        ... ]
        >>> save_metrics_to_file(test_results, 'my_results.txt')
        📄 Risultati salvati in: my_results.txt
        
    Output Format:
        TEST 1)
        query_input = "..."
        query_length = 280
        execution_CrewAnalysis_time_seconds = 17.85
        [additional metrics...]
        
        SUMMARY STATISTICS:
        Total tests: 2
        Successful: 2
        Average execution time: 14.65s
        [additional statistics...]
    """
    try:
        # Se è il path di default, usa path relativo al file corrente
        if output_file == "evaluation_output/analysis_crew_test_results.txt":
            script_dir = os.path.dirname(os.path.abspath(__file__))
            output_file = os.path.join(script_dir, "evaluation_output", "analysis_crew_test_results.txt")
        
        # Crea la directory se non esiste
        output_dir = os.path.dirname(output_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("=" * 70 + "\n")
            f.write("ANALYSIS CREW - TEST RESULTS SUMMARY\n")
            f.write("=" * 70 + "\n\n")
            
            for i, metrics in enumerate(test_results, 1):
                f.write(f"TEST {i})\n\n")
                f.write(f'query_input = "{metrics["query_input"]}"\n')
                f.write(f'query_length = {metrics["query_length"]}\n\n')
                f.write(f'execution_CrewAnalysis_time_seconds = {metrics["execution_CrewAnalysis_time_seconds"]:.2f}\n')
                f.write(f'execution_crew_success = {metrics["execution_crew_success"]}\n\n')
                f.write(f'llm_relevance_score_outline_for_user_query = {metrics["llm_relevance_score_outline_for_user_query"]}\n')
                f.write(f'judge_evaluation_time = {metrics["judge_evaluation_time"]:.2f}\n\n')
                f.write(f'keywords_total_count = {metrics["keywords_total_count"]}\n')
                f.write(f'keywords_found_count = {metrics["keywords_found_count"]}\n')
                f.write(f'keyword_coverage_percentage = {metrics["keyword_coverage_percentage"]:.1f}%\n')
                f.write(f'coverage_analysis_time = {metrics["coverage_analysis_time"]:.2f}\n')
                f.write(f'found_keywords = {metrics["found_keywords"]}\n')
                f.write(f'missing_keywords = {metrics["missing_keywords"]}\n')
                
                if 'error' in metrics:
                    f.write(f'error = "{metrics["error"]}"\n')
                
                f.write(f'status = {metrics["status"]}\n')
                f.write("\n" + "-" * 50 + "\n\n")
            
            # Summary statistics
            successful_tests = [m for m in test_results if m['status'] == 'success']
            if successful_tests:
                f.write("SUMMARY STATISTICS:\n")
                f.write("=" * 30 + "\n")
                f.write(f"Total tests: {len(test_results)}\n")
                f.write(f"Successful: {len(successful_tests)}\n")
                f.write(f"Failed: {len(test_results) - len(successful_tests)}\n\n")
                
                avg_execution_time = sum(m['execution_CrewAnalysis_time_seconds'] for m in successful_tests) / len(successful_tests)
                avg_relevance_score = sum(m['llm_relevance_score_outline_for_user_query'] for m in successful_tests) / len(successful_tests)
                avg_coverage = sum(m['keyword_coverage_percentage'] for m in successful_tests) / len(successful_tests)
                
                f.write(f"Average execution time AnalysisCrew: {avg_execution_time:.2f}s\n")
                f.write(f"Average relevance score: {avg_relevance_score:.1f}/10\n")
                f.write(f"Average keyword coverage: {avg_coverage:.1f}%\n")
        
        # Mostra il path assoluto per essere chiari su dove è stato salvato
        absolute_path = os.path.abspath(output_file)
        print(f"📄 Risultati salvati in: {absolute_path}")
        
    except Exception as e:
        print(f"❌ Errore durante salvataggio file: {e}")


if __name__ == "__main__":
    print("🚀 Test MLflow SEMPLIFICATO per AnalysisCrew")
    # print("Traccia solo: execution_success + execution_time_seconds")
    # print("Server MLflow: http://127.0.0.1:5000")
    print("-" * 50)
    
    tests_query = []

    tests_query.append("Create a presentation on my inventory management system for e-commerce developed with Spring Boot microservices, PostgreSQL database, caching strategies, RabbitMQ for asynchronous messaging and User Interface with React. The system manages 50k products and integrates external APIs for suppliers.")
    tests_query.append("Help with project presentation")
    tests_query.append("Create a detailed presentation for our enterprise human resources management system that includes modules for AI-powered recruitment, " \
                        "biometric attendance tracking, automated payroll processing, 360° performance review system, integrated e-learning platform, advanced analytics dashboards with Power BI, " \
                        "integration with Active Directory and SAP legacy systems, GDPR compliance and privacy regulations, deployment on hybrid Azure cloud with high availability and disaster recovery")
    tests_query.append("Present to executives our new platform for customer management with marketing campaign automation, sales pipeline and analytics. The system improves lead conversion by 30% and includes executive dashboards for company KPIs.")
    #test2 = "Aiutami a presentare la nostra strategia di trasformazione digitale aziendale per migliorare l'efficienza operativa del 40%, ridurre i costi IT e aumentare la soddisfazione clienti attraverso nuovi canali digitali e automazione processi."
    #test3 = "Crea presentazione per progetto importante"
    test = "Crea una docs per un sistema di gestione inventario con API REST, database PostgreSQL e interfaccia web React. Il sistema deve permettere di tracciare prodotti, gestire ordini e generare report automatici."

    # Lista per raccogliere tutti i risultati
    all_test_results = []
    
    print(f"📊 Eseguendo {len(tests_query)} test...")
    
    for i, query in enumerate(tests_query, 1):
        print(f"\n🔍 TEST {i}/{len(tests_query)}")
        print(f"Query: {query[:60]}{'...' if len(query) > 60 else ''}")
        
        try:
            metrics = test_analysis_crew_with_mlflow(query)
            all_test_results.append(metrics)
            print(f"✅ Test {i} completato - Status: {metrics['status']}")
        except Exception as e:
            print(f"❌ Test {i} fallito: {e}")
            # Anche in caso di eccezione, prova a recuperare metriche base
            error_metrics = {
                'query_input': query,
                'query_length': len(query),
                'execution_CrewAnalysis_time_seconds': 0.0,
                'execution_crew_success': 0,
                'llm_relevance_score_outline_for_user_query': 0.0,
                'judge_evaluation_time': 0.0,
                'keywords_total_count': 0,
                'keywords_found_count': 0,
                'keyword_coverage_percentage': 0.0,
                'coverage_analysis_time': 0.0,
                'found_keywords': [],
                'missing_keywords': [],
                'status': 'exception',
                'error': str(e)
            }
            all_test_results.append(error_metrics)
    
    print("-" * 50)
    print("✅ Tutti i test completati!")
    
    # Salva risultati su file
    print("\n📄 Salvando risultati su file...")
    save_metrics_to_file(all_test_results)
    
    print("-" * 50)
    print("✅ Test completato! Controlla MLflow UI per i risultati.")
    print("📄 Controlla anche il file 'test_results_summary.txt' per il riassunto!")
