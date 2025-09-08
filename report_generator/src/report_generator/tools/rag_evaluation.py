import rag_qdrant_hybrid as rag
import os
from typing import List

from ragas import evaluate, EvaluationDataset
from ragas.metrics import (
    context_precision,   # "precision@k" sui chunk recuperati
    context_recall,      # copertura dei chunk rilevanti
    faithfulness,        # ancoraggio della risposta al contesto
    answer_relevancy,    # pertinenza della risposta vs domanda
    answer_correctness,  # usa questa solo se hai ground_truth
)

CURRENT_FILE_PATH = os.path.abspath(__file__)
CURRENT_DIRECTORY_PATH = os.path.dirname(CURRENT_FILE_PATH)

def build_ragas_dataset(
    questions: List[str],
    chain,
    client,
    s,
    embeddings,
    llm,
    ground_truth: dict[str, str] | None = None,
):
    """
    Esegue la pipeline RAG per ogni domanda e costruisce il dataset per Ragas.
    Ogni riga contiene: question, contexts, answer, (opzionale) ground_truth.
    """
    dataset = []
    for q in questions:
        # answer = chain.invoke(q)
        contexts = rag.hybrid_search(client, s, q, embeddings)

        # For Ragas: list of individual context strings
        context_texts = rag.extract_context_texts(contexts)

        # For the LLM chain: formatted concatenated string
        ctx = rag.format_docs_for_prompt(contexts)
        chain = rag.build_rag_chain(llm)
        answer = chain.invoke({"question": q, "context": ctx})

        print("ctx: ", ctx)

        row = {
            # chiavi richieste da molte metriche Ragas
            "user_input": q,
            "retrieved_contexts": context_texts,  # List of strings for Ragas
            "response": answer,
        }
        if ground_truth and q in ground_truth:
            row["reference"] = ground_truth[q]

        dataset.append(row)
    return dataset


