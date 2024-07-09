import os
from llama_index.vector_stores.supabase import SupabaseVectorStore
from llama_index.core.vector_stores.types import BasePydanticVectorStore

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)
SUPABASE_CONNECTION_STRING=os.getenv('SUPABASE_CONNECTION_STRING')

# class VectorStore():
#     def __init__(self):
#         if SUPABASE_CONNECTION_STRING is None or SUPABASE_CONNECTION_STRING == "":
#             raise ValueError("SUPABASE_CONNECTION_STRING environment variable is not set.")
        
#         self._vector_store = SupabaseVectorStore(
#             postgres_connection_string=SUPABASE_CONNECTION_STRING, 
#             collection_name='members_and_build_updates'
#         )
    
#     @property
#     def vector_store(self):
#         return self._vector_store
    
def get_vector_store() -> BasePydanticVectorStore:
    if not SUPABASE_CONNECTION_STRING:
        raise ValueError("SUPABASE_CONNECTION_STRING not set.")
    return SupabaseVectorStore(
        postgres_connection_string=SUPABASE_CONNECTION_STRING, 
        collection_name='members_and_build_updates'
    )