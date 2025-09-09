"""
RAG pipeline with Qdrant and AzureOpenAI embeddings
"""
 
from __future__ import annotations
import os
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Dict, Any, Iterable, Tuple
 
from dotenv import load_dotenv
from langchain.schema import Document
from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker

from langchain_community.document_loaders import PyPDFLoader, PDFMinerLoader, UnstructuredMarkdownLoader, UnstructuredHTMLLoader
 
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.chat_models import init_chat_model
 
from openai import embeddings
from qdrant_client.models import ScalarType
from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    HnswConfigDiff,
    OptimizersConfigDiff,
    ScalarQuantization,
    ScalarQuantizationConfig,
    PayloadSchemaType,
    FieldCondition,
    MatchValue,
    MatchText,
    Filter,
    SearchParams,
    PointStruct,
)

from qdrant_client import QdrantClient, models
from qdrant_client.http.models import Distance, SparseVectorParams, VectorParams

CURRENT_FILE_PATH = os.path.abspath(__file__)
CURRENT_DIRECTORY_PATH = os.path.dirname(CURRENT_FILE_PATH)
 
# Load env vars
load_dotenv()
 
@dataclass
class Settings:
    """Configuration settings for RAG pipeline.
    
    This class contains all the configuration parameters needed for the RAG
    (Retrieval-Augmented Generation) pipeline, including Qdrant settings,
    embedding parameters, search configurations, and LLM settings.
    
    Attributes:
        qdrant_url (str): URL of the Qdrant vector database server.
            Defaults to "http://localhost:6333".
        collection (str): Name of the Qdrant collection to use for storing vectors.
            Defaults to "final_project_docs".
        emb_model_name (str): Name of the Azure OpenAI embedding model.
            Defaults to "text-embedding-ada-002".
        api_version (str): Environment variable name for Azure API version.
            Defaults to "AZURE_API_VERSION".
        chunk_size (int): Size of text chunks in characters for document splitting.
            Defaults to 700. Range: [100, 2000].
        chunk_overlap (int): Overlap between consecutive chunks in characters.
            Defaults to 200. Range: [0, chunk_size//2].
        top_n_semantic (int): Number of candidates for semantic search.
            Defaults to 30. Range: [1, 1000].
        top_n_text (int): Number of candidates for text search.
            Defaults to 100. Range: [1, 1000].
        final_k (int): Final number of results to return.
            Defaults to 5. Range: [1, min(top_n_semantic, top_n_text)].
        alpha (float): Weight for semantic search in hybrid fusion.
            Defaults to 0.75. Range: [0.0, 1.0].
        text_boost (float): Boost factor for text search matches.
            Defaults to 0.20. Range: [0.0, 1.0].
        use_mmr (bool): Whether to use Maximum Marginal Relevance diversification.
            Defaults to True.
        mmr_lambda (float): Balance parameter for MMR (relevance vs diversity).
            Defaults to 0.6. Range: [0.0, 1.0].
        lm_base_env (str): Environment variable name for LLM base URL.
            Defaults to "AZURE_API_BASE".
        lm_key_env (str): Environment variable name for LLM API key.
            Defaults to "AZURE_API_KEY".
        lm_model_env (str): Environment variable name for LLM model name.
            Defaults to "MODEL".
        use_cache (bool): Whether to enable embedding caching.
            Defaults to True.
        cache_file (str): Path to the embedding cache file.
            Defaults to "embedding_cache.pkl".
            
    Example:
        >>> settings = Settings()
        >>> settings.final_k = 10
        >>> settings.alpha = 0.8
        >>> print(settings.qdrant_url)
        http://localhost:6333
    """
    qdrant_url: str = "http://localhost:6333"  # Qdrant URL
    collection: str = "final_project_docs"             # Collection name
    emb_model_name: str = "text-embedding-ada-002"  # Embedding model
    api_version: str = "AZURE_API_VERSION"
    chunk_size: int = 700                      # Chunk size
    chunk_overlap: int = 200                   # Overlap size
    top_n_semantic: int = 30                   # Candidates for semantic search
    top_n_text: int = 100                      # Candidates for text search
    final_k: int = 5                           # Final results count
    alpha: float = 0.75                        # Semantic weight
    text_boost: float = 0.20                   # Text boost
    use_mmr: bool = True                       # Use MMR diversification
    mmr_lambda: float = 0.6                    # MMR balance
    lm_base_env: str = "AZURE_API_BASE"       # LLM base URL env
    lm_key_env: str = "AZURE_API_KEY"         # LLM API key env
    lm_model_env: str = "MODEL"       # LLM model env
    use_cache: bool = True                     # Enable embedding cache
    cache_file: str = "embedding_cache.pkl"   # Cache file path
 
