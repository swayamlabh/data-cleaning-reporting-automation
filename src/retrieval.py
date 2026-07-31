from dataclasses import dataclass


@dataclass(frozen=True)
class KnowledgeDocument:
    text: str
    source: str


def retrieve(query: str, documents: list[KnowledgeDocument], limit: int = 3) -> list[KnowledgeDocument]:
    """Dependency-free lexical retrieval seam for future vector/RAG backends."""
    terms = set(query.lower().split())
    return sorted(documents, key=lambda d: len(terms & set(d.text.lower().split())), reverse=True)[:limit]
