# Final Learning Roadmap: roadmap.sh + our courses

One ordered path. **roadmap.sh is the tracker** for every topic it covers (tick nodes off there and use its AI tutor
for deep dives). **Our modules cover everything roadmap.sh does not**: maths depth, GPU programming, distributed
training, database and system internals, LLM-evaluation depth and CPython internals. Nothing is left out:
all 175 modules sit in exactly one phase below.

## How to work each phase

1. Open the phase's roadmap.sh roadmaps and work the **must-know** nodes (skip the optional ones until later).
2. Do the phase's **our-material modules** in the listed order: watch the main lecture (in-app *Watch Video*),
   read the lesson and the *Read More* pages, run the playground/problem bank, then pass the quiz.
3. For anything still fuzzy, ask your AI to explain it with a small runnable example, give you three exercises,
   then quiz you. Do not move on until you can solve them without help.
4. Pass the course gate (`make check-gates`) for each course before leaving its last phase.

Pace: one module every 1 to 2 days plus the roadmap.sh nodes. The whole path is long (many months part-time);
Phase 9 and 10 can be deferred until you need them.

**Honest note:** videos and reading pages were chosen for relevance and checked to name each concept; nobody has
watched every minute. Swap any weak resource in the course's `CURATED_VIDEO_LECTURES.md` or `RECOMMENDED_READING.md`.

## Biggest holes in our courses that roadmap.sh fills

- **Classical machine learning:** decision trees, random forests, gradient boosting, unsupervised and semi-supervised learning, ROC/AUC, CNN/RNN/GAN applications (Phase 6).
- **LLM ecosystem and tooling:** MCP servers/clients/hosts, Hugging Face Hub and inference SDKs, Ollama/LM Studio local models, OpenRouter, agent SDKs, DeepEval, Helicone (Phase 7).
- **Prompting techniques:** chain-of-thought, tree-of-thoughts, prompt ensembling, calibration (Phase 7).
- **MLOps tooling:** Airflow, MLflow, DVC, Kubeflow, Jenkins, Ansible, data lakes/warehouses (Phase 8).
- **Cloud design patterns:** strangler fig, publisher/subscriber, competing consumers, valet key and the other Azure patterns (Phase 4).
- **Auth and protocols:** OpenID, SAML, SOAP, TLS, twelve-factor apps (Phase 4).
- **Ops breadth:** most of Git, Linux, shell, Kubernetes, Terraform, AWS and DevSecOps (Phases 0 and 5).
- **Vision, speech and diffusion inference** (Inference Engineering roadmap, Phase 8).

## Phase 0 - Tools

**Goal:** Use git, a Linux shell and a modern Python toolchain without friction.

