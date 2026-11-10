# Applied AI / LLM Engineer — Complete Career Learning Roadmap
### YouTube-Only Curriculum · 100% Verified Links · Sequential Mastery Path

> **Your Target:** Become a high-impact engineer capable of designing, building, optimizing, deploying, and operating production-grade AI applications, autonomous agents, and scalable LLM inference infrastructure.
>
> **Core Principle:** We are not training to become someone who merely glues together third-party API demos. We are training to become an engineer who can **design, develop, optimize, benchmark, deploy, and maintain robust, high-performance software and AI systems at scale**.

---

## 📊 Master Completion Tracker

Use this checklist directly in GitHub to track your progress through the 11 sequential phases, 5 portfolio systems, and interview drills.

- [ ] **Phase 01:** Python Mastery (Internals, OOP, Async, Typing & Packaging)
- [ ] **Phase 02:** Data Structures and Algorithms (NeetCode 150, Patterns & Timed Practice)
- [ ] **Phase 03:** Backend Engineering, Databases and Networking (FastAPI, PostgreSQL, Redis, Networks)
- [ ] **Phase 04:** Low-Level Design & Software Engineering (SOLID, GoF Patterns & Architecture)
- [ ] **Phase 05:** High-Level Design & Distributed Systems (Scalability, Sharding, Caching & Kafka)
- [ ] **Phase 06:** Machine Learning (Statistical Foundations, Tree Ensembles & Pipelines)
- [ ] **Phase 07:** Deep Learning & Transformers (Micrograd, Backpropagation, PyTorch & GPT)
- [ ] **Phase 08:** Generative AI & LLM Engineering (Architectures, RAG, LoRA/QLoRA & Quantization)
- [ ] **Phase 09:** Agentic AI Engineering (LangGraph, MCP Tooling, Memory & Orchestration)
- [ ] **Phase 10:** MLOps, LLMOps, Cloud & Infrastructure (Docker, K8s, vLLM Serving & LiteLLM)
- [ ] **Phase 11:** AI Cybersecurity & Red Teaming (Prompt Injection, PyRIT & Threat Modeling)
- [ ] **Portfolio:** 5 Mandatory Production-Grade Systems Built, Tested, and Deployed
- [ ] **Interview:** Python, DSA, SQL, System Design & Behavioral Loops Mastered

---

## 🗺️ The Roadmap at a Glance

| Phase | Core Domain | Priority | Primary Target Outcome |
|:---:|:---|:---:|:---|
| **01** | **Python Mastery** | `Essential` | Write idiomatic, typed, async, thread-safe, and packaged Python code |
| **02** | **Data Structures & Algorithms** | `Essential` | Solve 150–250 LeetCode/NeetCode problems with optimal time/space complexity |
| **03** | **Backend, Databases & Networks** | `Essential` | Build multi-tenant, high-throughput asynchronous REST/WebSocket APIs with PostgreSQL & Redis |
| **04** | **Low-Level Design (LLD)** | `Essential` | Design extensible, modular object-oriented systems using SOLID and GoF design patterns |
| **05** | **High-Level Design (HLD)** | `Essential` | Architect fault-tolerant, horizontally scalable distributed systems and event streams |
| **06** | **Machine Learning** | `Essential` | Train, validate, tune, and evaluate classical predictive regression & classification pipelines |
| **07** | **Deep Learning & Transformers** | `Essential` | Implement backpropagation and Transformer attention blocks from scratch in pure PyTorch |
| **08** | **Generative AI & LLM Engineering** | `Highest` | Build hybrid RAG engines, evaluate hallucinations, and fine-tune models with PEFT/QLoRA |
| **09** | **Agentic AI Engineering** | `Highest` | Orchestrate cyclical stateful agents, MCP tools, persistent memory, and human approval gates |
| **10** | **MLOps, LLMOps & Infrastructure** | `Highest` | Serve models with vLLM PagedAttention, containerize with Docker/K8s, and benchmark inference |
| **11** | **AI Security & Red Teaming** | `Important` | Defend LLMs and agents against prompt injections, data exfiltration, and insecure tool calls |

---

## ⏱️ Recommended Study Time Allocation

