"""
MLflow Testing Module for AnalysisCrew Evaluation

SISTEMA DI VALUTAZIONE INTELLIGENTE PER CREWAI
==============================================

Questo modulo implementa un sistema completo di testing e valutazione per CrewAI
che combina metriche di performance tradizionali con valutazione intelligente 
basata su LLM (Large Language Models).

ARCHITETTURA:
1. ESECUZIONE: Testa la AnalysisCrew in isolamento
2. VALUTAZIONE: Usa 2 approcci per misurare la qualità:
   - LLM-as-a-Judge: Valutazione semantica della rilevanza (1-10)
   - Keyword Coverage: Analisi della completezza degli argomenti (0-100%)
3. TRACKING: Registra tutto su MLflow per monitoraggio e benchmark

METRICHE TRACCIATE:
- Performance: execution_time, execution_success
- Qualità: llm_relevance_score, keyword_coverage_percentage  
- Dettagli: keywords_found/total, tempi di valutazione

TECNOLOGIE:
- CrewAI: Framework multi-agent per generazione contenuti
- Azure OpenAI: LLM per valutazione intelligente e estrazione keywords
- MLflow: Tracking esperimenti e monitoraggio performance
"""

import os
import time
import json
from datetime import datetime

import mlflow
from dotenv import load_dotenv
from openai import AzureOpenAI

from report_generator.crews.analysis_crew.analysis_crew import AnalysisCrew

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
            model=os.getenv("MODEL", "o4-mini"),
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
            model=os.getenv("MODEL", "o4-mini"),  # Usa stesso modello di CrewAI
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