SETTINGS = Settings()
 
# ========== Embeddings & LLM ==========

def retry_with_backoff(func, max_retries=3, base_delay=1.0):
    """Retry function with exponential backoff for rate limiting.
    
    Executes a function with exponential backoff when rate limits are encountered.
    Specifically handles HTTP 429 errors and rate limit exceptions by waiting
    progressively longer between retries.
    
    Args:
        func (callable): Function to execute with retry logic.
        max_retries (int, optional): Maximum number of retry attempts.
            Defaults to 3. Range: [1, 10].
        base_delay (float, optional): Base delay in seconds for exponential backoff.
            Defaults to 1.0. Range: [0.1, 60.0].
    
    Returns:
        Any: Result of the function call if successful.
        None: If all retries are exhausted for rate limit errors.
    
    Raises:
        Exception: Re-raises the original exception if it's not a rate limit error,
            or if max_retries is reached for rate limit errors.
    
    Example:
        >>> def api_call():
        ...     return "success"
        >>> result = retry_with_backoff(api_call, max_retries=3, base_delay=1.0)
        >>> print(result)
        success
    """
    for attempt in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "429" in str(e) or "rate limit" in str(e).lower():
                if attempt == max_retries - 1:
                    raise e
                delay = base_delay * (2 ** attempt)
                print(f"Rate limit hit, waiting {delay} seconds before retry {attempt + 1}/{max_retries}")
                time.sleep(delay)
            else:
                raise e
    return None

def get_embeddings(settings: Settings) -> AzureOpenAIEmbeddings:
    """Return Azure OpenAI embeddings instance.
    
    Creates and returns an AzureOpenAIEmbeddings object configured with the
    embedding model specified in the settings.
    
    Args:
        settings (Settings): Configuration object containing embedding model name.
    
    Returns:
        AzureOpenAIEmbeddings: Configured Azure OpenAI embeddings instance.
    
    Example:
        >>> settings = Settings()
        >>> embeddings = get_embeddings(settings)
        >>> isinstance(embeddings, AzureOpenAIEmbeddings)
        True
    """
    return AzureOpenAIEmbeddings(model=settings.emb_model_name)
 
def get_llm(settings: Settings):
    """Initialize LLM if configured.
    
    Attempts to initialize an Azure OpenAI language model using environment
    variables specified in the settings. Performs a test invocation to verify
    the configuration is working.
    
    Args:
        settings (Settings): Configuration object containing LLM environment
            variable names for base URL, API key, model name, and API version.
    
    Returns:
        Any: Initialized LLM instance if configuration is successful.
        None: If configuration is incomplete or initialization fails.
    
    Example:
        >>> settings = Settings()
        >>> llm = get_llm(settings)  # Returns None if env vars not set
        >>> print(llm is None)
        True
    """
    try:
        base = os.getenv(settings.lm_base_env)
        key = os.getenv(settings.lm_key_env)
        model_name = os.getenv(settings.lm_model_env)
        api_version = os.getenv(settings.api_version)
        if not (base and key and model_name):
            print("LLM not configured")
            return None
        llm = init_chat_model(model_name, model_provider="azure_openai", api_version=api_version, api_key=key, azure_endpoint=base)
        test_response = llm.invoke("test")
        if test_response:
            print("LLM configured")
            return llm
        print("LLM test failed")
        return None
    except Exception as e:
        print(f"LLM error: {e}")
        return None
 
# ========== Data prep ==========
 
