from typing import Sequence
from app.engine.vector_store import get_vector_store
import logging
from llama_index.core.indices import VectorStoreIndex
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.core.schema import BaseNode
from llama_index.llms.openai import OpenAI
from llama_index.core.postprocessor.llm_rerank import LLMRerank
from llama_index.core.chat_engine.types import BaseChatEngine, ChatMode
from llama_index.core.base.base_query_engine import BaseQueryEngine
from llama_index.core.vector_stores.types import BasePydanticVectorStore
import os

DEFAULT_SYSTEM_PROMPT = "You are an helpful assistant. Please provide detailed and factual responses."

class SemanticIndexer:
    def __init__(self, vector_store: BasePydanticVectorStore):
        self._semantic_query_engine = None
        self.vector_store = vector_store 
        self.embed_model = OpenAIEmbedding(model="text-embedding-3-small", dimension=1536, api_key=os.environ['OPENAI_API_KEY'])
        self._vector_store_index = None
        self._semantic_query_engine = None
        self._chat_engine = None
                # global
        Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small", dimension=1536)

    def _need_to_build_index(self) -> bool:
        # Implement the logic to check if the index needs to be built
        # Return True if it needs to be built, False otherwise
        return False

    def _get_vector_store_index(self):
        # TO DO: query vector store to find out if there is anything we need to build 
        # if YES: build vector store index, if NO: return without building
        logging.log(logging.INFO, f'===Get VectorStoreIndex=== members_and_build_updates using openai text-embedding-3-small dim 1536')
        embed_model = OpenAIEmbedding(model="text-embedding-3-small", dimension=1536, api_key=os.environ['OPENAI_API_KEY'])
        self._vector_store_index = VectorStoreIndex.from_vector_store(self.vector_store, use_async=True, embed_model=embed_model)
    
    def _add_nodes_to_vector_store_index(self, nodes: Sequence[BaseNode]):
        logging.log(logging.INFO, f'===BUILD VECTOR STORE INDEX insert nodes into supabase === members_and_build_updates')
        #nodes = self.reader.extract_nodes()

        self._vector_store_index.insert_nodes(self, nodes)
    
    def build(self, nodes=None):
        self._get_vector_store_index()
        if self._need_to_build_index():
            if nodes is not None and len(nodes) > 0:
                # add nodes to vector store index
                self._add_nodes_to_vector_store_index(nodes)
        return self._vector_store_index
    
    @property
    def vector_store_index(self) -> VectorStoreIndex:
        if self._vector_store_index is None:
            _ = self.build()
        return self._vector_store_index
    
    @property
    def semantic_query_engine(self) -> BaseQueryEngine:
        if self._vector_store_index is None:
            _ = self.build()

        if self._semantic_query_engine is None:
            llm = OpenAI(model="gpt-4o", temperature=0)
            print('NODE POSTPROCESSOR LLMRERANK')
            node_postprocessor = LLMRerank(llm=llm)
            #TODO: Maybe use graph query to return all relevant nodes / members
            self._semantic_query_engine = self._vector_store_index.as_query_engine(
                llm=llm, 
                # retriever kwargs
                similarity_top_k=8, 
                # post processing
                node_postprocessors=[node_postprocessor])
        return self._semantic_query_engine
    
    def as_chat_engine(self, system_prompt: str = DEFAULT_SYSTEM_PROMPT) -> BaseChatEngine:
        if self._vector_store_index is None:
            _ = self.build()

        if self._chat_engine is None:
            llm = OpenAI(model="gpt-4o", temperature=0)
            print('NODE POSTPROCESSOR LLMRERANK')
            node_postprocessor = LLMRerank(llm=llm)
            #TODO: Maybe use graph query to return all relevant nodes / members
            self._chat_engine = self._vector_store_index.as_chat_engine(
                chat_mode=ChatMode.CONDENSE_PLUS_CONTEXT,
                llm=llm, 
                # retriever kwargs
                similarity_top_k=8, 
                # post processing
                node_postprocessors=[node_postprocessor])
        return self._chat_engine
