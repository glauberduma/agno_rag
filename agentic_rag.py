"""🤖 Agentic RAG Agent - Your AI Knowledge Assistant!

This advanced example shows how to build a sophisticated RAG (Retrieval Augmented Generation) system that
leverages vector search and LLMs to provide deep insights from any knowledge base.

The agent can:
- Process and understand documents from multiple sources (PDFs, websites, text files)
- Build a searchable knowledge base using vector embeddings
- Maintain conversation context and memory across sessions
- Provide relevant citations and sources for its responses
- Generate summaries and extract key insights
- Answer follow-up questions and clarifications

Example queries to try:
- "What are the key points from this document?"
- "Can you summarize the main arguments and supporting evidence?"
- "What are the important statistics and findings?"
- "How does this relate to [topic X]?"
- "What are the limitations or gaps in this analysis?"
- "Can you explain [concept X] in more detail?"
- "What other sources support or contradict these claims?"

The agent uses:
- Vector similarity search for relevant document retrieval
- Conversation memory for contextual responses
- Citation tracking for source attribution
- Dynamic knowledge base updates

View the README for instructions on how to run the application.
"""

from typing import Optional

from agno.agent import Agent
from agno.embedder.openai import OpenAIEmbedder
from agno.knowledge import AgentKnowledge
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.storage.sqlite import SqliteStorage
from agno.vectordb.chroma import ChromaDb
from agno.document.chunking.fixed import FixedSizeChunking
from dotenv import load_dotenv
from agno_knowledge import AgnoKnowledgeBase


load_dotenv()


db_storage = SqliteStorage(table_name="agno_base", db_file="./db/sqlite.db")
    
vectordb = ChromaDb(
        collection="agno_documentation",
        path="./tmp/chroma",
        persistent_client=True,        
        embedder=OpenAIEmbedder(id="text-embedding-3-small"),
    )
    
knowledge_base = AgentKnowledge(vector_db=vectordb, num_documents=50)
knowledge_source = AgnoKnowledgeBase(
    path="c:/agno",
    formats=[".py", ".sh", ".md"],
    vector_db=vectordb,
    chunking_strategy=FixedSizeChunking(
        chunk_size=500,
        overlap=50
    )
)

def get_agentic_rag_agent(
    model_id: str = "gpt-4.1",
    user_id: Optional[str] = None,
    session_id: Optional[str] = None,
    debug_mode: bool = True,
) -> Agent:
    """Get an Agentic RAG Agent with Memory."""

    model = OpenAIChat(id=model_id)
    # Define persistent memory for chat history

    # Define the knowledge base

    # Create the Agent
    return Agent(
        name="agentic_rag_agent",
        session_id=session_id,  # Track session ID for persistent conversations
        user_id=user_id,
        model=model,
        storage=db_storage,  # Persist session data
        knowledge=knowledge_base,  # Add knowledge base
        description="Você é um agente prestativo chamado 'Agno Agentic RAG' e seu objetivo é ajudar o usuário da melhor forma nas questões relativa ao Agno.",
        instructions=[
            "0. Idioma e saudação:",
            "   - SEMPRE utilize o idioma portugues brasileiro",
            "   - Seja cordial, cumprimente o usuário de forma amigável e profissional.",
            "   - Pergunte como você pode ajudar.",
            "1. Busca na Base de Conhecimento:",
            "   - SEMPRE comece buscando na base de conhecimento usando a ferramenta search_knowledge_base",
            "   - Analise TODOS os documentos retornados cuidadosamente antes de responder",
            "   - Se múltiplos documentos forem retornados, sintetize as informações de forma coerente",
            "2. Busca Externa:",
            "   - Se a busca na base de conhecimento não for suficiente, utilize duckduckgo_search",
            "   - Foque em fontes confiáveis e informações recentes",
            "   - Faça a conferência cruzada das informações de múltiplas fontes quando possível",
            "3. Gestão de Contexto:",
            "   - Use a ferramenta get_chat_history para manter a continuidade da conversa",
            "   - Faça referência a interações anteriores quando relevante",
            "   - Mantenha o registro das preferências do usuário e esclarecimentos prévios",
            "4. Qualidade da Resposta:",
            "   - Forneça citações e fontes específicas para as afirmações",
            "   - Estruture as respostas com seções claras e tópicos quando apropriado",
            "   - Inclua citações relevantes dos materiais de origem",
            "   - Evite frases como 'com base no meu conhecimento' ou 'dependendo da informação'",
            "5. Interação com o Usuário:",
            "   - Peça esclarecimentos se a pergunta for ambígua",
            "   - Divida perguntas complexas em partes gerenciáveis",
            "   - Sugira proativamente tópicos relacionados ou perguntas de acompanhamento",
            "6. Tratamento de Erros:",
            "   - Se nenhuma informação relevante for encontrada, declare isso claramente",
            "   - Sugira abordagens ou perguntas alternativas",
            "   - Seja transparente sobre as limitações das informações disponíveis"
            ],
        search_knowledge=True,  # This setting gives the model a tool to search the knowledge base for information
        read_chat_history=True,  # This setting gives the model a tool to get chat history
        tools=[DuckDuckGoTools()],
        markdown=True,  # This setting tellss the model to format messages in markdown
        # add_chat_history_to_messages=True,
        show_tool_calls=True,
        add_history_to_messages=True,  # Adds chat history to messages
        add_datetime_to_instructions=True,
        debug_mode=debug_mode,
        read_tool_call_history=True,
        num_history_responses=3,
    )