def simulate_corpus() -> List[Document]:
    """Return a small fake corpus for testing.
    
    Creates a small collection of predefined Document objects with sample
    content about LangChain, FAISS, embeddings, RAG pipelines, and MMR.
    Useful for testing and development purposes.
    
    Returns:
        List[Document]: List of 5 Document objects with sample content and metadata.
    
    Example:
        >>> docs = simulate_corpus()
        >>> len(docs)
        5
        >>> docs[0].page_content
        'LangChain is a framework for building LLM apps.'
        >>> docs[0].metadata['id']
        'doc1'
    """
    docs = [
        Document(
            page_content="LangChain is a framework for building LLM apps.",
            metadata={"id": "doc1", "source": "intro-langchain.md", "title": "Intro LangChain", "lang": "en"}
        ),
        Document(
            page_content="FAISS is a library for similarity search of dense vectors.",
            metadata={"id": "doc2", "source": "faiss-overview.md", "title": "FAISS Overview", "lang": "en"}
        ),
        Document(
            page_content="Sentence-transformers like MiniLM produce embeddings.",
            metadata={"id": "doc3", "source": "embeddings-minilm.md", "title": "MiniLM Embeddings", "lang": "en"}
        ),
        Document(
            page_content="A RAG pipeline includes indexing, retrieval and generation.",
            metadata={"id": "doc4", "source": "rag-pipeline.md", "title": "RAG Pipeline", "lang": "en"}
        ),
        Document(
            page_content="MMR balances relevance and diversity in retrieval.",
            metadata={"id": "doc5", "source": "retrieval-mmr.md", "title": "MMR Retrieval", "lang": "en"}
        ),
    ]
    return docs
    
def load_docs_from_directory(directory_path: str) -> List[Document]:
    """Load all PDF, Markdown, and HTML files from a directory.
    
    Recursively loads and processes all supported document types (PDF, Markdown,
    HTML) from the specified directory. Each document's metadata is updated
    with the source filename.
    
    Args:
        directory_path (str): Absolute or relative path to the directory
            containing documents to load.
    
    Returns:
        List[Document]: List of loaded Document objects with content and metadata.
            Returns empty list if directory doesn't exist or no supported files found.
    
    Example:
        >>> docs = load_docs_from_directory("/path/to/docs")
        Loading documents from /path/to/docs...
        Loaded PDF: document.pdf
        Loaded Markdown: readme.md
        Total documents loaded: 2
        >>> len(docs) >= 0
        True
    """
    
    print(f"Loading documents from {directory_path}...")
    documents: List[Document] = []
    directory = Path(directory_path)
    
    if not directory.exists():
        print(f"Directory {directory_path} does not exist")
        return documents
    
    # Get all files recursively in directory and subdirectories
    for file_path in directory.rglob('*'):
        if file_path.is_file():
            extension = file_path.suffix.lower()
            
            if extension == '.pdf':
                try:
                    pdf_docs = load_pdf(str(file_path))
                    documents.extend(pdf_docs)
                    print(f"Loaded PDF: {file_path.relative_to(directory)}")
                except Exception as e:
                    print(f"Error loading PDF {file_path.relative_to(directory)}: {e}")
                    
            elif extension in ['.md', '.markdown', '.mdx']:
                try:
                    md_docs = load_md(str(file_path))
                    documents.extend(md_docs)
                    print(f"Loaded Markdown: {file_path.relative_to(directory)}")
                except Exception as e:
                    print(f"Error loading Markdown {file_path.relative_to(directory)}: {e}")
                    
            elif extension in ['.html', '.htm']:
                try:
                    html_docs = load_html(str(file_path))
                    documents.extend(html_docs)
                    print(f"Loaded HTML: {file_path.relative_to(directory)}")
                except Exception as e:
                    print(f"Error loading HTML {file_path.relative_to(directory)}: {e}")
    
    print(f"Total documents loaded: {len(documents)}")
    return documents

def load_pdf(file_path : str) -> List[Document]:
    """Load a PDF file using PDFMinerLoader.
    
    Loads and extracts text content from a PDF file, setting the source
    metadata to the filename.
    
    Args:
        file_path (str): Path to the PDF file to load.
    
    Returns:
        List[Document]: List of Document objects extracted from the PDF.
            Each document contains the page content and metadata with source filename.
    
    Raises:
        Exception: If the PDF file cannot be loaded or processed.
    
    Example:
        >>> docs = load_pdf("/path/to/document.pdf")
        >>> len(docs) >= 1
        True
        >>> docs[0].metadata['source']
        'document.pdf'
    """

    documents: List[Document] = []
    
    loader = PDFMinerLoader(file_path)
    docs = loader.load()
    
    for doc in docs:
            doc.metadata["source"] = os.path.basename(file_path)
            documents.append(doc)

    return documents

def load_md(file_path: str) -> List[Document]:
    """Load a Markdown file using UnstructuredMarkdownLoader.
    
    Loads and extracts text content from a Markdown file, setting the source
    metadata to the filename.
    
    Args:
        file_path (str): Path to the Markdown file to load.
    
    Returns:
        List[Document]: List of Document objects extracted from the Markdown file.
            Each document contains the content and metadata with source filename.
    
    Raises:
        Exception: If the Markdown file cannot be loaded or processed.
    
    Example:
        >>> docs = load_md("/path/to/readme.md")
        >>> len(docs) >= 1
        True
        >>> docs[0].metadata['source']
        'readme.md'
    """

    documents: List[Document] = []

    loader = UnstructuredMarkdownLoader(file_path)
    docs = loader.load()

    for doc in docs:
        doc.metadata["source"] = os.path.basename(file_path)
        documents.append(doc)

    return documents