For working engineers dedicating **25–30 hours per week**, allocate your study focus according to this career-weighted distribution:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                             CAREER STUDY TIME ALLOCATION (100%)                                  │
├──────────────────────────────────────┬─────────────┬─────────────────────────────────────────────┤
│ Focus Area                           │ Allocation  │ Primary Activities                          │
├──────────────────────────────────────┼─────────────┼─────────────────────────────────────────────┤
│ Python, Backend, DBs & Software Eng  │ **25%**     │ FastAPI, PostgreSQL MVCC, Redis, AsyncIO    │
│ DSA, LLD & High-Level System Design  │ **20%**     │ NeetCode 150, Object modeling, HLD whiteboards│
│ Machine Learning & LLM Engineering   │ **30%**     │ PyTorch, Transformers, Hybrid RAG, Fine-tune│
│ Agentic AI, MLOps & Infrastructure   │ **20%**     │ LangGraph, MCP, vLLM, Docker, Cloud Serving │
│ AI Security & Interview Revision     │ **5%**      │ PyRIT red-teaming, Mock interview defense   │
└──────────────────────────────────────┴─────────────┴─────────────────────────────────────────────┘
```

---

# 📚 Detailed Step-by-Step Learning Sequence

---

### Phase 1 — Master Python (Start Here)
*You need to become exceptionally comfortable with Python: not just writing simple scripts, but mastering how the language, object model, and runtime work under the hood.*

#### 📺 Curated Learning Resources
- [ ] **Order 01 · [Harvard CS50P — Python Programming Complete Course](https://www.youtube.com/playlist?list=PLhQjrBD2T3817j24-GogXmWqO5Q5vYy0V)**  
  *Action:* Complete the foundational series covering functions, conditionals, loops, exceptions, libraries, unit testing, file I/O, regex, and OOP.
- [ ] **Order 02 · [Corey Schafer — Advanced Python and Software Programming](https://www.youtube.com/@coreyms/playlists)**  
  *Action:* Complete playlists covering Type Hints, AsyncIO, Generators, Decorators, Context Managers, Multiprocessing, and Threading.
- [ ] **Order 03 · [ArjanCodes — Python Engineering & Architecture](https://www.youtube.com/@ArjanCodes/playlists)**  
  *Action:* Study clean code principles, architectural decoupling, dependency injection, and modern Pythonic paradigms.

#### 🧠 Concepts to Master
- Python internals: Object model, memory layout, reference counting, cyclic garbage collection, and descriptors.
- Object-Oriented Programming: Inheritance, composition vs inheritance, abstract base classes (`abc`), and polymorphism.
- Metaprogramming & syntax: Decorators (with and without arguments), generators (`yield`), iterators, and context managers (`contextlib`).
- Type safety: Type hints, generics (`TypeVar`), protocols (`typing.Protocol`), and schema validation with Pydantic.
- Error handling: Exception hierarchies, context-preserving error chaining (`raise from`), and structured JSON logging.
- Concurrency models: Multithreading, multiprocessing, AsyncIO event loops, tasks, and task groups.
- CPython runtime: GIL (Global Interpreter Lock), CPU-bound vs I/O-bound bottlenecks, and free-threaded execution.
- Quality tooling: Unit testing with `pytest`, mocking (`unittest.mock`), and modern packaging (`pyproject.toml`, `uv`, `poetry`).
- Profiling: Runtime profiling (`cProfile`, `py-spy`), memory benchmarking (`tracemalloc`), and optimization.

> 🛡️ **Phase 1 Exit Project:**  
> Build a production-grade, reusable Python package with asynchronous workers, static type hints (`mypy`/`pyright`), structured logging, comprehensive `pytest` test suites, and clean packaging metadata.

---

### Phase 2 — Data Structures and Algorithms (Interview Preparation)
*Non-negotiable foundation for senior, staff, and competitive engineering interviews across top tech and frontier AI labs.*

#### 📺 Curated Learning Resources
- [ ] **Order 04 · [NeetCode 150 — Complete 39-Hour Full DSA Course](https://www.youtube.com/watch?v=T0u5nwSA0w0)**  
  *Action:* Work through all 150 essential interview problems across arrays, sliding windows, graphs, DP, and heaps.
- [ ] **Order 05 · [NeetCode — Algorithm Playlists & Walkthroughs](https://www.youtube.com/@NeetCode/playlists)**  
  *Action:* Deep dive into targeted category playlists to drill into weak areas (Graphs, 2D Dynamic Programming, Backtracking).

#### 🧠 Concepts to Master
- Core linear structures: Arrays, two pointers, sliding window technique, strings, and prefix sums.
- Hash-based lookups: Hash tables, collision resolution, hash sets, and monotonic stacks/queues.
- Trees & Graphs: Binary Search Trees (BST), Heaps (Priority Queues), Tries (Prefix Trees), BFS, DFS, and topological sort.
- Graph algorithms: Shortest path (Dijkstra), minimum spanning trees, and Disjoint-Set Union (Union-Find with path compression).
- Algorithmic strategies: Sorting (Merge Sort, Quick Sort), binary search variants, recursion, backtracking, and greedy choices.
- Dynamic Programming: 1D memoization/tabulation, 2D state transitions, unbounded knapsack, and longest common subsequence.
- Asymptotic analysis: Rigorous Big-O time and space complexity derivations for all solutions.

> 🛡️ **Phase 2 Exit Requirement:**  
> Complete 150 problems from NeetCode independently, followed by an additional 50–100 mixed problems. Must be able to explain the intuition, edge cases, and exact time/space complexity under timed constraints without assistance.

---

### Phase 3 — Backend Engineering, Databases and Networking
*This is where you bridge from an AI demo-builder to a production software engineer capable of running mission-critical backends.*

#### 📺 Curated Learning Resources
- [ ] **Order 06 · [Corey Schafer — FastAPI Full Course (2026 Production Edition)](https://www.youtube.com/watch?v=iukOehU5aF4)**  
  *Action:* Complete the 13-hour comprehensive course: REST APIs, SQLAlchemy, PostgreSQL, authentication, async operations, testing, and Docker deployment.
- [ ] **Order 07 · [Hussein Nasser — Backend Engineering: Beginner](https://www.youtube.com/playlist?list=PLQnljOFTspQUNnO4p00ua_C5mKTfldiYT)**  
  *Action:* Understand backend server models, client-server communication, request-response lifecycles, and network listeners.
- [ ] **Order 08 · [Hussein Nasser — Backend Engineering: Intermediate](https://www.youtube.com/playlist?list=PLQnljOFTspQWGuRmwojJ6LiV0ejm6eOcs)**  
  *Action:* Master process pools, thread models, kernel socket buffers, connection pooling, and multi-tier architectures.
- [ ] **Order 09 · [Hussein Nasser — Backend Engineering: Advanced](https://www.youtube.com/playlist?list=PLQnljOFTspQUybacGRk1b_p13dgI-SmcZ)**  
  *Action:* Study distributed failure modes, connection draining, HTTP multiplexing, edge proxies, and reverse proxies.
- [ ] **Order 10 · [Hussein Nasser — Database Engineering Fundamentals & Internals](https://www.youtube.com/playlist?list=PLQnljOFTspQXjD0HOzN7P2tgzu7scWpl2)**  
  *Action:* Deep dive into database storage engines: B-Trees, LSM-Trees, WAL logs, ACID transactions, locking, and concurrency control.
- [ ] **Order 11 · [Hussein Nasser — Network Engineering Course](https://www.youtube.com/playlist?list=PLQnljOFTspQUBSgBXilKhRMJ1ACqr7pTr)**  
  *Action:* Master TCP 3-way handshakes, UDP, TLS 1.3 cryptographic handshakes, DNS caching, and IP routing.

#### 🧠 Concepts to Master
- Backend API architecture: FastAPI, Pydantic v2 schemas, dependency injection, middleware chains, WebSockets, and Server-Sent Events (SSE).
- API security: OAuth2, OpenID Connect, JWT signing and verification, API key management, and CORS configuration.
- Relational databases (PostgreSQL): Advanced SQL queries, indexing strategies (B-Tree, GIN, GiST), MVCC, transaction isolation levels (Read Committed vs Serializable), and schema migrations with Alembic.
- In-memory data stores (Redis): Strings, Hashes, Lists, Sets, Sorted Sets (ZSET), caching strategies (Cache-Aside, Write-Through), and pub/sub streams.
- Database optimization: `EXPLAIN ANALYZE` execution plans, index tuning, vacuuming, and connection pool management (PgBouncer).
- Networking & protocols: OSI stack, TCP/IP, TLS, HTTP/1.1 keep-alive vs HTTP/2 multiplexing vs HTTP/3 QUIC.
- Asynchronous task execution: Background task queues, workers (Celery, RQ, Redis Streams), and distributed worker management.
- Linux & Developer Tooling: Bash shell scripting, SSH, process monitoring (`htop`, `lsof`), Git branching, and Docker containerization.

> 🛡️ **Phase 3 Exit Project:**  
> Build an end-to-end multi-tenant backend platform with FastAPI: OAuth2/JWT authentication, PostgreSQL persistence with Alembic migrations, Redis caching, asynchronous background task workers, rate limiting, integration tests, and containerized Docker Compose deployment.

---

### Phase 4 — Low-Level Design (LLD) & Software Engineering
*Learn to write modular, decoupled, testable, and maintainable software that can evolve without breaking.*

#### 📺 Curated Learning Resources
- [ ] **Order 12 · [Code and Debug — Python LLD & Object-Oriented Design](https://www.youtube.com/@CodeAndDebug/playlists)**  
  *Action:* Study low-level system design patterns in Python, object modeling, UML diagramming, and interview problem breakdowns.
- [ ] **Order 13 · [ArjanCodes — Design Patterns & Software Architecture](https://www.youtube.com/@ArjanCodes/playlists)**  
  *Action:* Master SOLID principles, Gang of Four design patterns, architecture boundaries, and refactoring techniques.

#### 🧠 Concepts to Master
- SOLID Principles: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion.
- Clean architecture paradigms: Separation of concerns, DRY, KISS, and composition over inheritance.
- Creational Patterns: Factory Method, Abstract Factory, Builder, Prototype, Singleton (and its testing anti-patterns).
- Structural Patterns: Adapter, Decorator, Facade, Composite, Proxy.
- Behavioral Patterns: Strategy, Observer, Command, State, Chain of Responsibility, Template Method.
- Design artifacts: Class diagrams, sequence diagrams, state-machine diagrams, and interface abstractions.
- Enterprise patterns: Repository pattern, Service layer pattern, Unit of Work, and Domain-Driven Design (DDD) aggregates.

> 🛡️ **Phase 4 Exit Project:**  
> Implement and document clean, object-oriented solutions for four classic LLD scenarios: Parking Lot System, Notification Service, Payment Processing Engine, and an Extensible Workflow Engine. Include unit tests, class diagrams, and design trade-off justifications.

---

### Phase 5 — High-Level Design (HLD) & Distributed Systems
*Architecting, scaling, and maintaining distributed web applications, data stores, and AI inference backends under massive load.*

#### 📺 Curated Learning Resources
- [ ] **Order 14 · [Gaurav Sen — System Design Playlist](https://www.youtube.com/playlist?list=PLMCXHnjXnTnvo6alSjVkgxV-VH6EPyvoX)**  
  *Action:* Master core distributed systems concepts: Consistent Hashing, Message Queues, Sharding, Microservices, and CDNs.
- [ ] **Order 15 · [Hussein Nasser — Software Architecture](https://www.youtube.com/playlist?list=PLQnljOFTspQXNP6mQchJVP3S-3oKGEuw9)**  
  *Action:* Study monolithic vs microservice topologies, event-driven architectures, stateful vs stateless designs, and distributed trade-offs.
- [ ] **Order 16 · [Hussein Nasser — Backend Infrastructure & Performance Playlists](https://www.youtube.com/@hnasr/playlists)**  
  *Action:* Deep dive into reverse proxies (Nginx, Envoy), Layer 4 vs Layer 7 load balancing, connection draining, and caching layers.

#### 🧠 Concepts to Master
- Scalability dynamics: Horizontal vs vertical scaling, stateless services, auto-scaling, and Little's Law ($L = \lambda W$).
- Traffic routing: Layer 4 (Maglev/IPVS) vs Layer 7 (Envoy/Nginx), load balancing algorithms (Round Robin, Smooth Weighted Round Robin, Least Connections).
- Caching architecture: Cache-aside, write-through, write-behind, CDN edge caching, and cache stampede coalescing (`SingleFlight`).
- Data partitioning: Horizontal sharding, range-based partitioning, consistent hash rings with virtual nodes, and bounded load routing.
- High availability & replication: Leader-follower replication, semi-synchronous replication lag, read repair, and epoch fencing tokens.
- Distributed consensus & consistency: CAP theorem ($R + W > N$ quorums), PACELC theorem, linearizability vs causal consistency, and Raft consensus mechanics.
- Event-driven infrastructure: Apache Kafka, partitioned commit logs, consumer groups, cooperative sticky rebalancing, and Transactional Outbox pattern.
- Resilience patterns: Circuit Breakers (with atomic `HALF_OPEN`), rate limiters (token bucket, leaky bucket), timeouts, retries with exponential backoff & full jitter.
- Capacity estimation: Calculating peak QPS, bandwidth saturation, RAM caching budgets, SSD storage footprints, and cost estimation.

> 🛡️ **Phase 5 Exit Project:**  
> Produce complete, end-to-end architectural design documents for:
> 1. Video Ingestion & Global CDN Streaming (YouTube)
> 2. Real-Time Chat & Presence Fabric for 50M concurrent sockets (WhatsApp)
> 3. Geospatial Ride-Hailing Dispatch Service (Uber)
> 4. Distributed High-Concurrency Flash Sale Inventory Engine with ACID Ledger Reconciliation
> 5. High-Throughput Distributed LLM Serving Platform (vLLM & Continuous Batching)

---

### Phase 6 — Machine Learning (Applied Foundations)
*Develop the core intuition to train, evaluate, debug, and deploy predictive models using statistical machine learning.*

#### 📺 Curated Learning Resources
- [ ] **Order 17 · [StatQuest with Josh Starmer — Machine Learning Playlists](https://www.youtube.com/@statquest/playlists)**  
  *Action:* Master statistical fundamentals, decision trees, random forests, gradient boosting, and PCA with intuitive mathematical rigor.
- [ ] **Order 18 · [DataTalks.Club — Machine Learning Zoomcamp](https://www.youtube.com/playlist?list=PL3MmuxUbc_hIhxl5Ji8t4O6lPAOpHaCLR)**  
  *Action:* Complete the end-to-end practical course: data preparation, regression, classification, evaluation, Docker deployment, and cloud serving.

#### 🧠 Concepts to Master
- Statistical foundations: Probability distributions, Bayes' theorem, hypothesis testing, mean/variance, and covariance.
- Supervised learning: Linear regression, logistic regression, cost functions (MSE, Cross-Entropy), and gradient descent.
- Tree ensembles: Decision Trees, Random Forests, and Gradient Boosted Trees (XGBoost, LightGBM, CatBoost).
- Feature engineering: Imputation, standard scaling, one-hot encoding, target encoding, and feature selection.
- Model validation: Train/validation/test splits, $K$-Fold cross-validation, data leakage prevention, and class imbalance handling (SMOTE, class weighting).
- Evaluation metrics: Accuracy, Precision, Recall, F1-Score, ROC-AUC, PR-AUC, Confusion Matrix, and log loss.
- Unsupervised learning: $K$-Means clustering, hierarchical clustering, and Principal Component Analysis (PCA).
- Hyperparameter tuning: Grid Search, Random Search, and Bayesian Optimization (Optuna).

> 🛡️ **Phase 6 Exit Project:**  
> Train, evaluate, and containerize three end-to-end predictive systems:
> 1. Customer Churn Classification system with feature pipelines and ROC analysis.
> 2. Price Prediction Regression system with regularized ensembling.
> 3. E-Commerce Recommendation Engine combining collaborative filtering and matrix factorization.

---

### Phase 7 — Deep Learning & Transformers
*Understand deep learning from the ground up: implement backpropagation by hand, master PyTorch, and code a Transformer from scratch.*

#### 📺 Curated Learning Resources
- [ ] **Order 19 · [Andrej Karpathy — The spelled-out intro to neural networks and backpropagation: building micrograd](https://www.youtube.com/watch?v=VMj-3S1tku0)**  
  *Action:* Code a scalar-valued autograd engine and neural network library from scratch in pure Python.
- [ ] **Order 20 · [Andrej Karpathy — Neural Networks: Zero to Hero (Verified Playlist)](https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ)**  
  *Action:* Build `makemore` language models step-by-step: bigram models, MLP, manual backprop, WaveNet, and tokenizers.
- [ ] **Order 21 · [Andrej Karpathy — Let's build GPT: from scratch, in code, spelled out](https://www.youtube.com/watch?v=kCc8FmEb1nY)**  
  *Action:* Implement a complete decoder-only Transformer language model from scratch in PyTorch, train it on Shakespeare, and generate text.
- [ ] **Order 22 · [MIT 6.S191 — Introduction to Deep Learning (Alexander Amini)](https://www.youtube.com/@AlexanderAmini/playlists)**  
  *Action:* Complete MIT's lecture series on neural network foundations, computer vision, sequence modeling, and generative architectures.

#### 🧠 Concepts to Master
- Mathematical mechanics: Computational graphs, reverse-mode automatic differentiation, and backpropagation derivations.
- Deep learning framework: PyTorch tensors, autograd engine, custom `nn.Module`, datasets, dataloaders, and GPU device management.
- Optimization: SGD with Momentum, RMSprop, Adam, AdamW, learning rate schedules (Cosine Annealing), and gradient clipping.
- Deep architectures: Multi-Layer Perceptrons (MLP), Convolutional Neural Networks (CNN), Residual Connections (ResNet), and Normalization (LayerNorm, RMSNorm).
- Sequence models: Recurrent Neural Networks (RNN), LSTMs, and why Attention resolved the bottleneck of recurrence.
- Transformer architecture: Scaled dot-product attention, multi-head attention, queries, keys, values, feed-forward networks, and causal masking.
- Positional encodings: Learned positional embeddings, sinusoidal encodings, and modern Rotary Position Embeddings (RoPE).
- Training mechanics: Mixed-precision training (`torch.cuda.amp.autocast`), gradient accumulation, and model checkpointing.

> 🛡️ **Phase 7 Exit Project:**  
> Implement a functional autograd engine and small Transformer model from scratch in pure Python/PyTorch. Train it on a text dataset, generate coherent tokens, and thoroughly document the mathematical role of every layer and tensor operation.

---

### Phase 8 — Generative AI and LLM Engineering (Primary Specialization)
*The central pillar of your career profile: master frontier LLM architectures, production RAG systems, model evaluation, and parameter-efficient fine-tuning.*

#### 📺 Curated Learning Resources
- [ ] **Order 23 · [Andrej Karpathy — Deep Dive into LLMs like ChatGPT](https://www.youtube.com/watch?v=7xTGNNLPyMI)**  
  *Action:* Master the full lifecycle of LLMs: tokenization, base pre-training, supervised fine-tuning (SFT), RLHF, and thinking models.
- [ ] **Order 24 · [Andrej Karpathy — Build GPT from Scratch](https://www.youtube.com/watch?v=kCc8FmEb1nY)**  
  *Action:* Re-implement and experiment with Transformer attention blocks, context windows, and generation samplers.
- [ ] **Order 25 · [DataTalks.Club — LLM Zoomcamp Course Series](https://www.youtube.com/playlist?list=PL3MmuxUbc_hIoBpuc900htYF4uhEAbaT-)**  
  *Action:* Build real-world RAG applications, vector search indices, evaluation pipelines, and orchestration workflows.
- [ ] **Order 26 · [The Full Stack — LLM Bootcamp (Official Series)](https://www.youtube.com/playlist?list=PL1T8fO7ArWleyIqOy37OVXsP4hFXymdOZ)**  
  *Action:* Complete the production LLM bootcamp covering prompt engineering, RAG architecture, vector databases, and evaluation.  
  *(Official channel: [`@The_Full_Stack`](https://www.youtube.com/@The_Full_Stack/playlists))*
- [ ] **Order 27 · [DeepLearning.AI — LLM Fine-Tuning & Application Courses](https://www.youtube.com/@Deeplearningai/playlists)**  
  *Action:* Study short courses on instruction fine-tuning, LoRA/QLoRA adaptation, embeddings, and structured outputs.

#### 🧠 Step-by-Step Sub-Sequences to Master

##### A. LLM Foundations
- Tokenization: Byte-Pair Encoding (BPE), SentencePiece, token vocabularies, token compression ratios, and special tokens.
- Architecture: Pre-LN vs Post-LN, RMSNorm, SwiGLU activation functions, Rotary Position Embeddings (RoPE), and KV-Cache mechanics.
- Pretraining & Alignment: Web-scale pretraining $\rightarrow$ Supervised Fine-Tuning (SFT) $\rightarrow$ Preference Optimization (RLHF, DPO, KTO).

##### B. Production RAG & Context Engineering
- Document ingestion: Document loaders (PDF, HTML, Markdown), chunking strategies (fixed, semantic, recursive, parent-child).
- Embedding models: Dense representations, cosine similarity, distance metrics, and vector database indices (HNSW, IVFFlat).
- Hybrid search: Combining sparse lexical retrieval (BM25) with dense vector search via Reciprocal Rank Fusion (RRF).
- Retrieval optimization: Cross-encoder reranking (Cohere, BGE Reranker), query transformation (HyDE, Multi-Query, Step-Back prompting).
- Evaluation science: Measuring retrieval and generation using Ragas, DeepEval, and TruLens (Faithfulness, Answer Relevance, Context Precision, Context Recall).

##### C. Advanced LLM Engineering & Model Adaptation
- Parameter-Efficient Fine-Tuning (PEFT): Low-Rank Adaptation (LoRA), QLoRA, rank $r$, alpha scaling, and target projection layers.
- Model quantization: Post-Training Quantization (PTQ), FP16, BF16, INT8, INT4, AWQ, and GPTQ.
- Inference performance: KV-cache memory sizing, model routing, speculative decoding, and continuous batching.

> 🛡️ **Phase 8 Exit Project:**  
> Build an Enterprise RAG Platform supporting multi-format document ingestion, hybrid BM25 + dense vector retrieval, cross-encoder reranking, multi-tenant access control, user citation tracing, and automated regression evaluation. In parallel, fine-tune an open-source model using QLoRA and benchmark against the base model on a validation dataset.

---

### Phase 9 — Agentic AI Engineering (Second Major Specialization)
*Move beyond linear prompts into autonomous, cyclical, tool-using, multi-agent systems designed for reliable enterprise workflows.*

#### 📺 Curated Learning Resources
- [ ] **Order 28 · [LangChain — LangGraph Essentials (Complete Course)](https://www.youtube.com/watch?v=B_BCeWhyD5Q)**  
  *Action:* Complete the foundational course on state management, graph execution, human intervention, and checkpointing.
- [ ] **Order 29 · [LangChain — Official Agent & LangGraph Tutorials](https://www.youtube.com/@LangChain/playlists)**  
  *Action:* Study advanced multi-agent architectures, supervisor routing, hierarchical teams, streaming, and error handling.
- [ ] **Order 30 · [DeepLearning.AI — AI Agent Development Playlists](https://www.youtube.com/@Deeplearningai/playlists)**  
  *Action:* Master agent reasoning loops, tool dispatch patterns, autonomous research workflows, and agent design patterns.

#### 🧠 Concepts to Master
- Agent reasoning loops: ReAct (Reason + Act), Plan-and-Solve, Reflection, and native function/tool calling.
- Stateful graph execution (LangGraph): State schemas, state channels, node functions, conditional routing edges, and reducers.
- Tool integration: Model Context Protocol (MCP) clients, servers, schema definition, and secure external execution.
- Memory architecture: Short-term thread memory vs long-term cross-thread episodic and semantic memory stores.
- Human-in-the-Loop (HITL): Workflow interruption gates, review checkpoints, state inspection, and dynamic state editing.
- Multi-agent coordination: Supervisor-worker models, network topologies, multi-agent handoffs, and consensus protocols.
- Resilience: Durable checkpoint persistence (SQLite/PostgreSQL), idempotent tool execution, retries, and fallback handling.
- Guardrails: Permission boundaries, sandboxed execution, input sanitization, and output schema enforcement.

> 🛡️ **Phase 9 Exit Project:**  
> Build a production Multi-Tool Autonomous Agent with LangGraph: integrate database querying, external API dispatching, calendar/email integrations, persistent PostgreSQL checkpointing, failure self-healing, and a human approval gate before committing consequential transactions.

---

### Phase 10 — MLOps, LLMOps, Cloud and Infrastructure
*Take AI systems from prototype to production: containerization, high-throughput inference serving, GPU memory optimization, and cluster orchestration.*

#### 📺 Curated Learning Resources
- [ ] **Order 31 · [freeCodeCamp — Docker Full Course 2026 Edition](https://www.youtube.com/watch?v=rjjES5IsPdg)**  
  *Action:* Master Docker images, multi-stage builds, volumes, networking, Docker Compose, and production deployment.
- [ ] **Order 32 · [DataTalks.Club — MLOps & Infrastructure Course Playlists](https://www.youtube.com/@DataTalksClub/playlists)**  
  *Action:* Complete the MLOps Zoomcamp: experiment tracking (MLflow), feature engineering, model registry, and monitoring.  
  *(Direct course playlist: [`MLOps Zoomcamp`](https://www.youtube.com/playlist?list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK))*
- [ ] **Order 33 · [vLLM Project — High-Performance Inference & Serving Architecture](https://www.youtube.com/results?search_query=vLLM+inference+serving+tutorial)**  
  *Action:* Study high-throughput LLM serving, PagedAttention virtual memory block allocation, and continuous batching.  
  *(Official codebase & docs: [`github.com/vllm-project/vllm`](https://github.com/vllm-project/vllm))*
- [ ] **Order 34 · [freeCodeCamp — Kubernetes & Cloud Orchestration Playlists](https://www.youtube.com/@freecodecamp/playlists)**  
  *Action:* Master Kubernetes fundamentals: Pods, Deployments, Services, ConfigMaps, Ingress, and GPU node scheduling.
- [ ] **Order 35 · [Hussein Nasser — Infrastructure & Performance Engineering](https://www.youtube.com/@hnasr/playlists)**  
  *Action:* Study advanced production operations, connection management, reverse proxy optimization, and infrastructure bottlenecks.

#### 🧠 Concepts to Master
- Cloud & Containers: Multi-stage Docker builds for Python and CUDA, container registries, Kubernetes deployments, and GPU node affinities.
- CI/CD & Automation: GitHub Actions workflows, automated linting, test execution, image compilation, and automated deployment.
- MLOps Pipeline: MLflow experiment tracking, model registry promotion (Staging $\rightarrow$ Production), data lineage, and automated retraining.
- Model Monitoring: Production inference logging, ground-truth tracking, data drift, concept drift, and performance alerting.
- High-Performance LLM Serving (LLMOps):
  - **vLLM Engine:** Architecture, PagedAttention mechanics, virtual memory block tables, and eliminating internal memory fragmentation.
  - **Continuous Batching:** Iteration-level scheduling vs static request-level batching.
  - **GPU Memory Calculations:** Sizing model weights ($2\text{ B/param}$ in FP16, $0.5\text{ B}$ in INT4), activation memory, and KV-cache allocations ($2 \times 2 \times n_{\text{layers}} \times d_{\text{model}} \times \text{tokens}$).
  - **Distributed Inference:** Tensor Parallelism (TP) across intra-node NVLink and Pipeline Parallelism (PP) across nodes.
  - **Unified Model Gateways:** Routing, load balancing, fallback logic, and rate limiting with **LiteLLM**.

> 🛡️ **Phase 10 Exit Project:**  
> Deploy an open-source LLM (e.g., Llama-3 or Mistral) on a cloud GPU instance with vLLM, fronted by LiteLLM for routing, containerized with Docker, monitored with Prometheus (measuring TTFT, TPOT, tokens/second, and GPU utilization), and load-tested with Locust.

---

### Phase 11 — AI Security and Red Teaming
*Defend production AI systems against adversarial prompts, data extraction, and tool exploitation.*

#### 📺 Curated Learning Resources
- [ ] **Order 36 · [Microsoft — AI Red Teaming 101 (Complete 10-Episode Course)](https://www.youtube.com/watch?v=DwFVhFdD2fs)**  
  *Action:* Complete all 10 episodes on AI threat modeling, direct/indirect prompt injection, jailbreaking, and red-teaming methodologies.
- [ ] **Order 37 · [Microsoft — Automating AI Red Teaming with PyRIT](https://www.youtube.com/watch?v=cEHTxmpAgjA)**  
  *Action:* Study practical automated adversarial testing, scoring, and security scanning using the Python Risk Identification Tool (PyRIT).
- [ ] **Order 38 · [OWASP Global — Generative AI Security Videos](https://www.youtube.com/@OWASPGLOBAL/playlists)**  
  *Action:* Study the OWASP Top 10 for Large Language Applications, systemic attack surfaces, and defensive mitigations.
- [ ] **Order 39 · [Hussein Nasser — Web & API Security Playlist](https://www.youtube.com/@hnasr/playlists)**  
  *Action:* Master core web and API security: CORS, CSRF, SQL injection, timing attacks, authentication bypasses, and secure headers.

#### 🧠 Concepts to Master
- Attack surfaces: Direct prompt injections, indirect injections (via PDFs/web scraping), universal adversarial suffixes, and jailbreaks.
- Data security: Training data extraction, PII exfiltration, prompt leakage, and membership inference attacks.
- Agent vulnerabilities: Insecure tool execution, excessive permissions, unconstrained SQL/bash dispatching, and confused deputy problems.
- Automated security testing: Configuring automated adversarial multi-turn testing with Microsoft PyRIT.
- Defensive architectures: Input guardrails (Llama Guard), output schema validation, dual-LLM security judges, and fail-closed permission gates.

> 🛡️ **Phase 11 Exit Project:**  
> Conduct an adversarial red-teaming audit on your Phase 8 RAG engine and Phase 9 Agent: document 5 distinct vulnerability vectors (jailbreak, indirect injection, tool misuse), implement defensive mitigations, and create automated regression tests in PyRIT to verify prevention.

---

## 💼 The 5 Mandatory Standout Portfolio Projects

Courses alone will not make you stand out. The difference between an average candidate and a top engineering candidate is the ability to demonstrate **end-to-end production systems**. Build these 5 systems to complete your curriculum:

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                FIVE STANDOUT PORTFOLIO PROJECTS                                  │
├───────────────────────────────────┬──────────────────────────────────────────────────────────────┤
│ 1. Enterprise RAG Platform        │ Hybrid BM25/Dense + Reranking + Citations + DeepEval         │
│ 2. Autonomous Multi-Agent System  │ LangGraph + MCP + HITL Approval Gate + Persistent Checkpoint │
│ 3. LLM Evaluation Platform        │ Model Benchmarking + Prompt Versioning + Regression Tests    │
│ 4. Self-Hosted LLM Infrastructure │ vLLM + PagedAttention + LiteLLM + Prometheus + GPU Sizing    │
│ 5. Production AI SaaS Platform    │ FastAPI + Next.js + Stripe + Redis + Background Workers      │
└───────────────────────────────────┴──────────────────────────────────────────────────────────────┘
```

