"""
MLflow Testing Module for AnalysisCrew Evaluation

This module provides comprehensive testing and evaluation capabilities for CrewAI's AnalysisCrew
using MLflow tracking. It implements both basic performance metrics and advanced LLM-as-a-Judge
evaluation to assess the quality and relevance of generated content outlines.

The module integrates with Azure OpenAI services and provides automated tracking of:
- Execution performance metrics
- Content quality evaluation via LLM-based judging
- Error handling and logging
- MLflow experiment tracking and artifact management

Example:
    Run the evaluation test:
        $ python test_analysis_crew_mlflow.py
        
    Monitor results in MLflow UI:
        http://127.0.0.1:5000
"""

import os
import time
import json
from datetime import datetime

import mlflow
from dotenv import load_dotenv
from openai import AzureOpenAI

from src.report_generator.crews.analysis_crew.analysis_crew import AnalysisCrew

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


def test_analysis_crew_with_mlflow():
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
    
    Tracked Metrics:
        execution_success (int): Binary success indicator (1=success, 0=failure)
        execution_time_seconds (float): Total crew execution duration
        llm_relevance_score (float): LLM-judged relevance score (1-10)
        judge_evaluation_time (float): Duration of LLM evaluation process
        
    MLflow Artifacts:
        - Generated outline JSON files
        - Error logs (if any failures occur)
        - Execution metadata and timestamps
        
    Returns:
        Any: The raw result object from CrewAI's kickoff() method, containing
             the final output of the AnalysisCrew execution.
             
    Raises:
        Exception: Re-raises any exceptions from crew execution after logging
                  them to MLflow with appropriate error metrics and tags.
                  
    Note:
        - Requires MLflow server running on http://127.0.0.1:5000
        - Uses predefined test input simulating inventory management system request
        - Automatically handles markdown wrapper cleanup in JSON outputs
        - All errors are logged to MLflow before re-raising
        
    Example:
        >>> result = test_analysis_crew_with_mlflow()
        🔍 Start AnalysisCrew...
        🤖 Start valutazione LLM-as-a-Judge...
        📊 Evaluation LLM completed in 2.34s
        🎯 Score relevance: 8.5/10
        ✅ AnalysisCrew completed in 15.67 secondi
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
                    
                    # Registra le metriche
                    mlflow.log_metric("llm_relevance_score", relevance_score)
                    mlflow.log_metric("judge_evaluation_time", judge_time)
                    
                    print(f"📊 Valutazione LLM completata in {judge_time:.2f}s")
                    print(f"🎯 Punteggio rilevanza: {relevance_score}/10")
                    
                except Exception as e:
                    print(f"❌ Errore durante valutazione: {e}")
                    mlflow.log_metric("llm_relevance_score", 0.0)
                    mlflow.set_tag("judge_error", str(e))
            else:
                print(f"❌ File scaletta non trovato: {outline_path}")
                mlflow.log_metric("llm_relevance_score", 0.0)
                mlflow.set_tag("judge_error", "outline_file_missing")
            
            print(f"✅ AnalysisCrew completata in {execution_time:.2f} secondi")
            print(f"📊 Metriche registrate: execution_success=1, execution_time={execution_time:.2f}s, llm_relevance_score={relevance_score if 'relevance_score' in locals() else 0.0}")
            
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
            raise


if __name__ == "__main__":
    print("🚀 Test MLflow SEMPLIFICATO per AnalysisCrew")
    # print("Traccia solo: execution_success + execution_time_seconds")
    # print("Server MLflow: http://127.0.0.1:5000")
    print("-" * 50)
    
    test_analysis_crew_with_mlflow()
    
    print("-" * 50)
    print("✅ Test completato! Controlla MLflow UI per i risultati.")