def load_html(file_path: str) -> List[Document]:
    """Load an HTML file using UnstructuredHTMLLoader.
    
    Loads and extracts text content from an HTML file, setting the source
    metadata to the filename.
    
    Args:
        file_path (str): Path to the HTML file to load.
    
    Returns:
        List[Document]: List of Document objects extracted from the HTML file.
            Each document contains the content and metadata with source filename.
    
    Raises:
        Exception: If the HTML file cannot be loaded or processed.
    
    Example:
        >>> docs = load_html("/path/to/page.html")
        >>> len(docs) >= 1
        True
        >>> docs[0].metadata['source']
        'page.html'
    """
    
    documents: List[Document] = []
    
    loader = UnstructuredHTMLLoader(file_path)
    docs = loader.load()

    for doc in docs:
        doc.metadata["source"] = os.path.basename(file_path)
        documents.append(doc)

    return documents

def split_documents(docs: List[Document], settings: Settings, embeddings: AzureOpenAIEmbeddings) -> List[Document]:
    """Split documents into chunks using semantic chunking.
    
    Uses SemanticChunker to split documents into semantically coherent chunks
    based on embedding similarity. The chunker uses percentile-based breakpoint
    detection at the 95th percentile.
    
    Args:
        docs (List[Document]): List of documents to split into chunks.
        settings (Settings): Configuration settings (not currently used in implementation).
        embeddings (AzureOpenAIEmbeddings): Embeddings model for semantic chunking.
    
    Returns:
        List[Document]: List of document chunks with preserved metadata.
    
    Example:
        >>> docs = [Document(page_content="Long text..." * 100, metadata={"source": "test.txt"})]
        >>> settings = Settings()
        >>> embeddings = get_embeddings(settings)
        >>> chunks = split_documents(docs, settings, embeddings)
        >>> len(chunks) >= len(docs)
        True
    """
    splitter = SemanticChunker(
        embeddings=embeddings,
        breakpoint_threshold_type="percentile",  # o "standard_deviation"
        breakpoint_threshold_amount=95
    )
    return splitter.split_documents(docs)
 
# ========== Qdrant ==========
 
def get_qdrant_client(settings: Settings) -> QdrantClient:
    """Return Qdrant client instance.
    
    Creates and returns a QdrantClient configured with the URL from settings
    and a 30-second timeout.
    
    Args:
        settings (Settings): Configuration object containing Qdrant URL.
    
    Returns:
        QdrantClient: Configured Qdrant client instance with 30-second timeout.
    
    Example:
        >>> settings = Settings()
        >>> client = get_qdrant_client(settings)
        >>> isinstance(client, QdrantClient)
        True
    """
    return QdrantClient(url=settings.qdrant_url, timeout=30)




def recreate_collection_for_rag(client: QdrantClient, settings: Settings, vector_size: int):
    """Create Qdrant collection and indexes only if they don't exist.
    
    Creates a new Qdrant collection with optimized configuration for RAG workloads
    if it doesn't already exist. Includes HNSW indexing, scalar quantization,
    and payload indexes for efficient search.
    
    Args:
        client (QdrantClient): Qdrant client instance.
        settings (Settings): Configuration object containing collection name.
        vector_size (int): Dimension of the embedding vectors.
            Typically 1536 for text-embedding-ada-002. Range: [1, 10000].
    
    Returns:
        None
    
    Example:
        >>> client = get_qdrant_client(Settings())
        >>> settings = Settings()
        >>> recreate_collection_for_rag(client, settings, 1536)
        # Collection created with indexes if it didn't exist
    """
    if not client.collection_exists(settings.collection):
        client.create_collection(
            collection_name=settings.collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
            hnsw_config=HnswConfigDiff(m=32, ef_construct=256),
            optimizers_config=OptimizersConfigDiff(default_segment_number=2),
            quantization_config=ScalarQuantization(
                scalar=ScalarQuantizationConfig(type=ScalarType.INT8, always_ram=False)
            ),
        )
        client.create_payload_index(settings.collection, "text", PayloadSchemaType.TEXT)
        for key in ["doc_id", "source", "title", "lang"]:
            client.create_payload_index(settings.collection, key, PayloadSchemaType.KEYWORD)
    # If collection exists, do nothing (reuse existing collection and indexes)