### 1. Enterprise RAG Platform (LLM Engineering)
- **Tech Stack:** Python 3.11+, FastAPI, PostgreSQL (pgvector) / Qdrant, BGE Reranker, Ragas / DeepEval.
- **Key Features:** Multi-format document parsing (PDF, DOCX, Markdown), hybrid retrieval fusing BM25 lexical with dense vector search (Reciprocal Rank Fusion), cross-encoder reranking, strict tenant access control, exact document chunk citations, and automated evaluation metrics.

### 2. Enterprise Multi-Agent Platform (Agentic AI)
- **Tech Stack:** LangGraph, Model Context Protocol (MCP), SQLite/PostgreSQL checkpointing, Pydantic v2.
- **Key Features:** Cyclical state graphs, tool execution with automated retry recovery, multi-agent supervisor coordination, and human-in-the-loop interruption gates for sensitive side-effects (database updates, external emails).

### 3. LLM Evaluation & Tracing Platform (AI Quality Engineering)
- **Tech Stack:** Python, OpenTelemetry, DeepEval, Arize Phoenix / Langfuse, FastAPI.
- **Key Features:** Systematic model comparison (Llama vs Mistral vs OpenAI), prompt versioning, automated regression testing on golden datasets, latency/token cost tracking, and hallucination scoring.