def test_analysis_crew_with_mlflow():
    """Execute comprehensive AnalysisCrew testing with MLflow tracking and LLM evaluation.
    
    Performs an isolated test of the AnalysisCrew by simulating input from SanitizeCrew
    and measuring both performance metrics and content quality through LLM-as-a-Judge
    evaluation. All metrics and artifacts are automatically tracked in MLflow and
    saved to timestamped text files for easy review.
    
    The test workflow includes:
    1. Crew execution with simulated input
    2. Performance metrics collection (execution time, success rate)
    3. LLM-based relevance evaluation of generated outline
    4. Keyword coverage analysis
    5. MLflow logging of all metrics and artifacts
    6. Text file output with detailed scores and analysis
    7. Comprehensive error handling and logging
    
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
        - Detailed scores text files (success and error cases)
        - Error logs (if any failures occur)
        - Execution metadata and timestamps
        
    Text File Outputs:
        - analysis_crew_scores_YYYYMMDD_HHMMSS.txt: Detailed evaluation report with:
          * Performance metrics (execution times, success status)
          * Quality metrics (LLM relevance score, keyword coverage)
          * Found/missing keywords breakdown
          * Overall assessment and recommendations
          * Complete MLflow metric values
        - analysis_crew_error_scores_YYYYMMDD_HHMMSS.txt: Error report for failed runs
        
    Returns:
        Any: The raw result object from CrewAI's kickoff() method, containing
             the final output of the AnalysisCrew execution.
             
    Raises:
        Exception: Re-raises any exceptions from crew execution after logging
                  them to MLflow and saving error details to text file.
                  
    Note:
        - Requires MLflow server running on http://127.0.0.1:5000
        - Uses predefined test input simulating inventory management system request
        - Automatically handles markdown wrapper cleanup in JSON outputs
        - All errors are logged to MLflow and saved to text files before re-raising
        - Text files are saved to 'evaluation_output/' directory
        
    Example:
        >>> result = test_analysis_crew_with_mlflow()
        🔍 Start AnalysisCrew...
        🤖 Start valutazione LLM-as-a-Judge...
        📊 Evaluation LLM completed in 2.34s
        🎯 Score relevance: 8.5/10
        ✅ AnalysisCrew completed in 15.67 secondi
        💾 Scores saved to: evaluation_output/analysis_crew_scores_20250908_143022.txt
    """
    
    # Input di test simulato (normalmente arriverebbe da SanitizeCrew)
    test_input = {
        "improved_query": "Crea una docs per un sistema di gestione inventario con API REST, database PostgreSQL e interfaccia web React. Il sistema deve permettere di tracciare prodotti, gestire ordini e generare report automatici."
    }
    
    with mlflow.start_run(run_name="AnalysisCrew_Simple_Test"):
        # ==================== LOGGING SETUP ====================
        mlflow.set_tag("crew_name", "AnalysisCrew")
        mlflow.set_tag("test_type", "simple_test")
        mlflow.set_tag("timestamp", datetime.utcnow().isoformat())
        
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
            mlflow.log_metric("execution_time_seconds", execution_time)
            mlflow.log_metric("execution_success", 1)
            
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
                    mlflow.log_metric("llm_relevance_score", relevance_score)
                    mlflow.log_metric("judge_evaluation_time", judge_time)
                    
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
                    mlflow.log_metric("keyword_coverage_percentage", coverage_result['coverage_percentage'])
                    mlflow.log_metric("keywords_total_count", coverage_result['total_keywords'])
                    mlflow.log_metric("keywords_found_count", coverage_result['found_keywords'])
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
            coverage_result = locals().get('coverage_result', {})
            coverage_percentage = coverage_result.get('coverage_percentage', 0.0)
            judge_time = locals().get('judge_time', 0.0)
            coverage_time = locals().get('coverage_time', 0.0)
            
            print(f"📊 Metriche registrate:")
            print(f"   • execution_success: 1")
            print(f"   • execution_time: {execution_time:.2f}s")
            print(f"   • llm_relevance_score: {relevance_score}/10")
            print(f"   • keyword_coverage: {coverage_percentage:.1f}%")
            
            # ==================== SAVE SCORES TO TEXT FILE ====================
            # Create evaluation_output directory if it doesn't exist
            output_dir = "evaluation_output"
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            scores_file = os.path.join(output_dir, f"analysis_crew_scores_{timestamp}.txt")
            
            try:
                with open(scores_file, 'w', encoding='utf-8') as f:
                    f.write("=" * 80 + "\n")
                    f.write("ANALYSIS CREW EVALUATION SCORES\n")
                    f.write("=" * 80 + "\n")
                    f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                    f.write(f"Test Input Query: {test_input['improved_query']}\n")
                    f.write("=" * 80 + "\n\n")
                    
                    f.write("PERFORMANCE METRICS:\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"Execution Success: {'✅ SUCCESS' if True else '❌ FAILED'}\n")
                    f.write(f"Execution Time: {execution_time:.3f} seconds\n")
                    f.write(f"Judge Evaluation Time: {judge_time:.3f} seconds\n")
                    f.write(f"Coverage Analysis Time: {coverage_time:.3f} seconds\n")
                    f.write(f"Total Evaluation Time: {execution_time + judge_time + coverage_time:.3f} seconds\n\n")
                    
                    f.write("QUALITY METRICS:\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"LLM Relevance Score: {relevance_score:.2f}/10.0\n")
                    f.write(f"Keyword Coverage: {coverage_percentage:.1f}%\n")
                    f.write(f"Keywords Found: {coverage_result.get('found_keywords', 0)}/{coverage_result.get('total_keywords', 0)}\n\n")
                    
                    if coverage_result.get('found_keywords_list'):
                        f.write("KEYWORDS FOUND:\n")
                        f.write("-" * 20 + "\n")
                        for keyword in coverage_result['found_keywords_list']:
                            f.write(f"✅ {keyword}\n")
                        f.write("\n")
                    
                    if coverage_result.get('missing_keywords_list'):
                        f.write("KEYWORDS MISSING:\n")
                        f.write("-" * 20 + "\n")
                        for keyword in coverage_result['missing_keywords_list']:
                            f.write(f"❌ {keyword}\n")
                        f.write("\n")
                    
                    f.write("EVALUATION SUMMARY:\n")
                    f.write("-" * 40 + "\n")
                    
                    # Overall assessment
                    if relevance_score >= 9.0 and coverage_percentage >= 80:
                        overall_assessment = "🌟 EXCELLENT"
                    elif relevance_score >= 7.0 and coverage_percentage >= 60:
                        overall_assessment = "✅ GOOD"
                    elif relevance_score >= 5.0 and coverage_percentage >= 40:
                        overall_assessment = "⚠️ FAIR"
                    else:
                        overall_assessment = "❌ POOR"
                    
                    f.write(f"Overall Assessment: {overall_assessment}\n")
                    f.write(f"Relevance Level: {'High' if relevance_score >= 7 else 'Medium' if relevance_score >= 4 else 'Low'}\n")
                    f.write(f"Coverage Level: {'High' if coverage_percentage >= 70 else 'Medium' if coverage_percentage >= 40 else 'Low'}\n")
                    f.write(f"Performance Level: {'Fast' if execution_time < 30 else 'Medium' if execution_time < 60 else 'Slow'}\n\n")
                    
                    f.write("DETAILED METRICS (for MLflow):\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"execution_success: 1\n")
                    f.write(f"execution_time_seconds: {execution_time:.6f}\n")
                    f.write(f"llm_relevance_score: {relevance_score:.6f}\n")
                    f.write(f"judge_evaluation_time: {judge_time:.6f}\n")
                    f.write(f"keyword_coverage_percentage: {coverage_percentage:.6f}\n")
                    f.write(f"keywords_total_count: {coverage_result.get('total_keywords', 0)}\n")
                    f.write(f"keywords_found_count: {coverage_result.get('found_keywords', 0)}\n")
                    f.write(f"coverage_analysis_time: {coverage_time:.6f}\n")
                    
                    f.write("\n" + "=" * 80 + "\n")
                    f.write("END OF EVALUATION REPORT\n")
                    f.write("=" * 80 + "\n")
                
                print(f"💾 Scores saved to: {scores_file}")
                
                # Log the scores file as MLflow artifact
                mlflow.log_artifact(scores_file)
                
            except Exception as e:
                print(f"⚠️ Error saving scores to text file: {e}")
                mlflow.set_tag("scores_file_error", str(e))
            
            mlflow.set_tag("status", "success")
            return result
            
        except Exception as e:
            execution_time = time.perf_counter() - start_time
            
            # Log errore
            mlflow.log_metric("execution_time_seconds", execution_time)
            mlflow.log_metric("execution_success", 0)
            mlflow.set_tag("status", "failed")
            mlflow.set_tag("error_type", type(e).__name__)
            
            print(f"❌ Errore durante l'esecuzione: {e}")
            print(f"📊 Metriche registrate: execution_success=0, execution_time={execution_time:.2f}s")
            
            # ==================== SAVE ERROR SCORES TO TEXT FILE ====================
            # Create evaluation_output directory if it doesn't exist
            output_dir = "evaluation_output"
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            error_scores_file = os.path.join(output_dir, f"analysis_crew_error_scores_{timestamp}.txt")
            
            try:
                with open(error_scores_file, 'w', encoding='utf-8') as f:
                    f.write("=" * 80 + "\n")
                    f.write("ANALYSIS CREW EVALUATION SCORES - ERROR REPORT\n")
                    f.write("=" * 80 + "\n")
                    f.write(f"Timestamp: {datetime.now().isoformat()}\n")
                    f.write(f"Test Input Query: {test_input['improved_query']}\n")
                    f.write("=" * 80 + "\n\n")
                    
                    f.write("ERROR DETAILS:\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"Error Type: {type(e).__name__}\n")
                    f.write(f"Error Message: {str(e)}\n")
                    f.write(f"Execution Time Before Error: {execution_time:.3f} seconds\n\n")
                    
                    f.write("PERFORMANCE METRICS:\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"Execution Success: ❌ FAILED\n")
                    f.write(f"Execution Time: {execution_time:.3f} seconds\n")
                    f.write(f"Judge Evaluation Time: N/A (error occurred)\n")
                    f.write(f"Coverage Analysis Time: N/A (error occurred)\n\n")
                    
                    f.write("QUALITY METRICS:\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"LLM Relevance Score: 0.0/10.0 (error)\n")
                    f.write(f"Keyword Coverage: 0.0% (error)\n")
                    f.write(f"Keywords Found: 0/0 (error)\n\n")
                    
                    f.write("EVALUATION SUMMARY:\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"Overall Assessment: ❌ FAILED\n")
                    f.write(f"Relevance Level: N/A (error)\n")
                    f.write(f"Coverage Level: N/A (error)\n")
                    f.write(f"Performance Level: Failed after {execution_time:.1f}s\n\n")
                    
                    f.write("DETAILED METRICS (for MLflow):\n")
                    f.write("-" * 40 + "\n")
                    f.write(f"execution_success: 0\n")
                    f.write(f"execution_time_seconds: {execution_time:.6f}\n")
                    f.write(f"llm_relevance_score: 0.000000\n")
                    f.write(f"judge_evaluation_time: 0.000000\n")
                    f.write(f"keyword_coverage_percentage: 0.000000\n")
                    f.write(f"keywords_total_count: 0\n")
                    f.write(f"keywords_found_count: 0\n")
                    f.write(f"coverage_analysis_time: 0.000000\n")
                    
                    f.write("\n" + "=" * 80 + "\n")
                    f.write("END OF ERROR REPORT\n")
                    f.write("=" * 80 + "\n")
                
                print(f"💾 Error scores saved to: {error_scores_file}")
                
                # Log the error scores file as MLflow artifact
                mlflow.log_artifact(error_scores_file)
                
            except Exception as file_error:
                print(f"⚠️ Error saving error scores to text file: {file_error}")
                mlflow.set_tag("error_scores_file_error", str(file_error))
            
            raise


if __name__ == "__main__":
    print("🚀 Test MLflow COMPLETO per AnalysisCrew")
    print("📊 Traccia metriche di performance e qualità")
    print("💾 Salva risultati in MLflow + file di testo")
    print("🔗 Server MLflow: http://127.0.0.1:5000")
    print("-" * 50)
    
    test_analysis_crew_with_mlflow()
    
    print("-" * 50)
    print("✅ Test completato!")
    print("🔍 Controlla MLflow UI per i risultati")
    print("📄 Controlla evaluation_output/ per i file di testo")
