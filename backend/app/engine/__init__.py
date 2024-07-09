import os
# from app.engine.index import get_index
from fastapi import HTTPException

from app.engine.prompts import query_engine_prompt
from app.engine.semantic_indexer import SemanticIndexer
from app.engine.vector_store import get_vector_store
from llama_index.core.chat_engine.types import BaseChatEngine


def get_chat_engine_old():
    system_prompt = os.getenv("SYSTEM_PROMPT")
    top_k = os.getenv("TOP_K", 3)

    vector_store = get_vector_store()
    index = SemanticIndexer(vector_store).vector_store_index
    if index is None:
        raise HTTPException(
            status_code=500,
            detail=str(
                "StorageContext is empty - call 'poetry run generate' to generate the storage first"
            ),
        )

    return index.as_chat_engine(
        similarity_top_k=int(top_k),
        system_prompt=system_prompt,
        chat_mode="condense_plus_context",
    )

def get_chat_engine() -> BaseChatEngine:
    system_prompt = query_engine_prompt
    vector_store = get_vector_store()
    semantic_indexer = SemanticIndexer(vector_store)
    return semantic_indexer.as_chat_engine(system_prompt)
