# Agno RAG Agent

**Agno RAG Agent** is a chat application that combines models with retrieval-augmented generation (RAG).
It allows users to ask questions based on Agno's knowledge base, documents, and web data, retrieve context-aware answers, and maintain chat history across sessions.
This application, whose source code is provided along with Agno, was used to practically demonstrate the construction of knowledge bases
based on source code. (See article: https://www.linkedin.com/pulse/otimizando-o-tamanho-de-chunk-em-rag-para-bases-sistemas-glauber-duma-xf1tf)
In the `agentic_rag.py` script, I made some adjustments to build our knowledge base on top of the source code.
I chose to use SqliteStorage and ChromaDb for their simplicity and zero cost, but you are free to use other technologies.
I used `text-embedding-3-small` as the embedder, but you can use other embedders as well.
I suggest you run tests, experiment freely, and see what gives the best results.

If you need to contact me, my email is glauber.duma@gmail.com.

> Note: Fork and clone this repository if needed

### 1. Create a virtual environment

```shell
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```shell
pip install -r requirements.txt
```

### 3. Configure API keys

Required:
```bash
export OPENAI_API_KEY=your_openai_key_here
```

### 4. Build the knowledge base

Clone the Agno repository:

Repository URL: https://github.com/agno-agi/agno

If necessary, edit the `agentic_rag.py` file and adjust the path on line 60 of the code.
Then run:

```shell
python build_rag.py
```

### 5. Run the Agno RAG App

```shell
streamlit run app.py
```

### How to Use
- Open [localhost:8501](http://localhost:8501) in your browser.
- Type questions in the chat interface and get context-aware answers.
- The app can also answer questions using DuckDuckGo search without the need for external documents.

### Troubleshooting
- **OpenAI API Errors**: Make sure the `OPENAI_API_KEY` variable is set and valid.

## 📚 Documentation

For more detailed information:
- [Agno Documentation](https://docs.agno.com)
- [Streamlit Documentation](https://docs.streamlit.io)

## 🤝 Support

Need help? Join our [Discord community](https://agno.link/discord)

