### LLM Rerank response parser:

        /usr/local/python/3.11.9/lib/python3.11/site-packages/llama_index/core/indices/utils.py
                self._parse_choice_select_answer_fn = (
            parse_choice_select_answer_fn or default_parse_choice_select_answer_fn
        )

### ACtivate .venv with poetry:

node ➜ /workspaces/airtable-chat-2/backend (main) $ poetry shell
Spawning shell within /workspaces/airtable-chat-2/backend/.venv
. /workspaces/airtable-chat-2/backend/.venv/bin/activate

### App problems

1) llmrerank sometimes returns less than 8 nodes, it seems the references streaming using events callback 
only cares about retrieval and doesn't take into account llmrerank
Probably there is no event callback setup on llmrerank.

2) llmrerank llm also gets creative sometimes adding explation to the answers, need to update to a pydantic response
instead of this crappy text format.

3) Need to create a custom NodeInfo component for the front-end
