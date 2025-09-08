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
    """
    Inizializza client Azure OpenAI usando le stesse credenziali di CrewAI.
    Riusa la configurazione esistente dal file .env
    """
    return AzureOpenAI(
        api_key=os.getenv("AZURE_API_KEY"),
        api_version=os.getenv("AZURE_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_API_BASE"),
        azure_deployment=os.getenv("MODEL")
    )


def _evaluate_outline_relevance(original_query: str, outline_content: str) -> float:
    """
    Usa LLM-as-a-Judge per valutare la rilevanza della scaletta rispetto alla richiesta originale.
    
    Args:
        original_query: La richiesta originale dell'utente
        outline_content: Il contenuto della scaletta generata (JSON come string)
    
    Returns:
        float: Punteggio da 1.0 a 10.0 che indica la rilevanza
    """
    try:
        # Inizializza client Azure OpenAI
        client = _get_azure_openai_client()
        
        # Costruisce il prompt per la valutazione
        evaluation_prompt = f"""
COMPITO: Valuta la rilevanza di questa scaletta rispetto alla richiesta originale.

RICHIESTA ORIGINALE:
"{original_query}"

SCALETTA GENERATA:
{outline_content}

CRITERI DI VALUTAZIONE:
1. Coerenza tematica: La scaletta tratta effettivamente l'argomento richiesto?
2. Completezza tecnica: Include le tecnologie e componenti menzionati nella richiesta?
3. Struttura logica: Le sezioni e sottosezioni hanno un flusso logico?
4. Pertinenza dei contenuti: Ogni sezione è utile per l'obiettivo della richiesta?

SCALA DI VALUTAZIONE:
- 1-3: Completamente fuori tema o irrilevante
- 4-6: Parzialmente rilevante, mancano elementi importanti
- 7-8: Buona rilevanza, cubre la maggior parte degli aspetti
- 9-10: Perfettamente inerente e completa

RISPOSTA: Fornisci SOLO un numero da 1 a 10 (es: 8)
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
    """
    Test semplificato della AnalysisCrew con tracking MLflow basilare.
    
    Traccia solo:
    - execution_success: se funziona (1) o no (0)
    - execution_time_seconds: quanto tempo ci mette
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