**roadmap.sh (in order):** [git-github](https://roadmap.sh/git-github) → [linux](https://roadmap.sh/linux)  
*Optional:* [shell-bash](https://roadmap.sh/shell-bash)

**Our modules (1):** uv, ruff and the project workflow are in our Module 0.

| Course | # | Module | Main lecture | More videos |
|---|---|--------|--------------|-------------|
| 01 | 0 | Environment, uv, ruff & Modern Tooling | [Python Tutorial: UV - A Faster, All-in-One Package Manager t](https://www.youtube.com/watch?v=AMdG7IjgSPM) | 1 |

**On roadmap.sh but not in our courses (learn these on roadmap.sh):**

- [git-github](https://roadmap.sh/git-github) (40): campus program, cherry picking commits, cloning repositories, collaboration on github, collaborators / members, contribution guidelines, deploying static websites, detached head, fast forward vs non ff, forking vs cloning, git bisect, git commit / amend, git lfs, git rebase, git reflog, git remotes, git revert, git stash basics, git vs other vcs, git worktree, github classroom, github codespaces, github copilot, github discussions, github education, github marketplace, github sponsors, github wikis, kanban boards, labelling issues / prs, managing remotes, marketplace actions, pr from a fork, pr guidelines, rebase, scheduled worfklows, secrets and env vars, student developer pack, teams within organization, unstaged changes
- [linux](https://roadmap.sh/linux) (20): background / foreground processes, creating / deleting files / dirs, dhcp, ethernet / arprarp, icmp, inodes, install / remove / upgrade packages, netfilter, netstat, package repositories, process priorities, service management systemd, shell and other basics, starting / stopping services, stdout / stdin / stderr, subnetting, tcpip stack, traceroute, unexpand, vim
- [shell-bash](https://roadmap.sh/shell-bash) (33): bzip2 xz, chgrp, chmod, cli vs gui, disown, emacs, environment vs shell vars, extended regex, fg bg, gzip gunzip, ifconfig ip, inputoutput, iostat vmstat, ksh, navigate between dirs, netstat ss, nohup, popular shells, printf formatting, rsync, rwx, scp, shellcheck, stdin stdout stderr, systemd timers, tab completion, tcsh, top htop, variables best practices, vim, yum, zip unzip, zsh

## Phase 1 - Python

**Goal:** Write correct, tested, typed Python.

**roadmap.sh (in order):** [python](https://roadmap.sh/python)  
*Optional:* [python-data-analysis](https://roadmap.sh/python-data-analysis)

**Our modules (9):** Testing with pytest/Hypothesis, logging, serialization and strict typing go deeper in our modules.

| Course | # | Module | Main lecture | More videos |
|---|---|--------|--------------|-------------|
| 01 | 1 | Python Fundamentals, Types & Control Flow | [Python Tutorial for Beginners 3: Integers and Floats - Worki](https://www.youtube.com/watch?v=khKv-8q7YmY) | 2 |
| 01 | 2 | Functions, Scopes, Closures & LEGB Rule | [Python Tutorial: Variable Scope - Understanding the LEGB rul](https://www.youtube.com/watch?v=QVdf0LgmICw) | 2 |
| 01 | 3 | Data Structures, Collections & Hash Table Internals | [Python dataclasses will save you HOURS, also featuring attrs](https://www.youtube.com/watch?v=vBH6GRJ1REM) | 2 |
| 01 | 4 | Deep OOP, Inheritance, MRO & Dunder Protocols | [Python OOP Tutorial 6: Property Decorators - Getters, Setter](https://www.youtube.com/watch?v=jCzT9XFZ5bw) | 3 |
| 01 | 5 | Decorators, Generators & Context Managers | [Python Tutorial: Decorators - Dynamically Alter The Function](https://www.youtube.com/watch?v=FsAPt_9Bf3U) | 2 |
| 01 | 6 | Enterprise Error Handling & Resilient Logging | [Python Tutorial: Logging Basics - Logging to Files, Setting ](https://www.youtube.com/watch?v=-ARI4Cz-awo) | 1 |
| 01 | 7 | Modern File I/O, Data Formats & Serialization | [Python Tutorial: Working with JSON Data using the json Modul](https://www.youtube.com/watch?v=9N6a-VLBa2I) | 1 |
| 01 | 8 | Modern Testing & QA (Pytest & Hypothesis) | [How to Test Asynchronous Code in Python](https://www.youtube.com/watch?v=n1nqgMtWRwg) | 1 |
| 01 | 23 | Strict Typing, Mypy & Modern Packaging | [The REAL Reason You Should Use Type Hints in Python](https://www.youtube.com/watch?v=0oBLMwHdZ2Y) | 1 |

**On roadmap.sh but not in our courses (learn these on roadmap.sh):**

- [python](https://roadmap.sh/python) (11): asynchrony, doctest, pdm, pipenv, plotly dash, poetry, pyproject.toml, sanic, tornado, unittest / PyUnit, yapf
- [python-data-analysis](https://roadmap.sh/python-data-analysis) (22): airflow, altair, boxplot, customizing plots, dask, dropping vs imputing, exploratory data analysis, geopandas, google colab, iqr, isnull isna, jupyterlab, plot categories, power bi / tableau, pyspark, regression plots, saving figures, scatterplot, scrapy, seaborn, streamlit, subplots and figures

## Phase 2 - Computer science core

**Goal:** Reason about complexity and pick the right data structure and algorithm.

**roadmap.sh (in order):** [computer-science](https://roadmap.sh/computer-science) → [datastructures-and-algorithms](https://roadmap.sh/datastructures-and-algorithms)  
*Optional:* [leetcode](https://roadmap.sh/leetcode)

**Our modules (17):** Network flow, string matching, skip lists, Bloom filters and segment trees are only in our material.

| Course | # | Module | Main lecture | More videos |
|---|---|--------|--------------|-------------|
| 02 | 1 | Complexity Analysis & Memory Layout | [1.8.1 Asymptotic Notations Big Oh - Omega - Theta #1](https://www.youtube.com/watch?v=A03oI0znAoc) | 2 |
| 02 | 2 | Arrays, Dynamic Arrays & Two-Pointer Patterns | [Design a Dynamic Array (Resizable Array)](https://www.youtube.com/watch?v=xT70mHdAM74) | 1 |
| 02 | 3 | Linked Lists & Pointer Manipulation | [Design a Singly Linked List](https://www.youtube.com/watch?v=xqAvQsy5KkI) | - |
| 02 | 4 | Stacks, Queues & Monotonic Structures | [Next Greater Element I - Leetcode 496 - Python](https://www.youtube.com/watch?v=68a1Dc_qVq4) | 3 |
| 02 | 5 | Hash Tables & Collision Resolution | [Hashing Technique - Simplified](https://www.youtube.com/watch?v=mFY0J5W8Udk) | 2 |
| 02 | 6 | Trees, BSTs & Self-Balancing AVL/Red-Black | [10.1 AVL Tree - Insertion and Rotations](https://www.youtube.com/watch?v=jDM6_TnYIqE) | 3 |
| 02 | 7 | Heaps, Priority Queues & Top-K Patterns | [2.6.3 Heap - Heap Sort - Heapify - Priority Queues](https://www.youtube.com/watch?v=HqPJF2L5h9U) | 1 |
| 02 | 8 | Graph Traversals, BFS/DFS & Topological Sort | [5.1 Graph Traversals - BFS & DFS -Breadth First Search and D](https://www.youtube.com/watch?v=pcKY4hjDrxk) | 1 |
| 02 | 9 | Shortest Paths (Dijkstra, Bellman-Ford) & MST | [3.6 Dijkstra Algorithm - Single Source Shortest Path - Greed](https://www.youtube.com/watch?v=XB4MIexjvY0) | 2 |
| 02 | 10 | 1D Dynamic Programming & Sequence Patterns | [Dynamic Programming 1D - Full Course - Python](https://www.youtube.com/watch?v=_i4Yxeh5ceQ) | - |
| 02 | 11 | 2D Dynamic Programming (Knapsack & Grid Paths) | [4.5 0/1 Knapsack - Two Methods - Dynamic Programming](https://www.youtube.com/watch?v=nLmhmB6NzcM) | 1 |
| 02 | 12 | Greedy Algorithms & Interval Scheduling | [3.2 Job Sequencing with Deadlines - Greedy Method](https://www.youtube.com/watch?v=zPtI8q9gvX8) | 1 |
| 02 | 13 | Backtracking & Constraint Satisfaction | [6.1 N Queens Problem using Backtracking](https://www.youtube.com/watch?v=xFv_Hl4B83A) | 1 |
| 02 | 14 | Advanced Structures: Trie, Union-Find & Segment Tree | [Design Add and Search Words Data Structure - Leetcode 211 - ](https://www.youtube.com/watch?v=BTf05gs_8iU) | 2 |
| 02 | 15 | Systems-Level Structures: SkipLists, Bloom Filters & LRU | [Skip List: Randomized Data Structure](https://www.youtube.com/watch?v=zO5NJ8xiwTM) | 2 |
| 02 | 16 | String Algorithms & Substring Pattern Matching | [9.1 Knuth-Morris-Pratt KMP String Matching Algorithm](https://www.youtube.com/watch?v=V5-7GzOfADQ) | 1 |
| 02 | 17 | Network Flow & Bipartite Matching | [Ford-Fulkerson in 5 minutes](https://www.youtube.com/watch?v=Tl90tNtKvxs) | 1 |

**On roadmap.sh but not in our courses (learn these on roadmap.sh):**

- [computer-science](https://roadmap.sh/computer-science) (15): common uml diagrams, database federation, endianess, finding hamiltonian paths, k ary / m ary tree, lock / mutex / semaphore, maze solving problem, mfu cache, public key cryptography, small omega, statemachine diagrams, tcpip model, the knights tour problem, travelling salesman problem, usecase diagrams
- [datastructures-and-algorithms](https://roadmap.sh/datastructures-and-algorithms) (3): bb trees, bellman ford algoritm, edabit
- [leetcode](https://roadmap.sh/leetcode) (4): min interval to include query, powx n, reconstruct itinerary, spiral matrix

## Phase 3 - Data

**Goal:** Store, query and index data correctly, in relational, document, key-value and analytical systems.

**roadmap.sh (in order):** [sql](https://roadmap.sh/sql) → [postgresql-dba](https://roadmap.sh/postgresql-dba) → [redis](https://roadmap.sh/redis) → [mongodb](https://roadmap.sh/mongodb) → [data-engineer](https://roadmap.sh/data-engineer)  
*Optional:* [elasticsearch](https://roadmap.sh/elasticsearch)

**Our modules (14):** Columnar/OLAP, BM25 relevance and vector databases (pgvector, HNSW) are mostly in our modules.

| Course | # | Module | Main lecture | More videos |
|---|---|--------|--------------|-------------|
| 01 | 24 | High-Performance Data Engineering (Polars & DuckDB) | [Polars Tutorial: Blazingly Fast Exploratory Data Analysis in](https://www.youtube.com/watch?v=ps_KKM6upeQ) | 1 |
| 03 | 1 | Storage Theory, ACID & Relational Foundation | [Relational Database ACID Transactions (Explained by Example)](https://www.youtube.com/watch?v=pomxJOFVcQs) | 2 |
| 03 | 2 | Advanced SQL: Window Functions, CTEs & Joins | [SQL Window Functions Basics (Visually Explained) | PARTITION](https://www.youtube.com/watch?v=o666k19mZwE) | 2 |
| 03 | 3 | Embedded Databases: SQLite Architecture & WAL | [Redo, Undo and WAL logs | The Backend Engineering Show](https://www.youtube.com/watch?v=uHvR7nOu5m4) | 1 |
| 03 | 4 | PostgreSQL Core Architecture & Advanced Types | [PostgreSQL Internal Architecture Explained](https://www.youtube.com/watch?v=Q56kljmIN14) | 1 |
| 03 | 5 | PostgreSQL MVCC, Indexing & EXPLAIN ANALYZE | [Database Indexing Explained (with PostgreSQL)](https://www.youtube.com/watch?v=-qNSXK7s7_w) | 2 |
| 03 | 10 | MongoDB Document Modeling & BSON Internals | [MongoDB Internal Architecture](https://www.youtube.com/watch?v=ONzdr4SmOng) | 1 |
| 03 | 11 | MongoDB Aggregation Pipeline, Replication & Sharding | [MongoDB Sharding and Replication 101](https://www.youtube.com/watch?v=1sMZ455i1PU) | 1 |
| 03 | 12 | Redis In-Memory Architecture & Persistence | [Redis In-Memory Database Crash Course](https://www.youtube.com/watch?v=V7FPk4J10KI) | - |
| 03 | 13 | Redis Sentinel, Clustering & Lua Scripting | [Replication and Clustering in Redis](https://www.youtube.com/watch?v=p8mK8GBCARE) | 1 |
| 03 | 17 | Columnar OLAP: DuckDB, ClickHouse & Parquet | [Column vs Row Oriented Databases Explained](https://www.youtube.com/watch?v=Vw1fCeD06YI) | 4 |
| 03 | 18 | Analytics Engineering: Star Schemas & dbt Pipelines | [What is STAR schema | Star vs Snowflake Schema | Fact vs Dim](https://www.youtube.com/watch?v=hQvCOBv_-LE) | 1 |
| 03 | 19 | Search Engines: Apache Lucene & BM25 Relevance | [Inverted Index - The Data Structure Behind Search Engines](https://www.youtube.com/watch?v=iHHqnyThrqE) | 2 |
| 03 | 20 | AI Vector Databases: pgvector, Qdrant & HNSW | [What is a Vector Database? Powering Semantic Search & AI App](https://www.youtube.com/watch?v=gl1r1XV0SLw) | 3 |

**On roadmap.sh but not in our courses (learn these on roadmap.sh):**

- [sql](https://roadmap.sh/sql) (6): data manipulation language dml, dateadd, datepart, db security best practices, pivot / unpivot operations, rdbms benefits and limitations
- [postgresql-dba](https://roadmap.sh/postgresql-dba) (36): ansible, barman, check_pgactivity, depesz, ebpf, explaindalibocom, fortables, gdb, get involved in development, htap, indexes and their usecases, iotop, keepalived, mailing lists, patroni alternatives, pev2, pg_dumpall, pg_hbaconf, pg_probackup, pgbadger, pgbouncer alternatives, pgcenter, pgcluu, pgq, postgresql anonymizer, practical patterns / antipatterns, puppet, rdbms benefits and limitations, selinux, simple stateful setup, sp gist, strace, temboard, using pg_ctlcluster, using systemd, zabbix
- [redis](https://roadmap.sh/redis) (22): active active geo distribution, geoadd, geosearch, hdel, hexists, hgetall, lmove, lrange, rdb vs aof tradeoffs, redis vs sqlnosql dbs, redisbloom, rediscommander, redisconf, redisinsight, redisjson, redistimeseries, sdiff, setting and getting keys, smembers, ssltls encryption, sunion, zcount
- [mongodb](https://roadmap.sh/mongodb) (12): atlas search indexes, bulkwrite and relevant, elemmatch, int32int, kerberos authentication, ldap proxy auth, mongodb terminology, mongodump, mongorestore, queryable encryption, replicasets, x509 certificate auth
- [data-engineer](https://roadmap.sh/data-engineer) (48): amazon ec2 / compute, amazon rds database, amazon redshift, apache airflow, apache hadoop yarn, argocd, aurora db, aws cdk, aws eks, aws sns, azure blob storage, azure sql database, azure virtual machines, census, choosing the right technologies, circle ci, cosmosdb, couchdb, data factory etl, data mart, data warehousing architectures, databricks delta lake, ecpa, environmental management, eu ai act, gitlab ci, glue etl, google bigquery, google cloud gke, google deployment / mgr, hightouch, infrastructure as code / iac, looker, luigi, microsoft power bi, neptune, new relic, nosql databsases, onehouse, opentofu, prefect, reusability, reverse etl usecases, serverless options, streamlit, tableu, terraform, yarn
- [elasticsearch](https://roadmap.sh/elasticsearch) (6): elasticsearch usecases, fielddata, kibana console, kql, master elegible nodes, rollover policies

## Phase 4 - Backend and system design

**Goal:** Build real services, then design systems that scale and survive failure.

**roadmap.sh (in order):** [backend-beginner](https://roadmap.sh/backend-beginner) → [backend](https://roadmap.sh/backend) → [api-design](https://roadmap.sh/api-design) → [software-design-architecture](https://roadmap.sh/software-design-architecture) → [system-design](https://roadmap.sh/system-design)  
*Optional:* [software-architect](https://roadmap.sh/software-architect)

**Our modules (32):** Concurrency/asyncio, FastAPI internals, consistent hashing, Raft, vector clocks, sagas and every case study (TinyURL to payment gateway) are only in our material.

| Course | # | Module | Main lecture | More videos |
|---|---|--------|--------------|-------------|
| 01 | 9 | Concurrency (Threading, Multiprocessing & GIL) | [Python Multiprocessing Tutorial: Run Code in Parallel Using ](https://www.youtube.com/watch?v=fKl2JW_qrso) | 1 |
| 01 | 10 | Concurrency (Modern Asyncio & TaskGroups) | [Next-Level Concurrent Programming In Python With Asyncio](https://www.youtube.com/watch?v=GpqAQxH1Afc) | 1 |
| 01 | 11 | Networking, Raw Sockets & HTTP Protocols | [Python Socket Programming Tutorial 7 - TCP/IP Client and Ser](https://www.youtube.com/watch?v=BlQbUV_W954) | 1 |
| 01 | 13 | High-Performance Backend with FastAPI & ASGI | [How to Use FastAPI: A Detailed Python Tutorial](https://www.youtube.com/watch?v=SORiTsvnU28) | 1 |
| 01 | 14 | Robust Data Modeling with Pydantic V2 | [Why Python Needs Pydantic for Real Applications](https://www.youtube.com/watch?v=502XOB0u8OY) | - |
| 01 | 15 | Database Architecture with SQLAlchemy 2.0 & Alembic | [SQLAlchemy: The BEST SQL Database Library in Python](https://www.youtube.com/watch?v=aAy-B6KPld8) | 1 |
| 01 | 16 | Enterprise API Security (JWT & RBAC) | [API Authentication: JWT, OAuth2, and More](https://www.youtube.com/watch?v=xJA8tP74KD0) | 1 |
| 01 | 17 | Advanced FastAPI (WebSockets & Dependency Injection) | [Real Time Chat Room Made Easy! | FastAPI Tutorial](https://www.youtube.com/watch?v=ADVsjLHevtY) | - |
| 01 | 18 | Task Queues & Streaming with Celery and Redis | [Professional Task Queues in Python with Celery, RabbitMQ & R](https://www.youtube.com/watch?v=0gtdUkEzzn4) | - |
| 04 | 0 | System Design Fundamentals & Interview Playbook | [System Design Interview: A Step-By-Step Guide](https://www.youtube.com/watch?v=i7twT3x5yv8) | - |
| 04 | 1 | Physics of Scalability & Latency Hierarchy | [Latency Numbers Programmer Should Know: Crash Course System ](https://www.youtube.com/watch?v=FqR5vESuKe0) | 1 |
| 04 | 2 | Network Protocols: HTTP/2, gRPC & WebSockets | [WebSockets Crash Course - Handshake, Use-cases, Pros & Cons ](https://www.youtube.com/watch?v=2Nt-ZrNP22A) | 3 |
| 04 | 3 | Edge Infrastructure, CDNs & API Gateways | [Proxy vs Reverse Proxy Server Explained](https://www.youtube.com/watch?v=SqqrOspasag) | 3 |
| 04 | 4 | Load Balancing Algorithms & Health Probes | [What is a LOAD BALANCER really about?](https://www.youtube.com/watch?v=LQuuoHTyYz8) | 2 |
| 04 | 5 | SOLID Principles & Clean Architecture | [Uncle Bob’s SOLID Principles Made Easy 🍀 - In Python!](https://www.youtube.com/watch?v=pTB30aXS77U) | 1 |
| 04 | 6 | GoF Design Patterns in Scalable Backends | [Why Use Design Patterns When Python Has Functions?](https://www.youtube.com/watch?v=vzTrLpxPF54) | - |
| 04 | 7 | Low-Level Design: Elevator LOOK Scheduling | [Low-Level Design Interview: Design an Elevator w/ a Ex-Meta ](https://www.youtube.com/watch?v=fODT0ldeBiU) | - |
| 04 | 8 | Low-Level Design: Rate Limiting & Debt Simplification | [Rate Limiter System Design: Token Bucket, Leaky Bucket, Scal](https://www.youtube.com/watch?v=YXkOdWBwqaA) | 2 |
| 04 | 9 | Consistent Hashing & Distributed Partitioning | [Consistent Hashing | Algorithms You Should Know #1](https://www.youtube.com/watch?v=UF9Iqmg94tk) | 1 |
| 04 | 10 | Unique Distributed ID Generation (Twitter Snowflake) | [Generating Unique IDs at Scale: Inside Twitter’s Snowflake S](https://www.youtube.com/watch?v=SnyFRsPtoy4) | - |
| 04 | 11 | Distributed Caching & Cache Stampede Prevention | [Caching Pitfalls Every Developer Should Know](https://www.youtube.com/watch?v=wh98s0XhMmQ) | 1 |
| 04 | 12 | Probabilistic Data Structures in Large-Scale Systems | [Bloom Filters | Algorithms You Should Know #2 | Real-world E](https://www.youtube.com/watch?v=V3pzxngeLqw) | 3 |
| 04 | 13 | Distributed Messaging & Commit Logs (Kafka vs RabbitMQ) | [Kafka vs. RabbitMQ vs. Messaging Middleware vs. Pulsar](https://www.youtube.com/watch?v=x4k1XEjNzYQ) | 3 |
| 04 | 14 | System Design Case Study: Distributed URL Shortener (TinyURL) | [How Does a URL Shortener Work?](https://www.youtube.com/watch?v=HHUi8F_qAXM) | 1 |
| 04 | 15 | System Design Case Study: Real-Time Chat & Presence (Discord) | [FAANG System Design Interview: Design A Chat System (WhatsAp](https://www.youtube.com/watch?v=okrR1KXNLtA) | - |
| 04 | 16 | System Design Case Study: Newsfeed & Recommendation (Twitter) | [System Design: Design YouTube](https://www.youtube.com/watch?v=jWRW2xGMqSw) | 3 |
| 04 | 17 | System Design Case Study: Geospatial Ride-Sharing (Uber/Lyft) | [FAANG System Design Interview: Design A Location Based Servi](https://www.youtube.com/watch?v=M4lR_Va97cQ) | 2 |
| 04 | 18 | System Design Case Study: Video Streaming (YouTube/Netflix) | [What Is A CDN? How Does It Work?](https://www.youtube.com/watch?v=RI9np1LWzqw) | 1 |
| 04 | 19 | System Design Case Study: Distributed Web Crawler (Google) | [Design a Web Crawler: FAANG Interview Question](https://www.youtube.com/watch?v=6u25GckPhLU) | - |
| 04 | 20 | System Design Case Study: Flash Sale & Inventory Reservation | [Flash Sale System: System Design Interview (Stripe & Amazon ](https://www.youtube.com/watch?v=U2Acfwcah80) | - |
| 04 | 23 | Distributed Transactions: Sagas & Transactional Outbox | [Saga Pattern | Distributed Transactions | Microservices](https://www.youtube.com/watch?v=d2z78guUR4g) | 1 |
| 04 | 24 | Distributed Consensus: Raft Protocol & Vector Clocks | [Distributed Systems 6.2: Raft](https://www.youtube.com/watch?v=uXEYuDwm7e4) | 2 |

**On roadmap.sh but not in our courses (learn these on roadmap.sh):**

- [backend-beginner](https://roadmap.sh/backend-beginner) (1): repo hosting services
- [backend](https://roadmap.sh/backend) (21): ai assisted coding, antigravity, aws neptune, copilot, couchdb, firebase, gitlab, influx db, loadshifting, lxc, ms iis, openid, php, repo hosting services, rethinkdb, saml, soap, solr, ssltls, timescaledb, twelve factor apps
- [api-design](https://roadmap.sh/api-design) (15): bff pattern, building json / restful apis, ccpa, content negotiation, different api styles, hateoas, oidc, rabbit mq, readmecom, rebac, rfc 7807 / problem details, rfc 7807 / problem details for apis, soap apis, stoplight, webhooks vs polling
- [software-design-architecture](https://roadmap.sh/software-design-architecture) (14): blackboard pattern, command query separation, coupling and cohesion, encapsulate what varies, hollywood principle, keep it simple and refactor often, law of demeter, meaningful names over comments, microkernel, minimize cyclomatic complexity, organize code by actor it belongs to, posa patterns, tell dont ask, yagni
- [system-design](https://roadmap.sh/system-design) (23): ambassador, async request reply, asynchronism, busy frontend, chatty io, competing consumers, compute resource consolidation, deployment stamps, extraneous fetching, federated identity, federation, geodes, improper instantiation, lb vs reverse proxy, noisy neighbor, publishersubscriber, pull cdns, push cdns, scheduler agent supervisor, scheduling agent supervisor, static content hosting, strangler fig, valet key
- [software-architect](https://roadmap.sh/software-architect) (34): atlassian tools, babok, bpm bpel, consult / coach, cqrs eventual consistency, datawarehouse principles, emc dms, esb soap, etl datawarehouses, hadoop spark mapreduce, iaf, ibm bpm, important skills to learn, itil, java / kotlin / scala / swift, javascript / typescript, kanban, microfrontends, mvc mvp mvvm, net framework based, pki, prince2, react vue angular, reactive programming, salesforce, sap erp hana business objects, scrum, serverless concepts, spa ssr ssg, tcpip model, togaf, trello, uml, w3c and whatwg

## Phase 5 - Shipping

**Goal:** Containerise, deploy, cache and observe what you built.

**roadmap.sh (in order):** [docker](https://roadmap.sh/docker) → [kubernetes](https://roadmap.sh/kubernetes) → [devops-beginner](https://roadmap.sh/devops-beginner) → [devops](https://roadmap.sh/devops)  
*Optional:* [terraform](https://roadmap.sh/terraform), [aws](https://roadmap.sh/aws), [devsecops](https://roadmap.sh/devsecops)

**Our modules (3):** Redis multi-tier caching, SRE and distributed tracing are in our modules.

| Course | # | Module | Main lecture | More videos |
|---|---|--------|--------------|-------------|
| 01 | 19 | Containerization, Docker & Production CI/CD | [Learn Docker – Full DevOps Course for Deploying Containerize](https://www.youtube.com/watch?v=rjjES5IsPdg) | 2 |
| 01 | 20 | Performance Engineering & Redis Multi-Tier Caching | [Diagnose slow Python code. (Feat. async/await)](https://www.youtube.com/watch?v=m_a0fN48Alw) | 1 |
| 04 | 25 | Observability, Distributed Tracing & SRE Resilience | [OpenTelemetry: Simplifying Hybrid Cloud Monitoring](https://www.youtube.com/watch?v=hLvwoow3XTk) | 1 |

**On roadmap.sh but not in our courses (learn these on roadmap.sh):**

- [docker](https://roadmap.sh/docker) (9): docker and oci, docker desktop winmaclinux, docker swarm, dockerhub, image tagging best practices, others ghcr ecr gcr acr etc, paas options, underlying technologies, using 3rd party container images
- [kubernetes](https://roadmap.sh/kubernetes) (16): assigning quotas to namespaces, choosing a managed provider, csi drivers, custom resource definitions crds, custom schedulers and extenders, gitops, horizontal pod autoscaler hpa, injecting pod config with configmaps, key concepts and terminologies, kubernetes alternatives, kubernetes extensions and apis, pod priorities, replicasets, taints and tolerations, topology spread constraints, vertical pod autoscaler vpa
- [devops-beginner](https://roadmap.sh/devops-beginner) (2): ansible, terraform
- [devops](https://roadmap.sh/devops) (60): alibaba cloud, ansible, argocd, artifactory, aws cdk, aws ecs / fargate, azure, azure functions, bitbucket, buildkite, circle ci, cloud smith, cloudformation, contabo, digital ocean, dmarc, docker swarm, dynatrace, fluxcd, freebsd, ftp / sftp, gcp functions, gitlab, gitlab ci, gitops, gke / eks / aks, graylog, heroku, hetzner, istio, javascript / nodejs, jenkins, linkerd, loki, lxc, netbsd, netlify, new relic, nexus, octopus deploy, openbsd, openshift, papertrail, pop3s, pulumi, puppet, railway, rhel / derivatives, sealed secrets, sops, spf, splunk, suse linux, teamcity, terraform, tomcat, vcs hosting, vercel, vim / nano / emacs, zabbix
- [terraform](https://roadmap.sh/terraform) (31): best practices for state, cac vs iac, checkov, circle ci, custom provisioners, file provisioner, gitlab ci, hashicorp config language hcl, hcp, infracost, installing terraform, jenkins, kics, local exec provisioner, provisioners, remote exec provisioner, scaling terraform, state force unlock, terraform apply, terraform destroy, terraform fmt, terraform plan, terraform registry, terraform validate, terragrunt, terrascan, tflint, trivy, usecases and benefits, vcs integration, what and when to use hcp
- [aws](https://roadmap.sh/aws) (23): cidr blocks, cloudfront, clusters / ecs container agents, dkim setup, elasticache, fargate, glacier, hosted zones, iaas vs paas vs saas, introduction to aws, keypairs, lambdaedge, launch config / autoscaling groups, launch templates, private subnet, public subnet, public vs private vs hybrid cloud, s3 ia, sandbox / sending limits, sender reputation, subnets, vpc, well architected framework
- [devsecops](https://roadmap.sh/devsecops) (30): acls, audit / compliance mapping, burp suite, certificate lifecycle, cia triad, cspm, ddos miligation strategy, defense in depth concepts, devsecops vs devops, edr strategy, ir lifecycle, iso 27001, javascript / nodejs, nessus, nmap basics, openvas, pki design and failover, qualys, risk quantification, sboms, secure network zoning, siem, soar automation, soar concepts, soc 2, threat modeling workflows, vim / nano / emacs, vlans, wireshark basics, zero trust concepts

## Phase 6 - Maths and machine-learning core

**Goal:** Get the maths, then build and train neural networks yourself.

**roadmap.sh (in order):** [machine-learning](https://roadmap.sh/machine-learning) → [ai-data-scientist](https://roadmap.sh/ai-data-scientist)

**Our modules (18):** roadmap.sh names the maths topics only at basics level. SVD, Gram-Schmidt, MLE, PCA and Karpathy-style from-scratch builds are in our course 05 and 06.

| Course | # | Module | Main lecture | More videos |
|---|---|--------|--------------|-------------|
| 05 | 1 | Set Language & Probability Sample Spaces | [But what is the Central Limit Theorem?](https://www.youtube.com/watch?v=zeJD6dqJ5lo) | 2 |
| 05 | 2 | Mathematical Logic for Precise Reasoning | [1.5.1 Predicate Logic 1: Video](https://www.youtube.com/watch?v=UroprmQHTLc) | - |
| 05 | 3 | Linear Systems & Matrix Transformations | [Linear transformations and matrices | Chapter 3, Essence of ](https://www.youtube.com/watch?v=kYB8IZa5AuE) | 1 |
| 05 | 4 | Vector Spaces, Span, Bases & Rank | [Linear combinations, span, and basis vectors | Chapter 2, Es](https://www.youtube.com/watch?v=k7RM-ot2NWY) | 2 |
| 05 | 5 | Eigenvectors, Eigenvalues & Diagonalization | [Eigenvectors and eigenvalues | Chapter 14, Essence of linear](https://www.youtube.com/watch?v=PFDu9oVAE-g) | 1 |
| 05 | 6 | Orthogonality, Projections & Gram-Schmidt | [14. Orthogonal Vectors and Subspaces](https://www.youtube.com/watch?v=YzZUIYRCE38) | 2 |
| 05 | 7 | Singular Value Decomposition (SVD) & Quadratic Forms | [Singular Value Decomposition (SVD): Mathematical Overview](https://www.youtube.com/watch?v=nbBvuuNVfco) | 1 |
| 05 | 8 | Linear Algebra in ML Models & PCA | [StatQuest: Principal Component Analysis (PCA), Step-by-Step](https://www.youtube.com/watch?v=FgakZw6K1QQ) | 1 |
| 05 | 9 | Multivariable Calculus & Gradient Descent | [Gradient descent, how neural networks learn | Deep Learning ](https://www.youtube.com/watch?v=IHZwWFHWa-w) | 2 |
| 05 | 10 | Bayes Theorem & Probabilistic Reasoning | [Bayes theorem, the geometry of changing beliefs](https://www.youtube.com/watch?v=HZGCoVF3YvM) | - |
| 05 | 11 | Joint Distributions, Covariance & Independence | [Covariance, Clearly Explained!!!](https://www.youtube.com/watch?v=qtaqvPAeEJY) | 2 |
| 05 | 12 | Statistical Estimation & Maximum Likelihood (MLE) | [Maximum Likelihood, clearly explained!!!](https://www.youtube.com/watch?v=XepXtl9YKwc) | - |
| 06 | 1 | Backpropagation Calculus & Neural Intuitions | [Backpropagation, intuitively | Deep Learning Chapter 3](https://www.youtube.com/watch?v=Ilg3gGewQ5U) | - |
| 06 | 3 | PyTorch Bootcamp: Tensors, Autograd & Modules | [PyTorch for Deep Learning & Machine Learning – Full Course](https://www.youtube.com/watch?v=V_xro1bcAuA) | 1 |
| 06 | 4 | TensorFlow & Keras Foundations | [TensorFlow 2.0 Complete Course - Python Neural Networks for ](https://www.youtube.com/watch?v=tPYj3fFJGjk) | - |
| 06 | 5 | Building Neural Networks from Scratch (Micrograd) | [The spelled-out intro to neural networks and backpropagation](https://www.youtube.com/watch?v=VMj-3S1tku0) | - |
| 06 | 6 | Transformers & Self-Attention Explained | [Attention in transformers, step-by-step | Deep Learning Chap](https://www.youtube.com/watch?v=eMlx5fFNoYc) | 1 |
| 06 | 7 | Reinforcement Learning & Policy Gradients | [Policy Gradient Methods in Reinforcement Learning: Deep Dive](https://www.youtube.com/watch?v=007EvVofBC0) | - |

**On roadmap.sh but not in our courses (learn these on roadmap.sh):**

- [machine-learning](https://roadmap.sh/machine-learning) (19): applications of CNNs, decision trees random forest, descriptive statistics, elasticnet regularization, explainable ai, generative adversarial networks, gradient boosting machines, gru, image / video recognition, inferential statistics, lemmatization, loocv, neural network nn basics, random variances pdfs, recurrent neural networks, roc auc, seaborn, semi supervised learning, unsupervised learning
- [ai-data-scientist](https://roadmap.sh/ai-data-scientist) (2): econometrics, exploratory data analysis

## Phase 7 - Applied LLM systems

**Goal:** Prompt, retrieve, call tools and build agents, then measure them.

**roadmap.sh (in order):** [prompt-engineering](https://roadmap.sh/prompt-engineering) → [ai-engineer](https://roadmap.sh/ai-engineer) → [ai-agents](https://roadmap.sh/ai-agents)

**Our modules (29):** ColBERT, GraphRAG, hybrid search/RRF, LangGraph internals, sandboxing and the evaluation science (judges, benchmark harnesses, guardrails) go deeper in our courses 10 to 12.

| Course | # | Module | Main lecture | More videos |
|---|---|--------|--------------|-------------|
| 01 | 25 | AI Engineering (Vector Embeddings & Tool Calling) | [LangChain Explained in 10 Minutes (Components Breakdown + Bu](https://www.youtube.com/watch?v=xTmU8ZImUO8) | 1 |
| 04 | 21 | Vector Databases & HNSW Indexing (Milvus/Pinecone) | [Searching 100 Million Vectors in 50ms | HNSW Explained Visua](https://www.youtube.com/watch?v=BvYW2ISbqGA) | - |
| 06 | 2 | Core AI Intuitions & LLM High-Level Architecture | [[1hr Talk] Intro to Large Language Models](https://www.youtube.com/watch?v=zjkBMFhNj_g) | - |
| 06 | 8 | Building GPT from Scratch (Karpathy Masterclass) | [Let's build GPT: from scratch, in code, spelled out.](https://www.youtube.com/watch?v=kCc8FmEb1nY) | - |
| 06 | 9 | Reading & Writing Frontier AI Research Papers | [How To Read AI Research Papers Effectively](https://www.youtube.com/watch?v=K6Wui3mn-uI) | - |
| 06 | 10 | Parameter-Efficient Fine-Tuning (PEFT & LoRA) | [LoRA: Low-Rank Adaptation of Large Language Models - Explain](https://www.youtube.com/watch?v=PXWYUTMt-AU) | 1 |
| 06 | 12 | Frontier LLM Trends & State of the Art | [State of AI in 2026: LLMs, Coding, Scaling Laws, China, Agen](https://www.youtube.com/watch?v=EV7WhVT270Q) | - |
| 10 | 1 | Parsing & Hierarchical Semantic Chunking | [Text Splitters in LangChain | Generative AI using LangChain ](https://www.youtube.com/watch?v=SEWS9P4ODmc) | - |
| 10 | 2 | Anthropic Contextual Retrieval Architecture | [The Best RAG Technique Yet? Anthropic’s Contextual Retrieval](https://www.youtube.com/watch?v=tmiBae2goJM) | - |
| 10 | 3 | Vector Database Internals (HNSW & Product Quantization) | [Vector Database Search - Hierarchical Navigable Small Worlds](https://www.youtube.com/watch?v=77QH0Y2PYKg) | 1 |
| 10 | 4 | Hybrid Search & Reciprocal Rank Fusion (RRF) | [Hybrid Search RAG With Langchain And Pinecone Vector DB](https://www.youtube.com/watch?v=CK0ExcCWDP4) | 2 |
| 10 | 5 | Multi-Stage Retrieval & Cross-Encoder Reranking | [Advanced RAG 04 - Reranking with Cross Encoders, and Cohere ](https://www.youtube.com/watch?v=ZFbaA9eM0uo) | - |
| 10 | 6 | ColBERTv2 & Token-Level Late Interaction | [Supercharge Your RAG with Contextualized Late Interactions](https://www.youtube.com/watch?v=xTzUn3G9YA0) | - |
| 10 | 7 | Microsoft GraphRAG & Community Summarization | [Graph RAG: Improving RAG with Knowledge Graphs](https://www.youtube.com/watch?v=vX3A96_F3FU) | - |
| 10 | 8 | Query Transformation & Agentic Multi-Hop RAG | [RAG from scratch: Part 9 (Query Translation -- HyDE)](https://www.youtube.com/watch?v=SaDzIVkYqyY) | - |
| 10 | 9 | Context Optimization & Needle-in-a-Haystack (NIAH) | [Needle In A Haystack (GPT-4 128K)](https://www.youtube.com/watch?v=KwRRuiCCdmc) | - |
| 11 | 1 | Agent Cognitive Loops & ReAct Architecture | [Understanding ReACT with LangChain](https://www.youtube.com/watch?v=Eug2clsLtFs) | 2 |
| 11 | 2 | LangGraph Internals: Stateful Graphs & Cyclic Loops | [Hierarchical multi-agent systems with LangGraph](https://www.youtube.com/watch?v=B_0TNuYi56w) | 2 |
| 11 | 3 | Function Calling & Structured Tool Execution | [How to Use OpenAI Function Calling with Python (Full Demo & ](https://www.youtube.com/watch?v=nQMLAO20QTg) | - |
| 11 | 4 | Agent Memory: Short-Term, Episodic & Semantic | [Build Agents that Never Forget: LangMem Semantic Memory Tuto](https://www.youtube.com/watch?v=3Yp-hIEcWXk) | 2 |
| 11 | 5 | Multi-Agent Collaboration Topologies & Swarms | [LangChain vs LangGraph: A Tale of Two Frameworks](https://www.youtube.com/watch?v=qAF1NjEVHhY) | 2 |
| 11 | 6 | Sandboxed Code Execution & Security Isolation | [Running AI Agents in Secure Sandboxes with E2B & Docker MCP ](https://www.youtube.com/watch?v=csT16BaTHwY) | - |
| 11 | 7 | Human-in-the-Loop & Time Travel State Rewinding | [LangGraph Agents - Human-In-The-Loop Breakpoints](https://www.youtube.com/watch?v=Za8CrPqQxpA) | 1 |
| 11 | 8 | Production Agent Evaluation & Benchmarks | [Observability and Evals for AI Agents: A Simple Breakdown](https://www.youtube.com/watch?v=FDVdLrloFOw) | - |
| 12 | 1 | LLM Evaluation Science: Ground Truth & RAGAS | [RAG Evaluation: Precision, Recall, Faithfulness, RAGAS Expla](https://www.youtube.com/watch?v=7_LTU0LA374) | 1 |
| 12 | 2 | LLM-as-a-Judge Calibration & Bias Mitigation | [Building a LLM Judge with Weights & Biases](https://www.youtube.com/watch?v=zaNR3WaPTfo) | - |
| 12 | 3 | Benchmark Harnesses (MMLU, GSM8K, HumanEval) | [How We Test AI: Benchmark Datasets Explained (MMLU, GSM8K & ](https://www.youtube.com/watch?v=7t1RdmiW3fc) | - |
| 12 | 4 | Production Guardrails Architecture & Policy Filters | [Guardrails for LLM Applications | Complete Tutorial for AI D](https://www.youtube.com/watch?v=7V1w5gnZ-kw) | - |
| 12 | 5 | NVIDIA NeMo Guardrails & Meta Llama Guard | [Building Safe and Secure LLM Applications Using NVIDIA NeMo ](https://www.youtube.com/watch?v=Hg2KibOvnLM) | - |

**On roadmap.sh but not in our courses (learn these on roadmap.sh):**

- [prompt-engineering](https://roadmap.sh/prompt-engineering) (8): ai vs agi, calibrating llms, chain of thought cot prompting, fine tuning vs prompt engg, prompt ensembling, repetition penalties, tree of thoughts tot prompting, xai
- [ai-engineer](https://roadmap.sh/ai-engineer) (51): ai safety and ethics, ai vs agi, bias and fairness, building an mcp client, building an mcp server, claude agent sdk, codex, conducting adversarial testing, content moderation apis, context vs prompt eng, cost / latency monitoring, dall e api, datahub, deepeval, deepseek, google adk, google gemini, google gemini api, helicone, hugging face, hugging face hub, hugging face inference sdk, hugging face models, hugging face tasks, jina, langchain for multimodal apps, llamaindex for multimodal apps, lm studio, mcp host, models on hugging face, modus, mongodb atlas, multimodal ai usecases, nanobanana api, ollama, openai agentkit / agent sdk, openai compatible apis, openai gpt o series, openai vision api, openrouter, posthog, ragflow, repetition penalties, replit, security and privacy concerns, supabase, transformersjs, using sdks directly, vertex ai agent builder, whisper api, windsurf
- [ai-agents](https://roadmap.sh/ai-agents) (15): acting / tool invocation, chain of thought cot, creating mcp servers, crewai, deepeval, forgetting / aging strategies, helicone, mcp hosts, npc / game ai, openllmetry, planner executor, smol depot, specify length format etc, streamed vs unstreamed responses, use relevant technical terms

## Phase 8 - Production AI

**Goal:** Serve models fast and cheaply, operate them, and attack them before others do.

**roadmap.sh (in order):** [mlops](https://roadmap.sh/mlops) → [inference-engineering](https://roadmap.sh/inference-engineering) → [ai-red-teaming](https://roadmap.sh/ai-red-teaming)

**Our modules (14):** roadmap.sh's Inference Engineering is the tracker; our course 09 adds the paper-level internals (PagedAttention, RadixAttention, Medusa, Marlin).

| Course | # | Module | Main lecture | More videos |
|---|---|--------|--------------|-------------|
| 04 | 22 | Distributed LLM Serving & PagedAttention (vLLM) | [vLLM Explained: How to Serve LLMs at Scale](https://www.youtube.com/watch?v=RT5Z-CjvWjc) | 1 |
| 06 | 11 | Machine Learning Operations (MLOps) in Production | [MLOps Course – Build Machine Learning Production Grade Proje](https://www.youtube.com/watch?v=-dJPoLm_gtE) | - |
| 09 | 1 | Inference Latency, TTFT & TPOT Trade-offs | [LLM Inference Performance: Latency and Throughput Metrics](https://www.youtube.com/watch?v=DW-mo65DJ-Q) | - |
| 09 | 2 | KV-Cache Memory Hierarchy & Growth | [LLaMA explained: KV-Cache, Rotary Positional Embedding, RMS ](https://www.youtube.com/watch?v=Mn_9W1nCFLo) | 1 |
| 09 | 3 | PagedAttention Architecture (vLLM) | [PagedAttention: Behind vLLM's Insane Speed](https://www.youtube.com/watch?v=6uPnLkCiy5g) | - |
| 09 | 4 | RadixAttention & Prefix Caching (SGLang) | [SGLang Deep Dive: RadixAttention, KV Cache & High-Throughput](https://www.youtube.com/watch?v=TWbrz5rSfFI) | - |
| 09 | 5 | Continuous & Dynamic Iteration-Level Batching | [Continuous Batching: Optimize LLM Serving Throughput and Lat](https://www.youtube.com/watch?v=iiyu86UZwGg) | - |
| 09 | 6 | Chunked Prefill & Prefill-Decode (PD) Disaggregation | [Why Separating Prefill and Decode Makes LLMs Faster | vLLM, ](https://www.youtube.com/watch?v=BaD3CTYf6V0) | 1 |
| 09 | 7 | Speculative Decoding & Medusa Multi-Head Verification | [Faster LLMs: Accelerate Inference with Speculative Decoding](https://www.youtube.com/watch?v=VkWlLSTdHs8) | 1 |
| 09 | 8 | Model Quantization for Serving (FP8, AWQ, Marlin) | [Quantization explained with PyTorch - Post-Training Quantiza](https://www.youtube.com/watch?v=0VdNflU08yA) | 2 |
| 09 | 9 | Production Benchmarking, SLAs & Autoscaling | [Optimizing Load Balancing and Autoscaling for LLM Inference ](https://www.youtube.com/watch?v=TSEGAh1bs4A) | 1 |
| 12 | 6 | Adversarial AI Security & OWASP Top 10 for LLMs | [OWASP's Top 10 Ways to Attack LLMs: AI Vulnerabilities Expos](https://www.youtube.com/watch?v=gUNXZMcd2jU) | - |
| 12 | 7 | Automated Red Teaming & Jailbreak Testing (PyRIT) | [Episode 8: Automating AI Red Teaming with PyRIT | AI Red Tea](https://www.youtube.com/watch?v=cEHTxmpAgjA) | 1 |
| 12 | 8 | Production AI Observability & OpenTelemetry Tracing | [Ultimate OpenTelemetry Guide for Tracing AI Applications](https://www.youtube.com/watch?v=fHGSxOhWO-g) | - |

**On roadmap.sh but not in our courses (learn these on roadmap.sh):**

- [mlops](https://roadmap.sh/mlops) (15): airflow, ansible, AWS / Azure / GCP, cloud native ml services, data lakes / warehouses, dvc, explainable ai, gitlab, jenkins, jetson, kubeflow, mlflow, mlops components, pytorch mobile, terraform
- [inference-engineering](https://roadmap.sh/inference-engineering) (35): attention variants, auto speech recognition, bert style models, diffusion models, eagle, encoder decoder arch, expert parallelism, few step image generation, geo aware load balancing, gpu procurement, Grace / Vera, image generation arch, indep component scaling, kernel selection / fusion, lora aware routing, mobile inference, modelopt, nims, nvidia dynamo, nvidia genai perf, omni modal models, online vs offline inf, opsbyte ratio, post training quantization, quantization aware training, safetensors, sglang genai bench, shared vs dedicated inf, sizing / procurement, text to speech tts, transformers / diffusers, video processing for VLMs, vision language models, voice activity detection, zero downtime deplo
- [ai-red-teaming](https://roadmap.sh/ai-red-teaming) (17): adversarial examples, agentic ai security, conferences, confidentiality integrity availability, countermeasures, ctf challenges, emerging threats, forums, grey box testing, industry credentials, insecure deserialization, model weight stealing, red team simulations, research opportunities, responsible disclosure, specialized courses, unsupervised learning

## Phase 9 - Hardware, training scale and Python depth (our material only)

**Goal:** Understand GPUs and kernels, how large models train across clusters, and what CPython does underneath.

**roadmap.sh:** none covers this. Follow our modules.

**Our modules (24):** roadmap.sh has no roadmap for CUDA/Triton, ZeRO/FSDP/Megatron, ring attention or 3D parallelism. Follow these modules in full.

| Course | # | Module | Main lecture | More videos |
|---|---|--------|--------------|-------------|
| 01 | 12 | CPython Bytecode, AST & Memory Architecture | [25 nooby Python habits you need to ditch](https://www.youtube.com/watch?v=qUeud6DvOWI) | 2 |
| 01 | 21 | Descriptors, Metaclasses & Zero-Copy Memory | [8 things in Python you didn't realize are descriptors](https://www.youtube.com/watch?v=mMbVs17Vmo4) | 2 |
| 01 | 22 | CPython Internals & Native Rust Extensions (PyO3) | [Combining Rust and Python: The Best of Both Worlds?](https://www.youtube.com/watch?v=lyG6AKzu4ew) | 1 |
| 07 | 1 | GPU Microarchitecture & Execution Model | [Stanford CS149 I Parallel Computing I 2023 I Lecture 1 - Why](https://www.youtube.com/watch?v=V1tINV2-9p4) | 1 |
| 07 | 2 | CUDA C++ Programming Fundamentals | [Accelerating Applications with Parallel Algorithms | CUDA C+](https://www.youtube.com/watch?v=Sdjn9FOkhnA) | - |
| 07 | 3 | CUDA Memory Hierarchy & Coalescing | [CUDA Memory Hierarchy: Coalescing, Shared Memory, Bank Confl](https://www.youtube.com/watch?v=LieS0bBgy0w) | - |
| 07 | 4 | Parallel Reduction & Warp Primitives | [CUDA Crash Course: Sum Reduction Part 1](https://www.youtube.com/watch?v=bpbit8SPMxU) | - |
| 07 | 5 | Tiled Matrix Multiplication (GEMM) | [Tiled Matrix Multiplication on GPU | 16× Faster with Shared ](https://www.youtube.com/watch?v=VHsxF8lxpWw) | - |
| 07 | 6 | OpenAI Triton Programming Fundamentals | [Lecture 14: Practitioners Guide to Triton](https://www.youtube.com/watch?v=DdTsX6DQk24) | - |
| 07 | 7 | Fused Activations & Normalization Kernels | [JUST FUSE IT: Fixing GPU Memory Bottlenecks with kernel fusi](https://www.youtube.com/watch?v=FD_xre7abZU) | - |
| 07 | 8 | FlashAttention-1 & 2 Internals | [Flash Attention derived and coded from first principles with](https://www.youtube.com/watch?v=zy8ChVd_oTM) | 1 |
| 07 | 9 | FlashAttention-3 & Hopper/Blackwell Innovations | [FlashAttention-3 is Here](https://www.youtube.com/watch?v=mbmVHvk4-xA) | 1 |
| 07 | 10 | Quantization Kernels in Triton (FP8 & INT4) | [📦 LLM Quantization Explained: FP32, FP16, INT8, INT4, GPTQ, ](https://www.youtube.com/watch?v=37g8S71LfmQ) | 2 |
| 07 | 11 | Profiling & Tuning with Nsight (NCU & NSYS) | [Intro to NVIDIA Nsight Compute | CUDA Developer Tools](https://www.youtube.com/watch?v=Iuy_RAvguBM) | 1 |
| 08 | 1 | GPU Cluster Hardware & Interconnects | [NVIDIA Networking: Introduction to ConnectX Network Interfac](https://www.youtube.com/watch?v=xXXrX1CcuBw) | 1 |
| 08 | 2 | NCCL Collective Communication Primitives | [Lecture 17: NCCL](https://www.youtube.com/watch?v=T22e3fgit-A) | 1 |
| 08 | 3 | PyTorch Distributed Data Parallel (DDP) | [Part 2: What is Distributed Data Parallel (DDP)](https://www.youtube.com/watch?v=Cvdhwx-OBBo) | - |
| 08 | 4 | DeepSpeed ZeRO & PyTorch FSDP | [How to Train Billion-Parameter Models: DeepSpeed ZeRO vs. Py](https://www.youtube.com/watch?v=4pIpM0QvEtg) | - |
| 08 | 5 | Tensor Parallelism (Megatron-LM) | [Ultimate Guide To Scaling ML Models - Megatron-LM | ZeRO | D](https://www.youtube.com/watch?v=hc0u4avAkuM) | - |
| 08 | 6 | Pipeline Parallelism (1F1B Schedules) | [PipeDream: Model, Data & Pipeline Parallelism](https://www.youtube.com/watch?v=BZrL_jy4Pp8) | - |
| 08 | 7 | Sequence Parallelism & Ring Attention | [Building a distributed training framework from first princip](https://www.youtube.com/watch?v=XoGvCBRnwLs) | - |
| 08 | 8 | 3D Parallelism Integration & Orchestration | [BigScience BLOOM | 3D Parallelism Explained | Large Language](https://www.youtube.com/watch?v=pTChDs5uD8I) | - |
| 08 | 9 | Distributed Checkpointing & Fault Tolerance | [Sponsored Session: PyTorch Distributed and Fault Tolerance -](https://www.youtube.com/watch?v=B-BXSRwAVdE) | 1 |
| 08 | 10 | Scaling Laws, Cluster Profiling & FinOps | [Chinchilla Explained: Compute-Optimal Massive Language Model](https://www.youtube.com/watch?v=PZXN7jm9IC0) | - |

## Phase 10 - Database and distributed-data internals (our material only)

**Goal:** Know how the engines you used in Phase 3 actually work.

**roadmap.sh:** none covers this. Follow our modules.

**Our modules (11):** MySQL/InnoDB, Oracle (SGA, PL/SQL, RAC), Cassandra/Scylla, LSM-trees, Neo4j, buffer pools, query optimisation, 2PC/consensus and DBRE. Oracle modules are optional unless you work with Oracle.

| Course | # | Module | Main lecture | More videos |
|---|---|--------|--------------|-------------|
| 03 | 6 | MySQL & MariaDB Architecture: InnoDB & Replication | [All Types of Database Replication Discussed](https://www.youtube.com/watch?v=aE2UPg3Ckck) | 2 |
| 03 | 7 | Oracle Architecture: SGA, PGA & Storage Subsystems | [Oracle Database Memory Architecture Explained | SGA, PGA, Ba](https://www.youtube.com/watch?v=uni59ARMAO8) | 1 |
| 03 | 8 | Oracle PL/SQL, Packages, Triggers & Cursors | [Stored Procedures in PL/SQL | Oracle PL/SQL Tutorial Videos ](https://www.youtube.com/watch?v=pfLtGDJcdm4) | 2 |
| 03 | 9 | Oracle High Availability: RAC, Data Guard & GoldenGate | [Oracle GoldenGate Microservices Hub Setup on RAC - Step-by-S](https://www.youtube.com/watch?v=1-dCb4bqo_E) | 2 |
| 03 | 14 | Cassandra & ScyllaDB: Masterless Ring & Murmur3 | [Consistent Hashing | The Backend Engineering Show](https://www.youtube.com/watch?v=p6wwj0ozifw) | 1 |
| 03 | 15 | LSM-Trees, SSTables, Compaction & DynamoDB | [The Secret Sauce Behind NoSQL: LSM Tree](https://www.youtube.com/watch?v=I6jB0nM9SKU) | 2 |
| 03 | 16 | Neo4j & Graph Databases: Index-Free Adjacency | [Neo4j (Graph Database) Crash Course](https://www.youtube.com/watch?v=8jNPelugC2s) | 1 |
| 03 | 21 | Storage Engine Internals: Buffer Pools & B+ Trees | [B-tree vs B+ tree in Database Systems](https://www.youtube.com/watch?v=UzHl2VzyZS4) | 2 |
| 03 | 22 | Query Optimization, Cost Models & Physical Joins | [#02 - History of Query Optimizers ft. IBM System R (CMU Opti](https://www.youtube.com/watch?v=62cAdANFhBg) | - |
| 03 | 23 | Transactions, Two-Phase Commit & Distributed Consensus | [Distributed Transactions are Hard (How Two-Phase Commit work](https://www.youtube.com/watch?v=eltn4x788UM) | 1 |
| 03 | 24 | Database Reliability Engineering (DBRE) & Migrations | [Zero-downtime restarts are hard to get right](https://www.youtube.com/watch?v=iQU39VQfy3s) | - |

## Phase 11 - Capstones

**Goal:** Prove it end to end.

**roadmap.sh:** none covers this. Follow our modules.

**Our modules (3):** Build one project that uses each phase: a served, retrieval-grounded agent with evaluation and guardrails behind a load-tested API.

| Course | # | Module | Main lecture | More videos |
|---|---|--------|--------------|-------------|
| 01 | 26 | Enterprise Capstone (Distributed Platform) | [What Are Microservices Really All About? (And When Not To Us](https://www.youtube.com/watch?v=lTAcCNbJ7KE) | - |
| 03 | 25 | Capstone: Polyglot Persistence Architecture | [Distributed SQL vs Polyglot Persistence: Which Database Arch](https://www.youtube.com/watch?v=xG-NtcH0IJY) | - |
| 04 | 26 | Capstone: Enterprise Payment Gateway & AI Fraud Detection | [Scan To Pay in 2 Minutes](https://www.youtube.com/watch?v=XS8ACikD2qs) | 2 |

---
_175 modules, 346 videos. Regenerate with `python scripts/generate_roadmap.py`._