# ========== Ingest ==========
 
def build_points(chunks: List[Document], embeds: List[List[float]]) -> List[PointStruct]:
    """Build Qdrant points from document chunks and their embeddings.
    
    Creates PointStruct objects suitable for inserting into Qdrant by combining
    document chunks with their corresponding embeddings and metadata.
    
    Args:
        chunks (List[Document]): List of document chunks with content and metadata.
        embeds (List[List[float]]): List of embedding vectors corresponding to chunks.
            Must have the same length as chunks.
    
    Returns:
        List[PointStruct]: List of Qdrant points with sequential IDs starting from 1,
            embedding vectors, and payload containing metadata and text content.
    
    Example:
        >>> chunks = [Document(page_content="test", metadata={"source": "test.txt"})]
        >>> embeds = [[0.1, 0.2, 0.3]]
        >>> points = build_points(chunks, embeds)
        >>> len(points)
        1
        >>> points[0].id
        1
        >>> points[0].payload['text']
        'test'
    """
    pts: List[PointStruct] = []
    for i, (doc, vec) in enumerate(zip(chunks, embeds), start=1):
        payload = {
            "doc_id": doc.metadata.get("id"),
            "source": doc.metadata.get("source"),
            "title": doc.metadata.get("title"),
            "lang": doc.metadata.get("lang", "en"),
            "text": doc.page_content,
            "chunk_id": i - 1
        }
        pts.append(PointStruct(id=i, vector=vec, payload=payload))
    return pts
 
def upsert_chunks(client: QdrantClient, settings: Settings, chunks: List[Document], embeddings: AzureOpenAIEmbeddings):
    """Embed and upsert chunks with rate limiting.
    
    Processes document chunks in batches, generates embeddings for each batch
    with rate limiting and retry logic, then upserts the resulting points
    to Qdrant.
    
    Args:
        client (QdrantClient): Qdrant client for database operations.
        settings (Settings): Configuration object containing collection name.
        chunks (List[Document]): List of document chunks to embed and store.
        embeddings (AzureOpenAIEmbeddings): Embeddings model for generating vectors.
    
    Returns:
        None
    
    Raises:
        Exception: If embedding generation fails after all retries or if
            Qdrant upsert operation fails.
    
    Example:
        >>> client = get_qdrant_client(Settings())
        >>> settings = Settings()
        >>> chunks = [Document(page_content="test", metadata={})]
        >>> embeddings = get_embeddings(settings)
        >>> upsert_chunks(client, settings, chunks, embeddings)
        Embedding 1 chunks...
        Processing batch 1/1
    """
    print(f"Embedding {len(chunks)} chunks...")
    
    # Process chunks in smaller batches to avoid rate limits
    batch_size = 10  # Reduce batch size for rate limiting
    all_vecs = []
    
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        print(f"Processing batch {i//batch_size + 1}/{(len(chunks)-1)//batch_size + 1}")
        
        # Use retry logic for embedding
        def embed_batch():
            return embeddings.embed_documents([c.page_content for c in batch])
        
        batch_vecs = retry_with_backoff(embed_batch, max_retries=5, base_delay=2.0)
        all_vecs.extend(batch_vecs)
        
        # Add small delay between batches
        if i + batch_size < len(chunks):
            time.sleep(1.0)
    
    points = build_points(chunks, all_vecs)
    client.upsert(collection_name=settings.collection, points=points, wait=True)
 
# ========== Search ==========
 
def qdrant_semantic_search(client: QdrantClient, settings: Settings, query: str, embeddings: AzureOpenAIEmbeddings, limit: int, with_vectors: bool = False):
    """Semantic search in Qdrant with retry logic.
    
    Performs semantic similarity search by embedding the query and searching
    for the most similar vectors in the Qdrant collection using cosine similarity.
    
    Args:
        client (QdrantClient): Qdrant client for database operations.
        settings (Settings): Configuration object containing collection name.
        query (str): Text query to search for.
        embeddings (AzureOpenAIEmbeddings): Embeddings model for query encoding.
        limit (int): Maximum number of results to return. Range: [1, 1000].
        with_vectors (bool, optional): Whether to include vectors in results.
            Defaults to False.
    
    Returns:
        List: List of Qdrant points matching the query, sorted by similarity score.
    
    Raises:
        Exception: If query embedding fails after all retries or if
            Qdrant search operation fails.
    
    Example:
        >>> settings = Settings()
        >>> client = get_qdrant_client(settings)
        >>> embeddings = get_embeddings(settings)
        >>> results = qdrant_semantic_search(client, settings, "test query", embeddings, 5)
        >>> len(results) <= 5
        True
    """
    def embed_query():
        return embeddings.embed_query(query)
    
    qv = retry_with_backoff(embed_query, max_retries=5, base_delay=2.0)
    res = client.query_points(
        collection_name=settings.collection,
        query=qv,
        limit=limit,
        with_payload=True,
        with_vectors=with_vectors,
        search_params=SearchParams(hnsw_ef=256, exact=False),
    )
    return res.points
 
