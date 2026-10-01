# Recommended Reading - Advanced Retrieval and Context Engineering

Written explainers (official docs, university notes, standard references, well-known engineering blogs) for every module concept.
Each page was fetched and its text read by a script that checks the page actually names the concepts listed under `Covers`.
Use these when a video is not enough or you prefer text; then do the module exercises.

### Module 01: Parsing & Hierarchical Semantic Chunking

- [LangChain overview - Docs by LangChain](https://docs.langchain.com/oss/python/langchain/overview) | **python.langchain.com** | Covers: Parsing
- [Chunking Strategies to Improve LLM RAG Pipeline Performance | Weaviate](https://weaviate.io/blog/chunking-strategies-for-rag) | **weaviate.io** | Covers: Hierarchical Semantic Chunking
- [Chunking Strategies for LLM Applications | Pinecone](https://www.pinecone.io/learn/chunking-strategies/) | **pinecone.io** | Covers: Parsing
- [Overview - Unstructured](https://docs.unstructured.io/open-source/introduction/overview) | **docs.unstructured.io** | Covers: Parsing
- [Partitioning - Unstructured](https://docs.unstructured.io/open-source/core-functionality/partitioning) | **docs.unstructured.io** | Covers: Parsing

### Module 02: Anthropic Contextual Retrieval Architecture

- [Contextual Retrieval in AI Systems \ Anthropic](https://www.anthropic.com/engineering/contextual-retrieval) | **anthropic.com** | Covers: Anthropic Contextual Retrieval Architecture
- [Embeddings - Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/embeddings) | **docs.anthropic.com** | Covers: Anthropic Contextual Retrieval Architecture

### Module 03: Vector Database Internals (HNSW & Product Quantization)

- [What is a Vector Database & How Does it Work? Use Cases + Examples | Pinecone](https://www.pinecone.io/learn/vector-database/) | **pinecone.io** | Covers: Vector Database Internals, HNSW, Product Quantization
- [Hierarchical Navigable Small Worlds (HNSW) | Pinecone](https://www.pinecone.io/learn/series/faiss/hnsw/) | **pinecone.io** | Covers: HNSW, Product Quantization
- [Product Quantization: Compressing high-dimensional vectors by 97% | Pinecone](https://www.pinecone.io/learn/series/faiss/product-quantization/) | **pinecone.io** | Covers: HNSW, Product Quantization
- [Home · facebookresearch/faiss Wiki · GitHub](https://github.com/facebookresearch/faiss/wiki) | **github.com** | Covers: Product Quantization

### Module 04: Hybrid Search & Reciprocal Rank Fusion (RRF)

- [Hybrid Search Explained | Weaviate](https://weaviate.io/blog/hybrid-search-explained) | **weaviate.io** | Covers: Hybrid Search, Reciprocal Rank Fusion, RRF
- [Hybrid Search Scoring (RRF) - Azure AI Search | Microsoft Learn](https://learn.microsoft.com/en-us/azure/search/hybrid-search-ranking) | **learn.microsoft.com** | Covers: Hybrid Search, Reciprocal Rank Fusion, RRF
- [Reciprocal rank fusion | Elasticsearch Reference](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion) | **elastic.co** | Covers: Reciprocal Rank Fusion, RRF
- [Getting Started with Hybrid Search | Pinecone](https://www.pinecone.io/learn/hybrid-search-intro/) | **pinecone.io** | Covers: Hybrid Search

### Module 05: Multi-Stage Retrieval & Cross-Encoder Reranking

- [Rerankers and Two-Stage Retrieval | Pinecone](https://www.pinecone.io/learn/series/rag/rerankers/) | **pinecone.io** | Covers: Multi-Stage Retrieval, Cross-Encoder Reranking
- [Retrieve & Re-Rank — Sentence Transformers documentation](https://www.sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) | **sbert.net** | Covers: Multi-Stage Retrieval, Cross-Encoder Reranking
- [Cross-Encoders — Sentence Transformers documentation](https://www.sbert.net/examples/cross_encoder/applications/README.html) | **sbert.net** | Covers: Cross-Encoder Reranking

### Module 06: ColBERTv2 & Token-Level Late Interaction

- [[2112.01488] ColBERTv2: Effective and Efficient Retrieval via Lightweight Late Interaction](https://arxiv.org/abs/2112.01488) | **arxiv.org** | Covers: ColBERTv2, Token-Level Late Interaction
- [GitHub - stanford-futuredata/ColBERT: ColBERT: state-of-the-art neural search (SIGIR'20, TACL'21, Ne](https://github.com/stanford-futuredata/ColBERT) | **github.com** | Covers: ColBERTv2, Token-Level Late Interaction
- [An Overview of Late Interaction Retrieval Models: ColBERT, ColPali, and ColQwen | Weaviate](https://weaviate.io/blog/late-interaction-overview) | **weaviate.io** | Covers: ColBERTv2, Token-Level Late Interaction

### Module 07: Microsoft GraphRAG & Community Summarization

- [What is GraphRAG?](https://neo4j.com/blog/genai/what-is-graphrag/) | **neo4j.com** | Covers: Microsoft GraphRAG, Community Summarization
- [Welcome - GraphRAG](https://microsoft.github.io/graphrag/) | **microsoft.github.io** | Covers: Microsoft GraphRAG
- [GraphRAG: Unlocking LLM discovery on narrative private data - Microsoft Research](https://www.microsoft.com/en-us/research/blog/graphrag-unlocking-llm-discovery-on-narrative-private-data/) | **microsoft.com** | Covers: Microsoft GraphRAG
- [[2404.16130] From Local to Global: A Graph RAG Approach to Query-Focused Summarization](https://arxiv.org/abs/2404.16130) | **arxiv.org** | Covers: Community Summarization

### Module 08: Query Transformation & Agentic Multi-Hop RAG

- [Query Transformations](https://www.langchain.com/blog/query-transformations) | **blog.langchain.dev** | Covers: Query Transformation, Agentic Multi-Hop RAG
- [Build a custom RAG agent with LangGraph - Docs by LangChain](https://docs.langchain.com/oss/python/langgraph/agentic-rag) | **langchain-ai.github.io** | Covers: Agentic Multi-Hop RAG

### Module 09: Context Optimization & Needle-in-a-Haystack (NIAH)

- [GitHub - gkamradt/needle-in-a-haystack: Doing simple retrieval from LLM models at various context le](https://github.com/gkamradt/needle-in-a-haystack) | **github.com** | Covers: Context Optimization, Needle-in-a-Haystack, NIAH
- [[2404.06654] RULER: What's the Real Context Size of Your Long-Context Language Models?](https://arxiv.org/abs/2404.06654) | **arxiv.org** | Covers: Context Optimization, NIAH
- [[2307.03172] Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) | **arxiv.org** | Covers: Context Optimization
- [Prompting Claude's long context window \ Anthropic](https://www.anthropic.com/news/prompting-long-context) | **anthropic.com** | Covers: Context Optimization