### 4. Self-Hosted High-Throughput LLM Infrastructure (LLMOps)
- **Tech Stack:** vLLM, LiteLLM Gateway, Hugging Face, Prometheus, Grafana, Locust.
- **Key Features:** Hosting an open-source LLM with continuous batching and PagedAttention, KV-cache tuning, model routing, token-per-second latency benchmarking, and automated load testing measuring TTFT and TPOT.

### 5. Production AI SaaS Application (Full-Stack Engineering)
- **Tech Stack:** FastAPI, Next.js / React, PostgreSQL 16, Redis 7, Celery / RQ, Docker Compose, Stripe.
- **Key Features:** End-to-end product with user authentication, real-time token streaming over WebSockets, asynchronous background task pipelines, usage-based billing, structured observability, and production cloud deployment.

> 💡 **Portfolio Requirement:** For every project, maintain a dedicated GitHub repository featuring a clear architecture diagram, thorough README, comprehensive test suite, Docker containerization, and documented engineering design trade-offs.

---

## 🎯 Interview Preparation — Run Alongside the Curriculum

Do not leave interview preparation until the end of the roadmap. Allocate 5 hours every week to deliberate interview practice:

| Interview Round | Core Preparation Focus | Recommended Verified Resources |
|:---|:---|:---|
| **Python & Coding** | Internals, concurrency, AsyncIO, memory, profiling | [Corey Schafer Playlists](https://www.youtube.com/@coreyms/playlists) · [ArjanCodes](https://www.youtube.com/@ArjanCodes/playlists) |
| **Data Structures & Algorithms** | 150–250 problems, timed whiteboard practice | [NeetCode Channel](https://www.youtube.com/@NeetCode/playlists) |
| **SQL & Database Internals** | Complex queries, indexing, isolation, transactions | [Hussein Nasser Database Series](https://www.youtube.com/playlist?list=PLQnljOFTspQXjD0HOzN7P2tgzu7scWpl2) |
| **Backend & System Design** | API design, authentication, databases, concurrency | [Corey Schafer FastAPI](https://www.youtube.com/watch?v=iukOehU5aF4) · [Hussein Nasser](https://www.youtube.com/@hnasr/playlists) |
| **Low-Level Design (LLD)** | OOP, SOLID principles, machine-coding problems | [Code and Debug LLD](https://www.youtube.com/@CodeAndDebug/playlists) |
| **High-Level Design (HLD)** | Distributed systems, scalability, failure scenarios | [Gaurav Sen System Design](https://www.youtube.com/playlist?list=PLMCXHnjXnTnvo6alSjVkgxV-VH6EPyvoX) · [Gaurav Sen Channel](https://www.youtube.com/@gkcs/playlists) |
| **AI & LLM Architecture** | RAG mechanics, agents, fine-tuning, evaluation | [Karpathy Deep Dive](https://www.youtube.com/watch?v=7xTGNNLPyMI) · [The Full Stack](https://www.youtube.com/@The_Full_Stack/playlists) |
| **LLMOps & Infrastructure** | Inference optimization, GPU memory math, serving | [vLLM Project Tutorials](https://www.youtube.com/results?search_query=vLLM+inference+serving+tutorial) |
| **Behavioral & Leadership** | Project deep dives, technical trade-offs, ownership | [Exponent Interview Playlists](https://www.youtube.com/@tryexponent/playlists) |

---

## 🚀 Final Strategic Advice

Your target professional identity is:
```
╔═══════════════════════════════════════════════════════════════════════════════════════╗
║                      APPLIED AI / LLM SYSTEMS ENGINEER                                ║
╠═══════════════════════════════════════════════════════════════════════════════════════╣
║ An engineer who can build intelligent applications, engineer reliable AI agent        ║
║ workflows, understand underlying transformer models, optimize high-throughput GPU     ║
║ inference, and operate production-grade software infrastructure.                      ║
╚═══════════════════════════════════════════════════════════════════════════════════════╝
```

1. **Prioritize engineering depth over breadth:** Building five exceptional, robust systems and defending their trade-offs in depth will unlock more high-paying offers than watching 100 tutorials.
2. **Master the software foundation:** High-paying AI engineering roles are software engineering roles first. Teams hire engineers who can write clean, asynchronous, tested, containerized code.
3. **Understand model internals:** Knowing how attention, KV caching, tokenization, and quantization work allows you to optimize latency and cost in ways API wrappers cannot.
4. **Complete the roadmap sequentially:** Follow the phases step-by-step, check off each module, build the exit projects, and maintain consistent deliberate practice.