def qdrant_text_prefilter_ids(client: QdrantClient, settings: Settings, query: str, max_hits: int) -> List[int]:
    """Return IDs matching text filter using Qdrant's text search.
    
    Performs text-based search in Qdrant using the "text" field payload index
    to find documents containing the query terms. Uses pagination to handle
    large result sets.
    
    Args:
        client (QdrantClient): Qdrant client for database operations.
        settings (Settings): Configuration object containing collection name.
        query (str): Text query to search for in document text.
        max_hits (int): Maximum number of matching IDs to return.
            Range: [1, 10000].
    
    Returns:
        List[int]: List of point IDs that match the text query.
            Length is at most max_hits.
    
    Example:
        >>> settings = Settings()
        >>> client = get_qdrant_client(Settings())
        >>> ids = qdrant_text_prefilter_ids(client, settings, "python", 100)
        >>> len(ids) <= 100
        True
        >>> all(isinstance(id, int) for id in ids)
        True
    """
    matched_ids: List[int] = []
    next_page = None
    while True:
        points, next_page = client.scroll(
            collection_name=settings.collection,
            scroll_filter=Filter(must=[FieldCondition(key="text", match=MatchText(text=query))]),
            limit=min(256, max_hits - len(matched_ids)),
            offset=next_page,
            with_payload=False,
            with_vectors=False,
        )
        matched_ids.extend([p.id for p in points])
        if not next_page or len(matched_ids) >= max_hits:
            break
    return matched_ids
 
def mmr_select(query_vec: List[float], candidates_vecs: List[List[float]], k: int, lambda_mult: float) -> List[int]:
    """Select diverse results using Maximum Marginal Relevance (MMR).
    
    Implements MMR algorithm to balance relevance and diversity in search results.
    Iteratively selects candidates that maximize the weighted combination of
    query similarity and dissimilarity to already selected items.
    
    Args:
        query_vec (List[float]): Query embedding vector.
        candidates_vecs (List[List[float]]): List of candidate embedding vectors.
        k (int): Number of diverse results to select. Range: [1, len(candidates_vecs)].
        lambda_mult (float): Balance parameter between relevance and diversity.
            Range: [0.0, 1.0]. Higher values favor relevance, lower values favor diversity.
    
    Returns:
        List[int]: List of indices into candidates_vecs representing the selected
            diverse results, ordered by selection priority.
    
    Example:
        >>> query_vec = [1.0, 0.0, 0.0]
        >>> candidates = [[0.9, 0.1, 0.0], [0.8, 0.2, 0.0], [0.1, 0.9, 0.0]]
        >>> selected = mmr_select(query_vec, candidates, k=2, lambda_mult=0.7)
        >>> len(selected)
        2
        >>> selected[0] == 0  # Most similar to query selected first
        True
    """
    import numpy as np
    V = np.array(candidates_vecs, dtype=float)
    q = np.array(query_vec, dtype=float)
    def cos(a, b):
        na = (a @ a) ** 0.5 + 1e-12
        nb = (b @ b) ** 0.5 + 1e-12
        return float((a @ b) / (na * nb))
    sims = [cos(v, q) for v in V]
    selected: List[int] = []
    remaining = set(range(len(V)))
    while len(selected) < min(k, len(V)):
        if not selected:
            best = max(remaining, key=lambda i: sims[i])
            selected.append(best)
            remaining.remove(best)
            continue
        best_idx = None
        best_score = -1e9
        for i in remaining:
            max_div = max([cos(V[i], V[j]) for j in selected]) if selected else 0.0
            score = lambda_mult * sims[i] - (1 - lambda_mult) * max_div
            if score > best_score:
                best_score = score
                best_idx = i
        selected.append(best_idx)
        remaining.remove(best_idx)
    return selected
 
