# Vector Store Constraints

## Hard Constraints
- **Storage format**: JSON files (`documents.json`, `chunks.json`) in `rag-service/storage/`
- **Collection naming**: Lowercase alphanumeric + hyphens only
- **No concurrent writes**: Single-process access only (JSON files are not safe for concurrent writes)
- **Storage path**: Managed by `CollectionManager` — do not hardcode paths

## Migration Path
When moving to real Qdrant:
1. Implement a new store class matching the `LocalQdrantStore` interface
2. Update `CollectionManager` to point to Qdrant instance
3. No changes needed in API or retriever layers

## Known Limitations
- No persistence across collection recreation
- No built-in backup or replication
- Performance degrades with large datasets (>10K chunks)