def main():
    s = rag.SETTINGS
    
    s.collection = "example_docs"
    
    embeddings = rag.get_embeddings(s)
    llm = rag.get_llm(s)  # opzionale

    # 1) Client Qdrant
    client = rag.get_qdrant_client(s)

    # 2) Dati -> chunk
    # docs = simulate_corpus()
    docs_dir = os.path.join(CURRENT_DIRECTORY_PATH, "docs", "docs_example", "_build", "html")
    docs = rag.load_docs_from_directory(docs_dir)  # cartella con PDF e MD
    chunks = rag.split_documents(docs, s, embeddings)

    # 3) Crea (o ricrea) collection
    vector_size = len(embeddings.embed_query("test"))

    rag.recreate_collection_for_rag(client, s, vector_size)

    # 4) Upsert chunks
    rag.upsert_chunks(client, s, chunks, embeddings)
    
    questions = [
        # From index.html
        "What is the Game Builder Crew and what does it demonstrate?",
        "What are the three specialized AI agents in the Game Builder Crew architecture and what are their roles?",
        
        # From installation.html
        "What are the system requirements for installing the Game Builder Crew, including Python version and API access?",
        "What are the two installation methods available for the Game Builder Crew and which one is recommended?",
        
        # From quickstart.html
        "What are the key steps in the 5-minute quick start process for the Game Builder Crew?",
        "What are the three different usage patterns (methods) available for executing the Game Builder Crew?",
        
        # From usage.html
        "What are the core components of the Game Builder Crew system architecture and their purposes?",
        "What are the best practices for writing effective game specifications for the Game Builder Crew?",
        
        # From examples.html
        "What are the three predefined game examples in the Game Builder Crew and what is each one used for?",
        "What are the key features and specifications of the Snake game example (example3_snake)?",
        
        # From api/modules.html
        "What are the main modules in the Game Builder Crew and what are their key components?",
        "What are the most common classes and functions in the Game Builder Crew API reference?",
        
        # From api/crew.html
        "What is the GameBuilderCrew class and what are its main methods for agent and task management?",
        "How can you customize the GameBuilderCrew class with custom configurations and advanced usage patterns?",
        
        # From api/main.html
        "What are the two key functions provided by the main module and what are their purposes?",
        "What environment variables does the main module respect for configuration and how are they used?"
    ]
    
    chain = rag.build_rag_chain(llm)
    
    ground_truth = {
        questions[0]: "The Game Builder Crew is an innovative AI-powered system that leverages multiple specialized agents to collaboratively create Python games. It demonstrates the use of the CrewAI framework to automate the creation of Python games using AI agents, orchestrating autonomous AI agents to work together in a structured, sequential process that mirrors professional software development practices.",
        
        questions[1]: "The three specialized AI agents are: 1) Senior Engineer Agent - Creates the initial game code based on specifications, 2) QA Engineer Agent - Reviews code for errors, bugs, and improvements, and 3) Chief QA Engineer Agent - Performs final quality assurance and completeness validation. They work in sequence to create, review, and finalize game code.",
        
        questions[2]: "System requirements include: Python 3.8 or higher with pip package manager, Operating Systems (Windows 10/11, macOS 10.14+, or Linux Ubuntu 18.04+), OpenAI API key for GPT-4o access, optional Serper API key for web search capabilities, and memory requirements of minimum 4GB RAM (8GB+ recommended).",
        
        questions[3]: "The two installation methods are: 1) Using Poetry (Recommended) - which handles dependency management and virtual environments automatically, and 2) Using pip and venv - a traditional approach using pip and virtual environments. Poetry is recommended because it provides better dependency management and virtual environment handling.",
        
        questions[4]: "The key steps in the 5-minute quick start are: 1) Navigate to project directory (cd game-builder-crew), 2) Run your first game creation (poetry run game_builder_crew), 3) View the output which will show agent execution logs and complete Python game code, and 4) Save and run the game by copying the generated code to a file and executing it with python.",
        
        questions[5]: "The three usage patterns are: 1) Method 1: Command Line (Simplest) - running with default Snake game example using 'poetry run game_builder_crew', 2) Method 2: Python Script (Customizable) - writing custom Python scripts to define game requirements and generate games, and 3) Method 3: Using Predefined Examples - loading and using pre-built game examples from the gamedesign.yaml file.",
        
        questions[6]: "The core components include: Agents (Senior Engineer Agent for creating initial game code, QA Engineer Agent for reviews and fixes, Chief QA Engineer Agent for final quality assurance), Configuration Files (agents.yaml for agent personalities and capabilities, tasks.yaml for task definitions and requirements, gamedesign.yaml for pre-built game examples), and Input/Output (Input: detailed game specifications, Output: complete executable Python game code).",
        
        questions[7]: "Best practices for writing effective game specifications include: 1) Be specific and detailed about core mechanics, win/lose conditions, and technical requirements, 2) Include technical constraints like graphics library preferences, performance targets, and platform compatibility, 3) Specify user interface elements including control schemes, menu systems, and information display, 4) Define clear win/lose conditions, 5) Include performance targets and optimization requirements, and 6) Structure requirements with clear sections for game type, mechanics, technical requirements, and special features.",
        
        questions[8]: "The three predefined game examples are: 1) Snake Game (example3_snake) - Used by default in production runs, features classic Snake game with comprehensive mechanics, 2) Pac-Man Detailed (example1_pacman) - Used for training the crew, features full Pac-Man game mechanics with four distinct ghost AI personalities, and 3) Pac-Man Simple (example2_pacman) - Used for quick prototyping, features simplified Pac-Man with basic movement and random ghost behavior.",
        
        questions[9]: "The Snake game example (example3_snake) features: grid-based movement system, arrow key controls (Up, Down, Left, Right), food consumption with snake growth, collision detection for walls and self-collision, score tracking, game over conditions, rectangular grid (2D matrix/array), discrete movement (one cell per frame), continuous directional movement, growth mechanism (one segment per food), random food spawning, and scoring system with 10 points per food item consumed.",
        
        questions[10]: "The main modules are: Core Modules - crew.py (main orchestration with GameBuilderCrew class, agents, tasks), main.py (entry points with run() and train() functions), __init__.py (package setup with exports and version info). Configuration Files - agents.yaml (agent definitions with roles, goals, backstories), tasks.yaml (task specifications with descriptions, expected outputs), gamedesign.yaml (game examples with pre-built game specifications).",
        
        questions[11]: "The most common classes and functions include: GameBuilderCrew class (main orchestrator for the game building process with crew() method that returns configured crew ready for execution), run() function (executes game building process with default Snake game example), and train() function (trains the crew using iterative learning with parameters for n_iterations and filename).",
        
        questions[12]: "The GameBuilderCrew class is the main orchestrator class for the game building process. Its main methods include: Agent Methods (for creating and managing the three specialized agents), Task Methods (for defining and managing the sequential tasks), Crew Assembly (for combining agents and tasks into a working crew), and Configuration Attributes (agents_config pointing to 'config/agents.yaml' and tasks_config pointing to 'config/tasks.yaml').",
        
        questions[13]: "You can customize the GameBuilderCrew class by: creating custom configuration files and extending the class to use them, adding custom agents with the @agent decorator and specific configurations, implementing performance monitoring with timing and metrics collection, adding error handling with logging and graceful failure management, and modifying agent behavior by editing configuration files to change roles, goals, and backstories.",
        
        questions[14]: "The two key functions are: 1) run() - provides production execution with predefined examples, specifically executing the game building process with the default Snake game example (example3_snake), and 2) train() - provides training and model improvement functionality, allowing iterative learning with configurable parameters for number of iterations and output filename, using the complex Pac-Man example (example1_pacman) for training.",
        
        questions[15]: "The main module respects these environment variables: OpenAI Configuration (OPENAI_API_KEY for your API key, OPENAI_MODEL for the model like gpt-4o), Logging (LOG_LEVEL for logging level like INFO, CREW_VERBOSE for detailed logging as true/false), and Training Parameters (DEFAULT_ITERATIONS for number of training iterations like 10, MODEL_OUTPUT_DIR for model output directory like ./models/)."
    }
    
    # 6) Costruisci dataset per Ragas (stessi top-k del tuo retriever)
    dataset = build_ragas_dataset(
        questions=questions,
        chain=chain,
        client=client,
        s=s,
        embeddings=embeddings,
        llm=llm,
        ground_truth=ground_truth,  # rimuovi se non vuoi correctness
    )

    evaluation_dataset = EvaluationDataset.from_list(dataset)

    # 7) Scegli le metriche
    metrics = [context_precision, context_recall, faithfulness, answer_relevancy]
    # Aggiungi correctness solo se tutte le righe hanno ground_truth
    if all("ground_truth" in row for row in dataset):
        metrics.append(answer_correctness)

    # 8) Esegui la valutazione con il TUO LLM e le TUE embeddings
    ragas_result = evaluate(
        dataset=evaluation_dataset,
        metrics=metrics,
        llm=llm,                 # passa l'istanza LangChain del tuo LLM (LM Studio)
        embeddings=rag.get_embeddings(s),  # o riusa 'embeddings' creato sopra
    )

    df = ragas_result.to_pandas()
    cols = ["user_input", "response", "context_precision", "context_recall", "faithfulness", "answer_relevancy"]
    print("\n=== DETTAGLIO PER ESEMPIO ===")
    print(df[cols].round(4).to_string(index=False))

    # (facoltativo) salva per revisione umana
    df.to_csv("ragas_results.csv", index=False)
    print("Salvato: ragas_results.csv")
    
if __name__ == "__main__":
    main()