def hybrid_search(client: QdrantClient, settings: Settings, query: str, embeddings: AzureOpenAIEmbeddings):
    """Hybrid search combining semantic similarity, text matching, and MMR diversification.
    
    Performs a sophisticated hybrid search that:
    1. Conducts semantic search to find similar vectors
    2. Performs text search to find keyword matches
    3. Fuses scores using weighted combination with text boost
    4. Optionally applies MMR for result diversification
    
    Args:
        client (QdrantClient): Qdrant client for database operations.
        settings (Settings): Configuration containing search parameters (alpha,
            text_boost, use_mmr, mmr_lambda, final_k, etc.).
        query (str): Text query to search for.
        embeddings (AzureOpenAIEmbeddings): Embeddings model for query encoding.
    
    Returns:
        List: List of Qdrant points representing the best matching documents,
            limited to settings.final_k results.
    
    Raises:
        Exception: If semantic search, text search, or embedding operations fail.
    
    Example:
        >>> client = get_qdrant_client(Settings())
        >>> settings = Settings()
        >>> embeddings = get_embeddings(settings)
        >>> results = hybrid_search(client, settings, "machine learning", embeddings)
        >>> len(results) <= settings.final_k
        True
    """
    sem = qdrant_semantic_search(client, settings, query, embeddings, limit=settings.top_n_semantic, with_vectors=True)
    if not sem: return []
    text_ids = set(qdrant_text_prefilter_ids(client, settings, query, settings.top_n_text))
    scores = [p.score for p in sem]
    smin, smax = min(scores), max(scores)
    def norm(x): return 1.0 if smax == smin else (x - smin) / (smax - smin)
    fused: List[Tuple[int, float, Any]] = []
    for idx, p in enumerate(sem):
        base = norm(p.score)
        fuse = settings.alpha * base
        if p.id in text_ids:
            fuse += settings.text_boost
        fused.append((idx, fuse, p))
    fused.sort(key=lambda t: t[1], reverse=True)
    if settings.use_mmr:
        def embed_mmr_query():
            return embeddings.embed_query(query)
        
        qv = retry_with_backoff(embed_mmr_query, max_retries=5, base_delay=2.0)
        N = min(len(fused), max(settings.final_k * 5, settings.final_k))
        cut = fused[:N]
        vecs = [sem[i].vector for i, _, _ in cut]
        mmr_idx = mmr_select(qv, vecs, settings.final_k, settings.mmr_lambda)
        return [cut[i][2] for i in mmr_idx]
    return [p for _, _, p in fused[:settings.final_k]]
 
# ========== Prompt/Chain ==========
 
def format_docs_for_prompt(points: Iterable[Any]) -> str:
    """Format documents with source citations for LLM prompts.
    
    Converts Qdrant points into a formatted string suitable for use in LLM prompts,
    with each document prefixed by its source file for citation purposes.
    
    Args:
        points (Iterable[Any]): Iterable of Qdrant points with payload containing
            'source' and 'text' fields.
    
    Returns:
        str: Formatted string with documents separated by double newlines,
            each prefixed with [source:filename] citation.
    
    Example:
        >>> class MockPoint:
        ...     def __init__(self, source, text):
        ...         self.payload = {"source": source, "text": text}
        >>> points = [MockPoint("doc1.pdf", "Content 1"), MockPoint("doc2.md", "Content 2")]
        >>> result = format_docs_for_prompt(points)
        >>> "[source:doc1.pdf] Content 1" in result
        True
        >>> "[source:doc2.md] Content 2" in result
        True
    """
    blocks = []
    for p in points:
        pay = p.payload or {}
        src = pay.get("source", "unknown")
        blocks.append(f"[source:{src}] {pay.get('text','')}")
    return "\n\n".join(blocks)

# RAGAS

def get_contexts_for_question(client, settings, embeddings, question: str, k: int) -> List[str]:
    """Return the top-k document chunks used as context for a question.
    
    Retrieves relevant document chunks for a given question using hybrid search
    and extracts only the text content for use as context in RAG evaluation.
    
    Args:
        client: Qdrant client for database operations.
        settings: Configuration object with search parameters.
        embeddings: Embeddings model for query encoding.
        question (str): Question to find relevant context for.
        k (int): Number of context chunks to retrieve. Range: [1, 100].
    
    Returns:
        List[str]: List of text strings representing the most relevant
            document chunks for the question.
    
    Example:
        >>> client = get_qdrant_client(Settings())
        >>> settings = Settings()
        >>> embeddings = get_embeddings(settings)
        >>> contexts = get_contexts_for_question(client, settings, embeddings, "What is AI?", 3)
        >>> len(contexts) <= 3
        True
        >>> all(isinstance(ctx, str) for ctx in contexts)
        True
    """
    docs = hybrid_search(client, settings, question, embeddings)
    return [d.payload.get('text', '') for d in docs]

