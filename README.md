
# Agno RAG Agente

**Agno RAG Agente** é um aplicativo de chat que combina modelos com geração aumentada por recuperação (RAG).
Permite que usuários façam perguntas baseadas na base de conhecimento do Agno, documentos e dados da web, recuperem respostas contextuais e mantenham o histórico de conversas entre sessões.
Este aplicativo, cujo código fonte é fornecido junto com o Agno, foi utilizado para demonstrar na prática a construção de bases de conhecimento
baseadas em código fonte. (Veja o artigo: https://www.linkedin.com/pulse/otimizando-o-tamanho-de-chunk-em-rag-para-bases-sistemas-glauber-duma-xf1tf)
No script `agentic_rag.py` fiz alguns ajustes para montar nossa base de conhecimento sobre o código fonte.
Optei por utilizar SqliteStorage e ChromaDb pela simplicidade e custo zero, mas nada impede que você utilize outras tecnologias.
Utilizei `text-embedding-3-small` como embedder, mas nada impede de utilizar outros embedders.
Sugiro que você faça testes, brinque à vontade e veja o que gera o melhor resultado.

Se precisar entrar em contato comigo, meu e-mail é glauber.duma@gmail.com.

> Nota: Faça um fork e clone este repositório se necessário


### 1. Crie um ambiente virtual

```shell
python3 -m venv .venv
source .venv/bin/activate
```


### 2. Instale as dependências

```shell
pip install -r requirements.txt
```


### 3. Configure as chaves de API

Obrigatório:
```bash
export OPENAI_API_KEY=sua_chave_openai_aqui
```


### 4. Construção da base de conhecimento

Clone o repositório do Agno:

Endereço do repositório: https://github.com/agno-agi/agno

Se necessário, edite o arquivo `agentic_rag.py` e ajuste o path na linha 60 do código.
Em seguida, execute:

```shell
python build_rag.py
```


### 5. Execute o Agentic RAG App

```shell
streamlit run app.py
```


### Como Usar
- Abra [localhost:8501](http://localhost:8501) no seu navegador.
- Digite perguntas na interface de chat e obtenha respostas contextuais.
- O app também pode responder perguntas usando busca DuckDuckGo sem necessidade de documentos externos.


### Solução de Problemas
- **Erros de API OpenAI**: Verifique se a variável `OPENAI_API_KEY` está definida e válida.


## 📚 Documentação

Para mais informações detalhadas:
- [Documentação Agno](https://docs.agno.com)
- [Documentação Streamlit](https://docs.streamlit.io)


## 🤝 Suporte

Precisa de ajuda? Participe da nossa [comunidade no Discord](https://agno.link/discord)



