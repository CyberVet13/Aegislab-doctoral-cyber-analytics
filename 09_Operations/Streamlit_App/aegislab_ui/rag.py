"""
AegisLab UI — single RAG over repo docs.
- Index: governance, agents (charters/templates), research methods, praxis artifact, session logs.
- Embeddings: OpenAI text-embedding-3-small via ChromaDB.
- Query returns top-k chunks for prompt augmentation.
"""

import os
from pathlib import Path
from typing import List, Optional, Tuple

from .config import get_root, get_path, load_env

load_env()

# Directories to index (relative to repo root). Markdown and text only.
RAG_SOURCE_DIRS = [
    "00_Governance",
    "02_Agents",
    "03_Research_Methods",
    "04_Praxis_Artifact",
    "09_Operations/Session_Logs",
    "09_Operations/Decision_Logs",
]

# Chunk size (chars) and overlap for splitting
CHUNK_SIZE = 1200
CHUNK_OVERLAP = 200

# Collection name and persist path
RAG_COLLECTION_NAME = "aegislab_docs"
RAG_PERSIST_DIR = "09_Operations/Streamlit_App/rag_index"


def _chunk_text(text: str, path: str) -> List[Tuple[str, str]]:
    """Split text into overlapping chunks. Return list of (chunk_text, path)."""
    chunks: List[Tuple[str, str]] = []
    text = text.strip()
    if not text:
        return []
    start = 0
    while start < len(text):
        end = start + CHUNK_SIZE
        if end < len(text):
            # Try to break at paragraph or sentence
            break_at = max(
                text.rfind("\n\n", start, end + 1),
                text.rfind("\n", start, end + 1),
                text.rfind(". ", start, end + 1),
            )
            if break_at > start:
                end = break_at + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append((chunk, path))
        start = end - CHUNK_OVERLAP
        if start >= len(text):
            break
    return chunks


def _list_md_files(root: Path, rel_dirs: List[str]) -> List[Tuple[Path, str]]:
    """Return list of (full_path, rel_path_str) for all .md files under rel_dirs."""
    out: List[Tuple[Path, str]] = []
    for rel in rel_dirs:
        dir_path = root / rel.replace("/", os.sep)
        if not dir_path.is_dir():
            continue
        for f in dir_path.rglob("*.md"):
            if f.is_file():
                try:
                    rel_str = str(f.relative_to(root)).replace("\\", "/")
                    out.append((f, rel_str))
                except ValueError:
                    pass
    return out


class RAG:
    """Single retrieval-augmented index over AegisLab repo docs."""

    def __init__(self, persist_path: Optional[Path] = None) -> None:
        self.root = get_root()
        self._persist = persist_path or get_path(RAG_PERSIST_DIR)
        self._client = None
        self._collection = None

    def _get_client(self):
        if self._client is None:
            try:
                import chromadb
                from chromadb.config import Settings
                self._client = chromadb.PersistentClient(
                    path=str(self._persist),
                    settings=Settings(anonymized_telemetry=False),
                )
            except ImportError as e:
                raise RuntimeError("chromadb not installed; pip install chromadb") from e
        return self._client

    def _get_embedding_function(self):
        try:
            from chromadb.utils import embedding_functions
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                return None
            return embedding_functions.OpenAIEmbeddingFunction(
                api_key=api_key,
                model_name="text-embedding-3-small",
            )
        except Exception:
            return None

    def build_index(self) -> Tuple[int, str]:
        """
        Index all RAG_SOURCE_DIRS. Return (num_chunks, message).
        Requires OPENAI_API_KEY.
        """
        ef = self._get_embedding_function()
        if ef is None:
            return 0, "OPENAI_API_KEY not set; cannot build index."
        client = self._get_client()
        self._persist.mkdir(parents=True, exist_ok=True)
        try:
            client.delete_collection(RAG_COLLECTION_NAME)
        except Exception:
            pass
        collection = client.create_collection(
            name=RAG_COLLECTION_NAME,
            embedding_function=ef,
            metadata={"description": "AegisLab repo docs"},
        )
        files = _list_md_files(self.root, RAG_SOURCE_DIRS)
        all_chunks: List[Tuple[str, str]] = []
        for full_path, rel_path in files:
            try:
                text = full_path.read_text(encoding="utf-8", errors="replace")
                all_chunks.extend(_chunk_text(text, rel_path))
            except Exception:
                continue
        if not all_chunks:
            return 0, "No chunks extracted from source dirs."
        ids = [f"chunk_{i}" for i in range(len(all_chunks))]
        documents = [c[0] for c in all_chunks]
        metadatas = [{"path": c[1]} for c in all_chunks]
        collection.add(ids=ids, documents=documents, metadatas=metadatas)
        return len(all_chunks), f"Indexed {len(all_chunks)} chunks from {len(files)} files."

    def is_ready(self) -> bool:
        """Return True if index exists and has documents."""
        try:
            client = self._get_client()
            coll = client.get_collection(name=RAG_COLLECTION_NAME)
            return coll.count() > 0
        except Exception:
            return False

    def query(self, question: str, k: int = 5) -> List[Tuple[str, str]]:
        """
        Return top-k (chunk_text, path) for the question.
        Returns [] if index not ready or embedding fails.
        """
        if not question or not question.strip():
            return []
        try:
            ef = self._get_embedding_function()
            if ef is None:
                return []
            client = self._get_client()
            coll = client.get_collection(name=RAG_COLLECTION_NAME, embedding_function=ef)
            if coll.count() == 0:
                return []
            results = coll.query(
                query_texts=[question.strip()],
                n_results=min(k, coll.count()),
                include=["documents", "metadatas"],
            )
            if not results or not results["documents"] or not results["documents"][0]:
                return []
            docs = results["documents"][0]
            metas = results.get("metadatas", [[]])
            meta_list = metas[0] if metas else []
            out: List[Tuple[str, str]] = []
            for i, doc in enumerate(docs):
                path = meta_list[i].get("path", "") if i < len(meta_list) else ""
                out.append((doc, path))
            return out
        except Exception:
            return []

    def get_context_block(self, question: str, k: int = 5, max_chars: int = 4000) -> str:
        """Format retrieved chunks as a single block for injection into the prompt."""
        chunks = self.query(question, k=k)
        if not chunks:
            return ""
        lines = ["## Retrieved context (from repo docs)", ""]
        total = 0
        for text, path in chunks:
            block = f"**Source:** `{path}`\n\n{text}\n\n"
            if total + len(block) > max_chars:
                break
            lines.append(block)
            total += len(block)
        return "\n".join(lines).strip()