def extract_context_texts(points: Iterable[Any]) -> List[str]:
    """Extract individual context texts from Qdrant points for RAGAS evaluation.
    
    Extracts text content from Qdrant points for use in RAGAS (RAG Assessment)
    evaluation metrics. Specifically designed to provide context texts for
    evaluating retrieval quality.
    
    Args:
        points (Iterable[Any]): Iterable of Qdrant points with payload containing
            'text' field.
    
    Returns:
        List[str]: List of text strings extracted from the points' payloads.
    
    Example:
        >>> class MockPoint:
        ...     def __init__(self, text):
        ...         self.payload = {"text": text}
        >>> points = [MockPoint("Context 1"), MockPoint("Context 2")]
        >>> texts = extract_context_texts(points)
        >>> texts
        ['Context 1', 'Context 2']
    """
    context_texts = []
    for p in points:
        pay = p.payload or {}
        context_texts.append(pay.get('text', ''))
    return context_texts

def build_rag_chain(llm):
    """Build a RAG (Retrieval-Augmented Generation) chain for question answering.
    
    Creates a LangChain runnable chain that combines retrieved context with
    a language model to answer questions. The chain is configured to provide
    accurate, source-cited responses based only on provided context.
    
    Args:
        llm: Language model instance for generating responses.
    
    Returns:
        Any: LangChain runnable chain that takes context and question as input
            and returns a string response with source citations.
    
    Example:
        >>> # Assuming you have an LLM instance
        >>> llm = get_llm(Settings())
        >>> if llm:
        ...     chain = build_rag_chain(llm)
        ...     # chain can be invoked with {"context": "...", "question": "..."}
        ... else:
        ...     chain = None
    """
    system_prompt = (
        "You are a technical assistant. Answer in English, concisely and accurately. "
        "Use ONLY the information present in the CONTENT. "
        "If it is not present, state: 'Not present in the provided context.' "
        "Always cite sources in the format [source:FILE]."
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human",
         "Question:\n{question}\n\n"
         "CONTENT:\n{context}\n\n"
         "Instructions:\n"
         "1) Answer based only on the content.\n"
         "2) Include citations [source:...].\n"
         "3) No inventions.")
    ])

    chain = (
        {
            "context": RunnablePassthrough(),  # stringa già formattata
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
 
# ========== Main ==========
 
def rag_search(question, k):
    """Perform end-to-end RAG search for a question.
    
    Executes a complete RAG pipeline: loads documents, creates embeddings,
    stores in Qdrant, performs hybrid search, and returns formatted context.
    This is the main entry point for the RAG system.
    
    Args:
        question: Text question to search for relevant context.
        k: Number of relevant documents to retrieve and return.
            Range: [1, 100].
    
    Returns:
        str: Formatted context string with source citations, ready for use
            in LLM prompts. Documents are separated by double newlines and
            prefixed with [source:filename] tags.
    
    Raises:
        Exception: If document loading, embedding, Qdrant operations, or
            search operations fail.
    
    Example:
        >>> context = rag_search("What is machine learning?", 3)
        >>> "[source:" in context
        True
        >>> len(context) > 0
        True
    """
    s = SETTINGS
    
    s.final_k = k
    
    embeddings = get_embeddings(s)
    llm = get_llm(s)  # opzionale

    # 1) Client Qdrant
    client = get_qdrant_client(s)

    # 2) Dati -> chunk
    # docs = simulate_corpus()
    docs = load_docs_from_directory(os.path.join(CURRENT_DIRECTORY_PATH, "docs"))
    chunks = split_documents(docs, s, embeddings)

    # 3) Crea (o ricrea) collection
    vector_size = len(embeddings.embed_query("test"))
    
    recreate_collection_for_rag(client, s, vector_size)

    # 4) Upsert chunks
    upsert_chunks(client, s, chunks, embeddings)
    
    contexts = hybrid_search(client, s, question, embeddings)
    
    # For the LLM chain: formatted concatenated string
    ctx = format_docs_for_prompt(contexts)
    
    return ctx