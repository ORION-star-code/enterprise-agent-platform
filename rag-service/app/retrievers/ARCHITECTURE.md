# Retrievers Architecture

## Responsibility
Search and ranking logic for the RAG pipeline. Combines multiple retrieval strategies.

## Components
- **DenseRetriever**: Cosine similarity search on hash-based embeddings
- **KeywordRetriever**: Feature overlap scoring for exact term matching
- **SimpleReranker**: Merges results with configurable weighting (default: 65% dense, 35% keyword)
- **HybridRetriever**: Orchestrates dense + keyword retrieval and reranking

## Search Flow
1. Query text received
2. DenseRetriever computes cosine similarity against stored chunk embeddings
3. KeywordRetriever computes feature overlap scores
4. SimpleReranker merges and re-ranks results with weighted scoring
5. Top-K results returned

## Constraints
- Embedding dimension determined by HashEmbeddingClient (configurable in embedding_config.py)
- Reranker weights are configurable but default to 65/35
- Metadata filtering applied before ranking
