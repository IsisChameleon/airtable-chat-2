### LLM Rerank response parser:

        /usr/local/python/3.11.9/lib/python3.11/site-packages/llama_index/core/indices/utils.py
                self._parse_choice_select_answer_fn = (
            parse_choice_select_answer_fn or default_parse_choice_select_answer_fn
        )

### poetry config

./home/node/.config/pypoetry/config.toml

node ➜ /workspaces/airtable-chat-2/backend (main) $ poetry config --list
cache-dir = "/home/node/.cache/pypoetry"
experimental.system-git-client = false
installer.max-workers = null
installer.modern-installation = true
installer.no-binary = null
installer.parallel = true
keyring.enabled = true
solver.lazy-wheel = true
virtualenvs.create = false
virtualenvs.in-project = true
virtualenvs.options.always-copy = false
virtualenvs.options.no-pip = false
virtualenvs.options.no-setuptools = false
virtualenvs.options.system-site-packages = false
virtualenvs.path = "{cache-dir}/virtualenvs"  # /home/node/.cache/pypoetry/virtualenvs
virtualenvs.prefer-active-python = false
virtualenvs.prompt = "{project_name}-py{python_version}"
warnings.export = true