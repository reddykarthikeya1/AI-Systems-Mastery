const fs = require('fs');
const path = require('path');
const { marked } = require('marked');
const hljs = require('highlight.js');

const ROOT_DIR = path.resolve(__dirname, '..');
const HTML_OUT_DIR = path.resolve(ROOT_DIR, 'html');
const ASSETS_DIR = path.resolve(ROOT_DIR, 'scripts', 'assets');
const HIGHLIGHT_CSS_PATH = path.resolve(ROOT_DIR, 'node_modules', 'highlight.js', 'styles', 'github-dark.css');

// Configure marked with highlight.js
marked.setOptions({
  highlight: function(code, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(code, { language: lang }).value;
      } catch (e) {}
    }
    return hljs.highlightAuto(code).value;
  },
  breaks: false,
  gfm: true
});

// Custom renderer for mermaid, headings, and code blocks with copy buttons
const renderer = new marked.Renderer();

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;');
}

renderer.code = function(token) {
  const code = typeof token === 'object' ? token.text : arguments[0];
  const language = typeof token === 'object' ? token.lang : arguments[1];

  if (language === 'mermaid') {
    return `
    <div class="mermaid-container">
      <div class="diagram-toolbar">
        <button class="diagram-btn" onclick="zoomDiagram(this, -0.2)" title="Zoom Out (-)">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="8" y1="11" x2="14" y2="11"></line></svg>
        </button>
        <span class="diagram-zoom-level">100%</span>
        <button class="diagram-btn" onclick="zoomDiagram(this, 0.2)" title="Zoom In (+)">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><circle cx="11" cy="11" r="8"></circle><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg>
        </button>
        <button class="diagram-btn" onclick="resetDiagramZoom(this)" title="Reset Zoom">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><polyline points="3 3 3 8 8 8"></polyline></svg>
        </button>
        <button class="diagram-btn diagram-btn-expand" onclick="openDiagramFullscreen(this)" title="Full Resolution Modal">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 3 21 3 21 9"></polyline><polyline points="9 21 3 21 3 15"></polyline><line x1="21" y1="3" x2="14" y2="10"></line><line x1="3" y1="21" x2="10" y2="14"></line></svg>
          <span>Expand</span>
        </button>
      </div>
      <div class="mermaid-viewport">
        <div class="mermaid">\n${escapeHtml(code)}\n</div>
      </div>
    </div>`;
  }
  const highlighted = language && hljs.getLanguage(language)
    ? hljs.highlight(code, { language }).value
    : hljs.highlightAuto(code).value;
  const langLabel = language || 'text';
  return `
  <div class="code-block-wrapper">
    <div class="code-header">
      <span class="code-lang">${langLabel}</span>
      <button class="copy-btn" onclick="copyCode(this)" title="Copy code">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>
        <span>Copy</span>
      </button>
    </div>
    <pre><code class="hljs language-${langLabel}">${highlighted}</code></pre>
  </div>`;
};

// Add anchors to headers
renderer.heading = function(token) {
  const text = typeof token === 'object' ? token.text : arguments[0];
  const depth = typeof token === 'object' ? token.depth : arguments[1];
  const plainText = (text || '').replace(/<[^>]*>/g, '').trim();
  const slug = plainText.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
  return `<h${depth} id="${slug}"><a href="#${slug}" class="header-anchor">#</a>${text}</h${depth}>`;
};

// Add image lightbox support
renderer.image = function(token) {
  const href = typeof token === 'object' ? token.href : arguments[0];
  const title = typeof token === 'object' ? token.title : arguments[1];
  const text = typeof token === 'object' ? token.text : arguments[2];
  return `
  <div class="img-wrapper">
    <div class="img-container">
      <img src="${href}" alt="${text || ''}" title="${title || ''}" onclick="openImageModal(this)" loading="lazy" />
      <button class="img-expand-btn" onclick="openImageModal(this)" title="Expand Image">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 3 21 3 21 9"></polyline><polyline points="9 21 3 21 3 15"></polyline><line x1="21" y1="3" x2="14" y2="10"></line><line x1="3" y1="21" x2="10" y2="14"></line></svg>
        <span>Expand</span>
      </button>
    </div>
  </div>`;
};

marked.use({ renderer });

// Transform GitHub callout blockquotes into HTML callouts
function transformCallouts(html) {
  const alertIcons = {
    NOTE: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>`,
    TIP: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 18h6"></path><path d="M10 22h4"></path><path d="M12 2v1"></path><path d="M12 7a5 5 0 0 0-5 5c0 2 1.5 3.5 2 5h6c.5-1.5 2-3 2-5a5 5 0 0 0-5-5z"></path></svg>`,
    IMPORTANT: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>`,
    WARNING: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg>`,
    CAUTION: `<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="7.86 2 16.14 2 22 7.86 22 16.14 16.14 22 7.86 22 2 16.14 2 7.86 7.86 2"></polygon><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>`
  };

  for (const type of Object.keys(alertIcons)) {
    const regex = new RegExp(`<blockquote>\\s*<p>\\s*\\[!${type}\\]\\s*([\\s\\S]*?)<\\/blockquote>`, 'gi');
    html = html.replace(regex, (match, content) => {
      return `<div class="callout callout-${type.toLowerCase()}">
        <div class="callout-title">${alertIcons[type]} <span>${type}</span></div>
        <div class="callout-body"><p>${content}</div>
      </div>`;
    });
  }
  return html;
}

// Extract Table of Contents from HTML
function extractTOC(html) {
  const headingRegex = /<h([23])\s+id="([^"]+)">.*?<\/a>(.*?)<\/h\1>/g;
  const items = [];
  let match;
  while ((match = headingRegex.exec(html)) !== null) {
    items.push({
      level: parseInt(match[1]),
      id: match[2],
      title: match[3].replace(/<[^>]*>/g, '').trim()
    });
  }
  return items;
}

// Master curriculum tracks definition in reading order
const TRACKS = [
  {
    id: "overview",
    title: "Master Roadmap & Scorecard",
    dir: "",
    files: [
      { name: "README.md", label: "Master Curriculum & Scorecard" }
    ]
  },
  {
    id: "python",
    title: "Track 1: Python Engineering Mastery",
    dir: "01-Python-Mastery",
    files: [
      { name: "00-The-Python-Mental-Model-Visual-Map.md", label: "00: Mental Model & Visual Map" },
      { name: "01-Foundations-Syntax-Primitives.md", label: "01: Foundations & Memory Model" },
      { name: "02-Data-Structures-Under-The-Hood.md", label: "02: Data Structures Under the Hood" },
      { name: "03-Functions-Functional-Closures-Decorators.md", label: "03: Closures, Scopes & Decorators" },
      { name: "04-OOP-Dunder-Metaprogramming.md", label: "04: OOP, Dunders & Metaclasses" },
      { name: "05-Memory-Management-GIL-Garbage-Collection.md", label: "05: Memory Management, GIL & GC" },
      { name: "06-Concurrency-Asyncio-Threading-Multiprocessing.md", label: "06: Concurrency & Asyncio" },
      { name: "07-Type-System-Modern-Python-Architecture.md", label: "07: Type Systems & Protocols" },
      { name: "08-Environment-Dependency-Hell-And-Packaging-Mastery.md", label: "08: Dependency Hell & Packaging" },
      { name: "09-Enterprise-Testing-Async-Mocking-And-QA.md", label: "09: Testing, Mocking & QA" },
      { name: "10-Production-Debugging-Profiling-And-Memory-Leaks-Lab.md", label: "10: Debugging & Profiling Lab" },
      { name: "11-Legacy-Refactoring-And-Break-Fix-Engineering-Lab.md", label: "11: Monolith Refactoring Lab" },
      { name: "12-Production-SQL-And-Database-Internals.md", label: "12: Production SQL & DB Internals" },
      { name: "13-High-Performance-Web-Architecture-FastAPI-And-Pydantic-V2.md", label: "13: Web Architecture (FastAPI & Pydantic)" },
      { name: "14-Enterprise-Security-OAuth2-JWT-And-Cryptographic-RBAC.md", label: "14: Enterprise Security, JWT & RBAC" },
      { name: "15-Distributed-Task-Queues-Celery-Redis.md", label: "15: Distributed Tasks (Celery & Redis)" },
      { name: "16-Event-Driven-Python-Kafka-gRPC-Networking.md", label: "16: Event-Driven Kafka & gRPC" },
      { name: "17-Modern-Columnar-Data-Engineering-Polars-And-DuckDB.md", label: "17: Columnar Data (Polars & DuckDB)" },
      { name: "18-High-Performance-Computing-HPC-Python.md", label: "18: High-Performance Computing (HPC)" },
      { name: "19-Rust-Extensions-PyO3-And-CPython-C-ABI.md", label: "19: Rust Extensions & PyO3" },
      { name: "20-Interview-Practice-Problems-Solutions.md", label: "20: Staff Coding Practice Problems" },
      { name: "21-Scenario-Based-Interview-Questions-And-Answers.md", label: "21: Production Crisis Scenarios" },
      { name: "22-Track-1-Recap-Python-Mastery-Playbook.md", label: "22: Track 1 Recap & Playbook" }
    ]
  },
  {
    id: "lld",
    title: "Track 2: Low-Level Design (LLD)",
    dir: "02-Low-Level-Design",
    files: [
      { name: "00-The-Intuitive-LLD-Mental-Model-And-Interview-Blueprint.md", label: "00: LLD Mental Model & Blueprint" },
      { name: "00-B-Zero-Prerequisite-OOP-And-Concurrency-Primer.md", label: "00-B: Zero-Prereq OOP & Concurrency Primer" },
      { name: "01-OOP-Fundamentals-And-SOLID-Principles.md", label: "01: OOP & SOLID Principles" },
      { name: "02-UML-Modeling-Class-Sequence-State-Diagrams.md", label: "02: UML Modeling Masterclass" },
      { name: "03-Design-Patterns-Catalog-Python-Implementations.md", label: "03: Design Patterns Catalog" },
      { name: "03-B-Design-Patterns-Catalog-Part-2.md", label: "03-B: Design Patterns, Part 2" },
      { name: "04-Concurrency-Patterns-ThreadSafety-Locking.md", label: "04: Concurrency & Thread-Safety" },
      { name: "05-Curveball-Requirement-Evolution-Mastery.md", label: "05: Mid-Interview Curveball Drills" },
      { name: "06-Legacy-Code-Refactoring-To-Design-Patterns.md", label: "06: Legacy Spaghetti Refactoring" },
      { name: "07-Concurrency-Stress-Testing-And-Race-Condition-Labs.md", label: "07: Concurrency Stress-Testing Lab" },
      { name: "systems/01-distributed-job-scheduler.md", label: "Sys 01: Distributed Job Scheduler" },
      { name: "systems/02-library-management-system.md", label: "Sys 02: Library Management System" },
      { name: "systems/03-movie-booking-system.md", label: "Sys 03: Movie Booking System" },
      { name: "systems/04-car-rental-system.md", label: "Sys 04: Car Rental System" },
      { name: "systems/05-parking-lot.md", label: "Sys 05: Parking Lot" },
      { name: "systems/06-inventory-management-system.md", label: "Sys 06: Inventory Management System" },
      { name: "systems/07-ride-sharing-application.md", label: "Sys 07: Ride-Sharing Application" },
      { name: "systems/08-rate-limiter.md", label: "Sys 08: API Rate Limiter" },
      { name: "systems/09-snake-and-ladders.md", label: "Sys 09: Snake and Ladders" },
      { name: "systems/10-elevator-system.md", label: "Sys 10: Elevator System" },
      { name: "systems/11-vending-machine.md", label: "Sys 11: Vending Machine" },
      { name: "systems/12-in-memory-file-system.md", label: "Sys 12: In-Memory File System" },
      { name: "systems/13-high-throughput-logging-framework.md", label: "Sys 13: High-Throughput Logging Framework" },
      { name: "systems/14-pub-sub-message-broker.md", label: "Sys 14: Pub/Sub Message Broker (Kafka Lite)" },
      { name: "systems/15-distributed-lock-manager.md", label: "Sys 15: Distributed Lock Manager (Redlock)" },
      { name: "systems/16-kafka-consumer-group-rebalance.md", label: "Sys 16: Kafka Consumer Rebalance Protocol" },
      { name: "systems/17-splitwise-expense-sharing.md", label: "Sys 17: Splitwise & Debt Simplification" },
      { name: "systems/18-notification-alerting-service.md", label: "Sys 18: Multi-Channel Notification Service" },
      { name: "12-Scenario-Based-LLD-Interview-Questions-And-Grills.md", label: "12: Staff-Level LLD Grills" },
      { name: "13-Track-2-Recap-LLD-And-Design-Patterns-Playbook.md", label: "13: Track 2 Recap & Playbook" }
    ]
  },
  {
    id: "hld",
    title: "Track 3: High-Level Design (HLD)",
    dir: "03-High-Level-Design",
    files: [
      { name: "00-Intuitive-Mental-Models-And-Visual-Glossary.md", label: "00: HLD Intuitive Glossary & Models" },
      { name: "00-B-Zero-Prerequisite-Global-Infrastructure-Primer.md", label: "00-B: Zero-Prereq Global Infra Primer" },
      { name: "01-Distributed-Systems-Core-Prerequisites.md", label: "01: Distributed Systems Foundations" },
      { name: "02-Back-Of-The-Envelope-Calculations-Guide.md", label: "02: Back-of-the-Envelope Math" },
      { name: "03-Databases-Storage-Replication-Partitioning.md", label: "03: Databases, Sharding & Consistent Hashing" },
      { name: "04-Caching-Load-Balancing-CDNs-Proxies.md", label: "04: Caching, CDNs & Stampede Defenses" },
      { name: "05-Distributed-Transactions-Sagas-Coordination.md", label: "05: Distributed Sagas & Outbox Pattern" },
      { name: "06-HLD-Interview-Framework-And-Communication.md", label: "06: 45-Min Interview Playbook" },
      { name: "07-Chaos-Engineering-Disaster-Recovery-And-Post-Mortems.md", label: "07: Chaos Engineering & Post-Mortems" },
      { name: "08-Cloud-Cost-Engineering-And-FinOps-Architecture.md", label: "08: Cloud Cost & FinOps Architecture" },
      { name: "09-Load-Testing-Benchmarking-And-SRE-Playbook.md", label: "09: Load Testing & SRE Playbook" },
      { name: "systems/01-messaging-app.md", label: "Sys 01: Real-Time Messaging (WhatsApp)" },
      { name: "systems/02-ticketing-system-hotel-reservation.md", label: "Sys 02: Ticketing & Hotel Reservation" },
      { name: "systems/03-instagram.md", label: "Sys 03: Photo Sharing Feed (Instagram)" },
      { name: "systems/04-distributed-task-scheduler.md", label: "Sys 04: Distributed Task Scheduler" },
      { name: "systems/05-video-streaming-youtube.md", label: "Sys 05: Video Streaming (YouTube)" },
      { name: "systems/06-ecommerce-platform.md", label: "Sys 06: E-Commerce Platform (Amazon)" },
      { name: "systems/07-proximity-service.md", label: "Sys 07: Proximity Service (Yelp/Nearby)" },
      { name: "systems/08-tinder.md", label: "Sys 08: Mutual Match System (Tinder)" },
      { name: "systems/09-uber.md", label: "Sys 09: Real-Time Geospatial (Uber)" },
      { name: "systems/10-twitter.md", label: "Sys 10: Social Feed & Snowflake (Twitter)" },
      { name: "systems/11-distributed-cache-redis-cluster.md", label: "Sys 11: Distributed Cache (Redis Cluster)" },
      { name: "systems/12-distributed-search-engine-elasticsearch.md", label: "Sys 12: Search Engine & Typeahead" },
      { name: "systems/13-time-series-metrics-monitoring-prometheus.md", label: "Sys 13: Time-Series Metrics (Prometheus)" },
      { name: "systems/14-distributed-web-crawler.md", label: "Sys 14: Distributed Web Crawler" },
      { name: "systems/15-payment-gateway-idempotent-ledger.md", label: "Sys 15: Payment Gateway & Idempotent Ledger" },
      { name: "systems/16-url-shortener.md", label: "Sys 16: URL Shortener" },
      { name: "systems/17-notification-service.md", label: "Sys 17: Notification Service" },
      { name: "systems/18-typeahead-autocomplete.md", label: "Sys 18: Typeahead / Autocomplete" },
      { name: "systems/19-file-storage-and-sync-dropbox.md", label: "Sys 19: File Storage & Sync" },
      { name: "systems/20-object-store-s3.md", label: "Sys 20: Object Store (S3)" },
      { name: "11-Scenario-Based-HLD-Interview-Questions-And-Grills.md", label: "11: Crisis Scenarios & Staff Grills" },
      { name: "12-Track-3-Recap-HLD-And-Distributed-Systems-Playbook.md", label: "12: Track 3 Recap & Playbook" }
    ]
  },
  {
    id: "agentic",
    title: "Track 4: Agentic AI Engineering",
    dir: "04-Agentic-AI",
    files: [
      { name: "01-LLM-Foundations-Tokenization-Inference.md", label: "01: LLM Foundations & KV-Cache" },
      { name: "02-Prompt-Engineering-To-Tool-Calling.md", label: "02: Tool Calling & Structured Output" },
      { name: "03-RAG-And-Vectorless-RAG-Deep-Dive.md", label: "03: Advanced & Vectorless RAG" },
      { name: "04-Agent-Architectures-ReAct-PlanSolve-StateMachines.md", label: "04: ReAct Loops & Task DAGs" },
      { name: "05-LangChain-And-LangGraph-Mastery.md", label: "05: LangGraph Stateful Graphs" },
      { name: "06-Memory-Guardrails-Evaluation-Gateways.md", label: "06: Memory, Guardrails & Gateways" },
      { name: "07-Multi-Agent-Collaboration-And-Production.md", label: "07: Multi-Agent Swarms & Tracing" },
      { name: "08-Capstone-Project-Autonomous-Research-And-Code-Agent.md", label: "08: Autonomous Capstone Agent" },
      { name: "09-Scenario-Based-Agentic-AI-Interview-Questions-And-Grills.md", label: "09: Agentic Scenarios & Security" },
      { name: "10-Production-Resilience-Defensive-Prompting-And-Rate-Limits.md", label: "10: Resilience, Jitter & Circuit Breakers" },
      { name: "11-Evaluation-Harnesses-LLM-As-A-Judge-And-CI-CD.md", label: "11: Evaluation Harnesses & CI/CD" },
      { name: "12-Production-Agent-Deployment-Streaming-And-Human-In-The-Loop.md", label: "12: Production SSE & Human-in-Loop" },
      { name: "13-Vector-Database-Internals-And-HNSW-Math.md", label: "13: Vector DB Internals & HNSW Math" },
      { name: "14-Model-Fine-Tuning-LoRA-And-DPO-Alignment.md", label: "14: Fine-Tuning, LoRA & DPO Alignment" },
      { name: "15-Multimodal-Agents-And-AI-Red-Teaming-Security.md", label: "15: Multimodal Agents & AI Security" },
      { name: "16-Hierarchical-Episodic-Memory-And-GraphRAG.md", label: "16: Hierarchical Episodic Memory & GraphRAG" },
      { name: "17-Model-Context-Protocol-And-Multi-Agent-Swarms.md", label: "17: Model Context Protocol & Swarms" },
      { name: "18-GPU-Serving-Mechanics-PagedAttention-And-vLLM.md", label: "18: GPU Serving & PagedAttention" },
      { name: "19-Reasoning-Models-Test-Time-Compute-And-GRPO.md", label: "19: Reasoning Models & GRPO" },
      { name: "20-Context-Compaction-Prompt-Caching-And-Token-Budgets.md", label: "20: Context Compaction & Prompt Caching" },
      { name: "21-Track-4-Recap-Agentic-AI-Architecture-Playbook.md", label: "21: Track 4 Recap & Playbook" }
    ]
  },
  {
    id: "dsa",
    title: "Track 5: DSA Interview Playbook",
    dir: "05-DSA-Interview-Playbook",
    files: [
      { name: "01-Interview-Tactics-Dry-Run-Communication.md", label: "01: 5-Step Interview Strategy" },
      { name: "02-Essential-Patterns-Cheat-Sheet.md", label: "02: 15 Master Pattern Templates" },
      { name: "03-The-Core-75-Mastery-Walkthroughs.md", label: "03: Core 75 Visual Dry-Runs" },
      { name: "04-The-45-Minute-Ticking-Clock-Mock-Interview-Simulations.md", label: "04: 45-Min Timed Interview Drills" },
      { name: "05-The-Stuck-Engineers-Diagnostic-Decision-Tree.md", label: "05: The Stuck Diagnostic Tree" },
      { name: "06-Whiteboard-And-Google-Doc-Coding-Discipline.md", label: "06: Whiteboard & No-IDE Discipline" },
      { name: "07-Advanced-Data-Structures-Segment-Trees-Fenwick-Bitmask-DP.md", label: "07: Segment/Fenwick Trees & Bitmask DP" },
      { name: "08-Company-Specific-Interview-Playbook.md", label: "08: Company-Specific Interview Playbook" },
      { name: "09-Track-5-Recap-DSA-Mastery-And-Interview-Playbook.md", label: "09: Track 5 Recap & Playbook" }
    ]
  }
];

// Build flat list of all books for prev/next navigation
const ALL_CHAPTERS = [];
TRACKS.forEach(track => {
  track.files.forEach(file => {
    const relMd = track.dir ? path.join(track.dir, file.name).replace(/\\/g, '/') : file.name;
    const relHtml = relMd.replace(/\.md$/, '.html');
    const relPdf = relMd.replace(/\.md$/, '.pdf');
    ALL_CHAPTERS.push({
      trackId: track.id,
      trackTitle: track.title,
      label: file.label,
      relMd,
      relHtml,
      relPdf
    });
  });
});

// Load Highlight.js CSS
const highlightCss = fs.readFileSync(HIGHLIGHT_CSS_PATH, 'utf8');

// Build Master CSS for the Interactive Web Portal
const PORTAL_CSS = `
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f8fafc;
  --bg-surface: #ffffff;
  --border-color: #e2e8f0;
  --text-primary: #0f172a;
  --text-secondary: #475569;
  --text-muted: #64748b;
  --accent: #0369a1;
  --accent-hover: #075985;
  --accent-light: #e0f2fe;
  --c-note: #0369a1; --c-tip: #047857; --c-imp: #4f46e5; --c-warn: #b45309; --c-caution: #b91c1c;
  --code-bg: #0d1117;
  --sidebar-width: 310px;
  --toc-width: 250px;
  --header-height: 64px;
}

[data-theme="dark"] {
  --bg-primary: #0b0f19;
  --bg-secondary: #111827;
  --bg-surface: #172033;
  --border-color: #1e293b;
  --text-primary: #f8fafc;
  --text-secondary: #94a3b8;
  --text-muted: #94a3b8;
  --accent: #38bdf8;
  --accent-hover: #7dd3fc;
  --c-note: #38bdf8; --c-tip: #34d399; --c-imp: #a5b4fc; --c-warn: #fbbf24; --c-caution: #f87171;
  --accent-light: rgba(56, 189, 248, 0.12);
  --code-bg: #090d16;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  background-color: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.7;
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Header */
.top-nav {
  position: sticky;
  top: 0;
  height: var(--header-height);
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1.5rem;
  z-index: 100;
  backdrop-filter: blur(8px);
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 700;
  font-size: 1.15rem;
  color: var(--text-primary);
  text-decoration: none;
}

.brand-badge {
  background: linear-gradient(135deg, #0284c7, #6366f1);
  color: white;
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
}

.header-controls {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.search-input-wrap {
  position: relative;
}

.search-input {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  padding: 0.45rem 1rem 0.45rem 2.2rem;
  border-radius: 8px;
  font-size: 0.85rem;
  width: 240px;
  transition: all 0.2s;
}

.search-input:focus {
  outline: none;
  border-color: var(--accent);
  width: 320px;
  box-shadow: 0 0 0 3px var(--accent-light);
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
}

.btn-icon {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  color: var(--text-secondary);
  border-radius: 8px;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-icon:hover {
  color: var(--accent);
  border-color: var(--accent);
}

.btn-pdf {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  background: var(--accent-light);
  color: var(--accent);
  border: 1px solid var(--accent);
  padding: 0.4rem 0.8rem;
  border-radius: 8px;
  text-decoration: none;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all 0.2s;
}

.btn-pdf:hover {
  background: var(--accent);
  color: #ffffff;
}

/* Layout */
.app-container {
  display: flex;
  flex: 1;
}

/* Sidebar */
.sidebar {
  width: var(--sidebar-width);
  background: var(--bg-surface);
  border-right: 1px solid var(--border-color);
  position: sticky;
  top: var(--header-height);
  height: calc(100vh - var(--header-height));
  overflow-y: auto;
  padding: 1.25rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  scrollbar-width: thin;
}

.track-group {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
}

.track-title {
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  font-weight: 700;
  padding: 0.3rem 0.5rem;
}

.nav-link {
  display: flex;
  align-items: center;
  padding: 0.45rem 0.65rem;
  border-radius: 6px;
  color: var(--text-secondary);
  text-decoration: none;
  font-size: 0.875rem;
  transition: all 0.15s ease;
  line-height: 1.35;
}

.nav-link:hover {
  background: var(--bg-secondary);
  color: var(--text-primary);
}

.nav-link.active {
  background: var(--accent-light);
  color: var(--accent);
  font-weight: 600;
}

/* Main Content Area */
.main-wrapper {
  flex: 1;
  display: flex;
  min-width: 0;
  justify-content: center;
}

.content-container {
  max-width: 1060px;
  width: 100%;
  padding: 2.5rem 2.5rem;
}

/* Right TOC */
.toc-sidebar {
  width: var(--toc-width);
  position: sticky;
  top: var(--header-height);
  height: calc(100vh - var(--header-height));
  overflow-y: auto;
  padding: 2rem 0.85rem 2rem 1.25rem;
  border-left: 1px solid var(--border-color);
  font-size: 0.825rem;
  scrollbar-width: thin;
}

.toc-title {
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  font-size: 0.725rem;
  margin-bottom: 0.85rem;
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.toc-title::before {
  content: "";
  display: inline-block;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--accent);
}

.toc-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  position: relative;
  border-left: 1px solid var(--border-color);
  margin-left: 0.25rem;
  padding-left: 0;
}

.toc-item {
  position: relative;
}

.toc-item.level-3 {
  padding-left: 0.75rem;
}

.toc-link {
  color: var(--text-secondary);
  text-decoration: none;
  transition: all 0.18s cubic-bezier(0.4, 0, 0.2, 1);
  display: block;
  padding: 0.35rem 0.65rem;
  line-height: 1.4;
  font-size: 0.815rem;
  border-left: 2px solid transparent;
  margin-left: -1px;
  border-radius: 0 4px 4px 0;
  word-break: break-word;
}

.toc-link:hover {
  color: var(--accent);
  background: var(--accent-light);
}

.toc-link.active {
  color: var(--accent);
  font-weight: 600;
  border-left: 2px solid var(--accent);
  background: var(--accent-light);
  transform: translateX(2px);
}

/* Markdown Content Typography */
.markdown-body h1 {
  font-size: 2.25rem;
  font-weight: 800;
  color: var(--text-primary);
  margin-bottom: 1.25rem;
  line-height: 1.25;
  border-bottom: 2px solid var(--border-color);
  padding-bottom: 0.5rem;
}

.markdown-body h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text-primary);
  margin-top: 2.5rem;
  margin-bottom: 1rem;
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.4rem;
}

.markdown-body h3 {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--text-primary);
  margin-top: 1.8rem;
  margin-bottom: 0.75rem;
}

.markdown-body p {
  margin-bottom: 1.25rem;
  color: var(--text-secondary);
}

.markdown-body ul, .markdown-body ol {
  margin-bottom: 1.25rem;
  padding-left: 1.5rem;
  color: var(--text-secondary);
}

.markdown-body li {
  margin-bottom: 0.4rem;
}

.markdown-body a {
  color: var(--accent);
  text-decoration: none;
}

.markdown-body a:hover {
  text-decoration: underline;
}

.markdown-body table {
  width: 100%;
  border-collapse: collapse;
  margin: 1.5rem 0;
  font-size: 0.9rem;
}

.markdown-body th, .markdown-body td {
  border: 1px solid var(--border-color);
  padding: 0.75rem 1rem;
  text-align: left;
}

.markdown-body th {
  background: var(--bg-secondary);
  font-weight: 600;
  color: var(--text-primary);
}

.markdown-body tr:nth-child(even) {
  background: var(--bg-secondary);
}

.markdown-body hr {
  border: none;
  border-top: 1px solid var(--border-color);
  margin: 2.5rem 0;
}

.header-anchor {
  margin-right: 0.4rem;
  color: var(--text-muted);
  text-decoration: none;
  opacity: 0;
  transition: opacity 0.2s;
}

h2:hover .header-anchor, h3:hover .header-anchor {
  opacity: 1;
}

/* Callouts */
.callout {
  border-radius: 8px;
  padding: 1rem 1.25rem;
  margin: 1.5rem 0;
  border-left: 4px solid;
}

.callout-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 700;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 0.4rem;
}

.callout-body p {
  margin-bottom: 0;
}

.callout-note { background: rgba(2, 132, 199, 0.08); border-color: #0284c7; color: var(--text-primary); }
.callout-note .callout-title { color: var(--c-note); }

.callout-tip { background: rgba(16, 185, 129, 0.08); border-color: #10b981; color: var(--text-primary); }
.callout-tip .callout-title { color: var(--c-tip); }

.callout-important { background: rgba(99, 102, 241, 0.08); border-color: #6366f1; color: var(--text-primary); }
.callout-important .callout-title { color: var(--c-imp); }

.callout-warning { background: rgba(245, 158, 11, 0.08); border-color: #f59e0b; color: var(--text-primary); }
.callout-warning .callout-title { color: var(--c-warn); }

.callout-caution { background: rgba(239, 68, 68, 0.08); border-color: #ef4444; color: var(--text-primary); }
.callout-caution .callout-title { color: var(--c-caution); }

/* Code Blocks */
.code-block-wrapper {
  background: var(--code-bg);
  border-radius: 10px;
  margin: 1.5rem 0;
  border: 1px solid var(--border-color);
  overflow: hidden;
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(255, 255, 255, 0.04);
  padding: 0.4rem 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}

.code-lang {
  color: #94a3b8;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-family: monospace;
}

.copy-btn {
  background: transparent;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.75rem;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.copy-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
}

.copy-btn.copied {
  color: #10b981;
}

.markdown-body pre {
  margin: 0;
  padding: 1rem;
  overflow-x: auto;
  font-size: 0.875rem;
  line-height: 1.6;
}

.markdown-body code {
  font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace;
}

:not(pre) > code {
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  padding: 0.15rem 0.35rem;
  border-radius: 4px;
  font-size: 0.85em;
  color: var(--accent);
}

/* Images & Lightbox */
.img-wrapper {
  display: flex;
  justify-content: center;
  margin: 2rem 0;
}

.img-container {
  position: relative;
  display: inline-block;
  max-width: 100%;
}

.markdown-body img {
  max-width: 100%;
  height: auto;
  border-radius: 10px;
  border: 1px solid var(--border-color);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.08);
  cursor: zoom-in;
  transition: all 0.2s ease;
  display: block;
}

.markdown-body img:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  border-color: var(--accent);
}

.img-expand-btn {
  position: absolute;
  bottom: 0.75rem;
  right: 0.75rem;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(6px);
  color: #ffffff;
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 6px;
  padding: 0.35rem 0.65rem;
  font-size: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  opacity: 0.85;
  transition: all 0.2s ease;
  z-index: 5;
}

.img-container:hover .img-expand-btn {
  opacity: 1;
}

.img-expand-btn:hover {
  background: var(--accent);
  border-color: var(--accent);
  color: #ffffff;
}

/* Mermaid Diagrams Container & Controls */
.mermaid-container {
  position: relative;
  display: flex;
  flex-direction: column;
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 1.25rem 1rem;
  margin: 2rem 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
}

.diagram-toolbar {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  display: flex;
  align-items: center;
  gap: 0.35rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  padding: 0.25rem 0.5rem;
  border-radius: 8px;
  z-index: 10;
  backdrop-filter: blur(8px);
}

.diagram-btn {
  background: transparent;
  border: none;
  color: var(--text-secondary);
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  font-size: 0.75rem;
  font-weight: 600;
  padding: 0.25rem 0.45rem;
  border-radius: 6px;
  transition: all 0.15s ease;
}

.diagram-btn:hover {
  background: var(--border-color);
  color: var(--accent);
}

.diagram-btn-expand {
  border-left: 1px solid var(--border-color);
  padding-left: 0.5rem;
  margin-left: 0.2rem;
  color: var(--accent);
}

.diagram-zoom-level {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-muted);
  min-width: 40px;
  text-align: center;
  user-select: none;
}

.mermaid-viewport {
  width: 100%;
  overflow-x: auto;
  overflow-y: hidden;
  display: flex;
  justify-content: center;
  padding: 2.2rem 0.5rem 0.5rem 0.5rem;
  scrollbar-width: thin;
}

.mermaid {
  display: inline-block;
  min-width: fit-content;
  text-align: center;
  transform-origin: top center;
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.mermaid svg {
  max-width: none !important;
  height: auto !important;
  display: inline-block;
  margin: 0 auto;
}

/* Fullscreen High-Resolution Modal */
.pv-modal {
  display: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(15, 23, 42, 0.88);
  backdrop-filter: blur(10px);
  z-index: 9999;
  justify-content: center;
  align-items: center;
  padding: 1.5rem;
}

.pv-modal.open {
  display: flex !important;
}

.pv-modal-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  border-radius: 14px;
  width: 95vw;
  height: 92vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 25px 60px -15px rgba(0, 0, 0, 0.35);
}

.pv-modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.9rem 1.5rem;
  border-bottom: 1px solid var(--border-color);
  background: var(--bg-secondary);
}

.pv-modal-title {
  display: flex;
  align-items: center;
  gap: 0.6rem;
  font-weight: 700;
  font-size: 0.95rem;
  color: var(--text-primary);
}

.pv-modal-tools {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.pv-btn {
  background: var(--bg-surface);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  border-radius: 6px;
  padding: 0.35rem 0.65rem;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.3rem;
  transition: all 0.15s ease;
}

.pv-btn:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.pv-zoom-val {
  font-size: 0.8rem;
  font-weight: 700;
  color: var(--text-secondary);
  min-width: 44px;
  text-align: center;
  user-select: none;
}

.pv-close-btn {
  background: transparent;
  border: none;
  font-size: 1.6rem;
  line-height: 1;
  color: var(--text-muted);
  cursor: pointer;
  padding: 0.2rem 0.5rem;
  border-radius: 6px;
  margin-left: 0.5rem;
  transition: all 0.15s ease;
}

.pv-close-btn:hover {
  background: rgba(239, 68, 68, 0.12);
  color: #ef4444;
}

.pv-modal-viewport {
  flex: 1;
  overflow: auto;
  padding: 2.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
  background: var(--bg-surface);
  cursor: grab;
}

.pv-modal-viewport:active {
  cursor: grabbing;
}

.pv-modal-content {
  transform-origin: center center;
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1);
  display: inline-block;
}

.pv-modal-content svg {
  max-width: none !important;
  height: auto !important;
  display: block;
}

/* Prev / Next Pagination */
.page-navigation {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
  margin-top: 3.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
}

.nav-card {
  display: flex;
  flex-direction: column;
  padding: 1rem 1.25rem;
  border: 1px solid var(--border-color);
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.2s;
}

.nav-card:hover {
  border-color: var(--accent);
  background: var(--bg-secondary);
  transform: translateY(-2px);
}

.nav-card.next {
  text-align: right;
  align-items: flex-end;
}

.nav-direction {
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.nav-page-title {
  font-weight: 600;
  color: var(--text-primary);
  font-size: 0.95rem;
}

/* Reading Progress Bar */
.reading-progress {
  position: fixed;
  top: 0;
  left: 0;
  height: 3px;
  background: linear-gradient(90deg, #0284c7, #6366f1);
  z-index: 200;
  width: 0%;
  transition: width 0.1s ease;
}



.markdown-body p a, .markdown-body li a, .markdown-body td a { text-decoration: underline; text-underline-offset: 2px; }
/* Accessibility */
.skip-link {
  position: absolute; left: -999px; top: 0; z-index: 400;
  background: var(--accent); color: #fff; padding: 0.6rem 1rem; border-radius: 0 0 8px 0; font-weight: 600;
}
.skip-link:focus { left: 0; }
:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px; border-radius: 4px; }
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation: none !important; transition: none !important; scroll-behavior: auto !important; }
}

/* Full-text search results */
.search-results {
  position: absolute; top: calc(100% + 6px); right: 0; width: min(560px, 92vw); max-height: 70vh; overflow-y: auto;
  background: var(--bg-surface); border: 1px solid var(--border-color); border-radius: 10px;
  box-shadow: 0 12px 32px rgba(15, 23, 42, 0.25); z-index: 300; padding: 0.35rem;
}
.search-results[hidden] { display: none; }
.sr-item { display: block; padding: 0.6rem 0.75rem; border-radius: 8px; text-decoration: none; color: var(--text-primary); }
.sr-item:hover, .sr-item.sr-active { background: var(--accent-light); }
.sr-title { font-weight: 600; font-size: 0.9rem; }
.sr-sec { font-size: 0.75rem; color: var(--text-secondary); margin-top: 1px; }
.sr-snip { font-size: 0.8rem; color: var(--text-secondary); margin-top: 3px; line-height: 1.4; }
.sr-snip mark { background: #fde68a; color: #1f2937; border-radius: 2px; padding: 0 1px; }
.sr-empty { padding: 0.9rem; color: var(--text-secondary); font-size: 0.85rem; }

/* Mobile navigation drawer */
.btn-menu { display: none; }
.nav-overlay { display: none; }
@media (max-width: 768px) {
  .btn-menu { display: inline-flex; align-items: center; justify-content: center; min-width: 44px; min-height: 44px;
    background: transparent; border: 1px solid var(--border-color); border-radius: 8px; color: var(--text-primary); cursor: pointer; }
  .top-nav { padding: 0 0.6rem; gap: 0.4rem; }
  .brand span:last-child, .btn-pdf span, .progress-stat-badge { display: none; }
  .header-controls { gap: 0.4rem; }
  .btn-mark-read span { font-size: 0.7rem; }
  .btn-icon, .btn-pdf, .btn-mark-read, .diagram-btn { min-height: 44px; min-width: 44px; }
  .sidebar {
    display: flex !important; position: fixed; top: var(--header-height); left: 0; bottom: 0; height: auto;
    width: min(86vw, 340px); z-index: 250; transform: translateX(-102%); transition: transform 0.2s ease;
    box-shadow: 8px 0 24px rgba(15, 23, 42, 0.25);
  }
  body.nav-open .sidebar { transform: none; }
  body.nav-open .nav-overlay { display: block; position: fixed; inset: var(--header-height) 0 0 0; background: rgba(15, 23, 42, 0.5); z-index: 240; }
  .sidebar .nav-link { min-height: 44px; }
  .search-input { width: 120px; }
  .search-input:focus { width: 160px; }
  .search-results { position: fixed; top: var(--header-height); left: 0.5rem; right: 0.5rem; width: auto; }
}

/* Responsive */
@media (max-width: 1100px) {
  .toc-sidebar { display: none; }
}



/* Progress Tracker & Mark as Read */
.progress-stat-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--bg-secondary);
  border: 1px solid var(--border-color);
  padding: 0.35rem 0.75rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
  color: var(--text-secondary);
}

.progress-mini-bar {
  width: 50px;
  height: 6px;
  background: var(--border-color);
  border-radius: 3px;
  overflow: hidden;
}

.progress-mini-fill {
  height: 100%;
  background: #10b981;
  width: 0%;
  transition: width 0.3s ease;
}

.btn-mark-read {
  display: flex;
  align-items: center;
  gap: 0.45rem;
  background: var(--bg-secondary);
  color: var(--text-secondary);
  border: 1px solid var(--border-color);
  padding: 0.4rem 0.85rem;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-mark-read:hover {
  border-color: #10b981;
  color: #10b981;
}

.btn-mark-read.is-read {
  background: rgba(16, 185, 129, 0.12);
  color: #10b981;
  border-color: #10b981;
}

.bottom-completion-wrap {
  margin-top: 2.5rem;
  padding-top: 1.5rem;
  border-top: 1px solid var(--border-color);
  display: flex;
  justify-content: center;
}

.btn-mark-read-large {
  padding: 0.65rem 1.75rem;
  font-size: 0.95rem;
}

.sidebar-check-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 15px;
  height: 15px;
  border-radius: 50%;
  border: 1.5px solid var(--border-color);
  font-size: 9px;
  color: transparent;
  flex-shrink: 0;
  margin-left: 0.4rem;
  transition: all 0.2s ease;
}

.nav-link.is-read .sidebar-check-icon {
  background: #10b981;
  border-color: #10b981;
  color: #ffffff;
}

.nav-link {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-label-text {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
`;

// Build Master JS
const PORTAL_JS = `
function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'light';
  const next = current === 'light' ? 'dark' : 'light';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
}

// Init theme
(function() {
  const saved = localStorage.getItem('theme') || 'light';
  document.documentElement.setAttribute('data-theme', saved);
})();

// Reading Progress Bar at page top
window.addEventListener('scroll', () => {
  const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
  const scrolled = (winScroll / height) * 100;
  const el = document.getElementById('progress-bar');
  if (el) el.style.width = scrolled + '%';
});

// Active Heading Indicator for Right "On This Page" TOC
(function initTocScrollSpy() {
  function setupSpy() {
    const tocLinks = Array.from(document.querySelectorAll('.toc-link'));
    if (tocLinks.length === 0) return;

    const headings = [];
    tocLinks.forEach(link => {
      const href = link.getAttribute('href');
      if (href && href.startsWith('#')) {
        const id = decodeURIComponent(href.substring(1));
        const el = document.getElementById(id);
        if (el) {
          headings.push({ id, el, link });
        }
      }
    });

    if (headings.length === 0) return;

    const tocSidebar = document.querySelector('.toc-sidebar');
    let isClickScrolling = false;
    let clickTimeout = null;

    function updateActiveHeading() {
      if (isClickScrolling) return;

      const scrollY = window.scrollY || window.pageYOffset;
      const headerOffset = 95;
      const scrollPos = scrollY + headerOffset;

      let activeItem = null;
      const isAtBottom = (window.innerHeight + scrollY) >= (document.documentElement.scrollHeight - 50);

      if (isAtBottom) {
        activeItem = headings[headings.length - 1];
      } else {
        for (let i = 0; i < headings.length; i++) {
          const top = headings[i].el.getBoundingClientRect().top + scrollY;
          if (top <= scrollPos) {
            activeItem = headings[i];
          } else {
            break;
          }
        }
        if (!activeItem && headings.length > 0) {
          activeItem = headings[0];
        }
      }

      headings.forEach(item => {
        if (activeItem && item.id === activeItem.id) {
          if (!item.link.classList.contains('active')) {
            item.link.classList.add('active');
            if (tocSidebar) {
              const linkTop = item.link.offsetTop;
              const sidebarScroll = tocSidebar.scrollTop;
              const sidebarHeight = tocSidebar.clientHeight;
              if (linkTop < sidebarScroll + 40 || linkTop > sidebarScroll + sidebarHeight - 60) {
                tocSidebar.scrollTo({
                  top: Math.max(0, linkTop - sidebarHeight / 2),
                  behavior: 'smooth'
                });
              }
            }
          }
        } else {
          item.link.classList.remove('active');
        }
      });
    }

    // Intercept TOC link clicks for smooth scrolling and immediate activation
    headings.forEach(item => {
      item.link.addEventListener('click', (e) => {
        e.preventDefault();
        isClickScrolling = true;
        clearTimeout(clickTimeout);

        headings.forEach(h => h.link.classList.remove('active'));
        item.link.classList.add('active');

        const headerOffset = 80;
        const elementPos = item.el.getBoundingClientRect().top;
        const offsetPos = elementPos + window.pageYOffset - headerOffset;

        window.scrollTo({
          top: offsetPos,
          behavior: 'smooth'
        });

        history.pushState(null, '', '#' + item.id);

        clickTimeout = setTimeout(() => {
          isClickScrolling = false;
          updateActiveHeading();
        }, 600);
      });
    });

    // Throttled scroll listener
    let ticking = false;
    window.addEventListener('scroll', () => {
      if (!ticking) {
        window.requestAnimationFrame(() => {
          updateActiveHeading();
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });

    // Initial check
    updateActiveHeading();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', setupSpy);
  } else {
    setTimeout(setupSpy, 50);
  }
})();

// Copy Code
function copyCode(btn) {
  const pre = btn.closest('.code-block-wrapper').querySelector('pre');
  navigator.clipboard.writeText(pre.innerText).then(() => {
    btn.classList.add('copied');
    btn.querySelector('span').innerText = 'Copied!';
    setTimeout(() => {
      btn.classList.remove('copied');
      btn.querySelector('span').innerText = 'Copy';
    }, 2000);
  });
}


// ---------- Accessibility helpers ----------
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('button[title], a[title]').forEach(function (el) {
    if (!el.getAttribute('aria-label')) el.setAttribute('aria-label', el.getAttribute('title'));
  });
  document.querySelectorAll('.mermaid-container').forEach(function (c) {
    var h = c, label = 'Diagram';
    while (h && (h = h.previousElementSibling)) {
      if (/^H[1-6]$/.test(h.tagName)) { label = 'Diagram for section: ' + h.textContent.replace('#', '').trim(); break; }
    }
    c.setAttribute('role', 'group');
    c.setAttribute('aria-label', label);
    var vp = c.querySelector('.mermaid-viewport');
    if (vp) { vp.setAttribute('tabindex', '0'); vp.setAttribute('role', 'region'); vp.setAttribute('aria-label', label + ' (scrollable)'); }
  });
  document.querySelectorAll('pre, pre code, .table-wrap, table').forEach(function (el) {
    if (el.scrollWidth > el.clientWidth + 1 && !el.hasAttribute('tabindex')) el.setAttribute('tabindex', '0');
  });
  var menuBtn = document.getElementById('menu-btn');
  if (menuBtn) {
    menuBtn.addEventListener('click', function () {
      var open = document.body.classList.toggle('nav-open');
      menuBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    var ov = document.getElementById('nav-overlay');
    if (ov) ov.addEventListener('click', function () { document.body.classList.remove('nav-open'); menuBtn.setAttribute('aria-expanded', 'false'); });
  }
});

// ---------- Full-text search (prebuilt index, no network) ----------
(function () {
  var active = -1;
  function esc(t) { return t.replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function root() { var d = (window.CURRENT_PAGE || '').split('/').length - 1; return d === 0 ? '.' : Array(d).fill('..').join('/'); }
  window.runSearch = function (q) {
    var box = document.getElementById('search-results');
    if (!box) return;
    var terms = q.toLowerCase().split(/[^a-z0-9_+#.]+/).filter(function (t) { return t.length > 1; });
    if (!terms.length || !window.SEARCH_INDEX) { box.hidden = true; box.innerHTML = ''; return; }
    var hits = [];
    window.SEARCH_INDEX.forEach(function (doc) {
      doc.s.forEach(function (sec) {
        var hay = sec.x, score = 0, ok = true;
        for (var i = 0; i < terms.length; i++) {
          var t = terms[i], n = 0, pos = hay.indexOf(t);
          while (pos !== -1 && n < 50) { n++; pos = hay.indexOf(t, pos + t.length); }
          var inHead = sec.h.toLowerCase().indexOf(t) !== -1, inTitle = doc.t.toLowerCase().indexOf(t) !== -1;
          if (!n && !inHead && !inTitle) { ok = false; break; }
          score += Math.min(n, 10) + (inHead ? 15 : 0) + (inTitle ? 8 : 0);
        }
        if (ok) hits.push({ doc: doc, sec: sec, score: score });
      });
    });
    hits.sort(function (a, b) { return b.score - a.score; });
    var seen = {}, out = [];
    for (var i = 0; i < hits.length && out.length < 12; i++) {
      var key = hits[i].doc.u + '#' + hits[i].sec.id;
      if (!seen[key]) { seen[key] = 1; out.push(hits[i]); }
    }
    if (!out.length) { box.innerHTML = '<div class="sr-empty">No results for "' + esc(q) + '".</div>'; box.hidden = false; return; }
    box.innerHTML = out.map(function (h, idx) {
      var x = h.sec.x, p = x.indexOf(terms[0]); if (p < 0) p = 0;
      var snip = esc(x.substring(Math.max(0, p - 50), p + 130));
      terms.forEach(function (t) { snip = snip.split(t).join('<mark>' + t + '</mark>'); });
      var href = root() + '/' + h.doc.u + (h.sec.id ? '#' + h.sec.id : '');
      return '<a class="sr-item" role="option" data-i="' + idx + '" href="' + href + '"><div class="sr-title">' + esc(h.doc.t) + '</div><div class="sr-sec">' + esc(h.sec.h) + '</div><div class="sr-snip">... ' + snip + ' ...</div></a>';
    }).join('');
    box.hidden = false; active = -1;
  };
  document.addEventListener('keydown', function (e) {
    var inp = document.querySelector('.search-input'), box = document.getElementById('search-results');
    if (e.key === '/' && document.activeElement && !/INPUT|TEXTAREA/.test(document.activeElement.tagName)) { e.preventDefault(); inp && inp.focus(); return; }
    if (!box || box.hidden) return;
    var items = box.querySelectorAll('.sr-item');
    if (e.key === 'Escape') { box.hidden = true; inp && inp.blur(); }
    else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      active = e.key === 'ArrowDown' ? Math.min(items.length - 1, active + 1) : Math.max(0, active - 1);
      items.forEach(function (it, i) { it.classList.toggle('sr-active', i === active); });
      if (items[active]) items[active].scrollIntoView({ block: 'nearest' });
    } else if (e.key === 'Enter' && active >= 0 && items[active]) { window.location.href = items[active].getAttribute('href'); }
  });
  document.addEventListener('click', function (e) {
    var box = document.getElementById('search-results');
    if (box && !e.target.closest('.search-input-wrap')) box.hidden = true;
  });
})();

// Client search filter in sidebar
function filterNav(query) {
  if (window.runSearch) window.runSearch(query);
  const q = query.toLowerCase().trim();
  const links = document.querySelectorAll('.sidebar .nav-link');
  links.forEach(link => {
    const text = link.innerText.toLowerCase();
    if (!q || text.includes(q)) {
      link.style.display = 'flex';
    } else {
      link.style.display = 'none';
    }
  });
}

// Master Course Completion Progress Tracker
const TOTAL_CHAPTERS = ${ALL_CHAPTERS.length};

function getCompletedList() {
  try {
    return JSON.parse(localStorage.getItem('pbc_read_chapters') || '[]');
  } catch(e) {
    return [];
  }
}

function toggleCurrentChapterRead() {
  if (!window.CURRENT_PAGE) return;
  let list = getCompletedList();
  const idx = list.indexOf(window.CURRENT_PAGE);
  if (idx >= 0) {
    list.splice(idx, 1);
  } else {
    list.push(window.CURRENT_PAGE);
  }
  localStorage.setItem('pbc_read_chapters', JSON.stringify(list));
  refreshProgressUI();
}

function refreshProgressUI() {
  const list = getCompletedList();
  const count = list.length;
  const pct = Math.round((count / TOTAL_CHAPTERS) * 100);

  // Update header text and mini bar
  const textEl = document.getElementById('header-progress-text');
  const barEl = document.getElementById('header-progress-bar');
  if (textEl) textEl.innerText = \`\${count}/\${TOTAL_CHAPTERS} (\${pct}%)\`;
  if (barEl) barEl.style.width = pct + '%';

  // Update Mark as Read buttons on this page
  const isRead = window.CURRENT_PAGE && list.includes(window.CURRENT_PAGE);
  const btns = [document.getElementById('header-mark-read-btn'), document.getElementById('bottom-mark-read-btn')];
  btns.forEach(btn => {
    if (!btn) return;
    if (isRead) {
      btn.classList.add('is-read');
      btn.innerHTML = \`<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="20 6 9 17 4 12"></polyline></svg><span>Completed ✓</span>\`;
    } else {
      btn.classList.remove('is-read');
      btn.innerHTML = \`<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"></circle></svg><span>Mark as Read</span>\`;
    }
  });

  // Update sidebar checkmarks
  document.querySelectorAll('.nav-link').forEach(link => {
    const rel = link.getAttribute('data-rel');
    if (rel && list.includes(rel)) {
      link.classList.add('is-read');
    } else {
      link.classList.remove('is-read');
    }
  });
}

document.addEventListener('DOMContentLoaded', refreshProgressUI);

// Diagram Zoom & Pan Controller
function zoomDiagram(btn, delta) {
  const container = btn.closest('.mermaid-container');
  const target = container.querySelector('.mermaid');
  const label = container.querySelector('.diagram-zoom-level');
  let currentZoom = parseFloat(target.getAttribute('data-zoom') || '1');
  currentZoom = Math.max(0.4, Math.min(3.0, currentZoom + delta));
  target.setAttribute('data-zoom', currentZoom);
  target.style.transform = 'scale(' + currentZoom + ')';
  if (label) label.innerText = Math.round(currentZoom * 100) + '%';
}

function resetDiagramZoom(btn) {
  const container = btn.closest('.mermaid-container');
  const target = container.querySelector('.mermaid');
  const label = container.querySelector('.diagram-zoom-level');
  target.setAttribute('data-zoom', '1');
  target.style.transform = 'scale(1)';
  if (label) label.innerText = '100%';
}

// Fullscreen Modal for Diagrams and Images
let modalScale = 1;

function openDiagramFullscreen(btn) {
  const container = btn.closest('.mermaid-container');
  if (!container) return;
  const svg = container.querySelector('.mermaid svg') || container.querySelector('.mermaid-viewport svg');
  if (!svg) {
    console.warn('No diagram SVG found in container');
    return;
  }
  const modal = document.getElementById('pv-modal');
  const content = document.getElementById('pv-modal-content');
  const title = document.getElementById('pv-modal-title-text');
  if (title) title.innerText = 'High-Resolution Architecture Viewer';

  const clonedSvg = svg.cloneNode(true);
  clonedSvg.style.maxWidth = '90vw';
  clonedSvg.style.maxHeight = '75vh';
  clonedSvg.style.width = 'auto';
  clonedSvg.style.height = 'auto';

  if (content) {
    content.innerHTML = '';
    content.appendChild(clonedSvg);
  }
  modalScale = 1;
  updateModalScale();
  if (modal) modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function openImageModal(target) {
  let img = target;
  if (target && target.tagName !== 'IMG') {
    img = target.closest('.img-container')?.querySelector('img') || target.closest('.img-wrapper')?.querySelector('img');
  }
  if (!img) return;
  const modal = document.getElementById('pv-modal');
  const content = document.getElementById('pv-modal-content');
  const title = document.getElementById('pv-modal-title-text');
  if (title) title.innerText = img.getAttribute('title') || img.getAttribute('alt') || 'High-Resolution Image Viewer';
  if (content) {
    content.innerHTML = '<img src="' + img.src + '" style="max-height: 75vh; max-width: 90vw; object-fit: contain; border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.3);" />';
  }
  modalScale = 1;
  updateModalScale();
  if (modal) modal.classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closePvModal(e) {
  if (e && e.target && e.target.closest('.pv-modal-card') && !e.target.classList.contains('pv-close-btn')) {
    return;
  }
  const modal = document.getElementById('pv-modal');
  if (modal) modal.classList.remove('open');
  document.body.style.overflow = '';
}

function modalZoomStep(delta) {
  modalScale = Math.max(0.3, Math.min(4.0, modalScale + delta));
  updateModalScale();
}

function modalReset() {
  modalScale = 1;
  updateModalScale();
}

function updateModalScale() {
  const content = document.getElementById('pv-modal-content');
  const label = document.getElementById('pv-zoom-val');
  if (content) content.style.transform = 'scale(' + modalScale + ')';
  if (label) label.innerText = Math.round(modalScale * 100) + '%';
}

// Close modal on Escape
document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') closePvModal();
});
`;

function buildPageHtml(currentChapter, bodyHtml, tocItems) {
  const currentIndex = ALL_CHAPTERS.findIndex(c => c.relHtml === currentChapter.relHtml);
  const prevChapter = currentIndex > 0 ? ALL_CHAPTERS[currentIndex - 1] : null;
  const nextChapter = currentIndex < ALL_CHAPTERS.length - 1 ? ALL_CHAPTERS[currentIndex + 1] : null;

  // Compute relative path to root HTML directory
  const pageDepth = currentChapter.relHtml.split('/').length - 1;
  const rootRel = pageDepth === 0 ? '.' : Array(pageDepth).fill('..').join('/');

  // Build sidebar HTML
  let sidebarHtml = '';
  TRACKS.forEach(track => {
    sidebarHtml += `<div class="track-group">
      <div class="track-title">${track.title}</div>`;
    track.files.forEach(file => {
      const relMd = track.dir ? path.join(track.dir, file.name).replace(/\\/g, '/') : file.name;
      const relHtml = relMd.replace(/\.md$/, '.html');
      const href = `${rootRel}/${relHtml}`;
      const isActive = relHtml === currentChapter.relHtml;
      sidebarHtml += `<a href="${href}" class="nav-link ${isActive ? 'active' : ''}" data-rel="${relHtml}"><span class="nav-label-text">${file.label}</span><span class="sidebar-check-icon">✓</span></a>`;
    });
    sidebarHtml += `</div>`;
  });

  // Build TOC HTML
  let tocHtml = '';
  if (tocItems.length > 0) {
    tocHtml = `<div class="toc-title">On This Page</div><ul class="toc-list">`;
    tocItems.forEach(item => {
      tocHtml += `<li class="toc-item level-${item.level}"><a href="#${item.id}" class="toc-link">${item.title}</a></li>`;
    });
    tocHtml += `</ul>`;
  }

  // Build pagination cards
  let navHtml = `<div class="page-navigation">`;
  if (prevChapter) {
    navHtml += `
    <a href="${rootRel}/${prevChapter.relHtml}" class="nav-card prev">
      <span class="nav-direction">← Previous Chapter</span>
      <span class="nav-page-title">${prevChapter.label}</span>
    </a>`;
  } else {
    navHtml += `<div></div>`;
  }
  if (nextChapter) {
    navHtml += `
    <a href="${rootRel}/${nextChapter.relHtml}" class="nav-card next">
      <span class="nav-direction">Next Chapter →</span>
      <span class="nav-page-title">${nextChapter.label}</span>
    </a>`;
  } else {
    navHtml += `<div></div>`;
  }
  navHtml += `</div>`;

  const pdfHref = `${rootRel}/../pdfs/${currentChapter.relPdf}`;

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>${currentChapter.label} | PBC 2026 Master Preparation Guide</title>
  <style>
    ${highlightCss}
    ${PORTAL_CSS}
  </style>
  <link rel="stylesheet" href="${rootRel}/assets/katex/katex.min.css">
  <script defer src="${rootRel}/assets/katex/katex.min.js"></script>
  <script defer src="${rootRel}/assets/katex/auto-render.min.js"></script>
  <script defer src="${rootRel}/assets/search-index.js"></script>
  <script src="${rootRel}/assets/mermaid.min.js"></script>
  <script>
    document.addEventListener("DOMContentLoaded", function() {
      // 1. Initialize Mermaid FIRST on untouched raw diagram blocks
      if (window.mermaid) {
        mermaid.initialize({
          startOnLoad: true,
          theme: 'neutral',
          securityLevel: 'loose',
          fontFamily: 'Inter, -apple-system, sans-serif',
          flowchart: {
            curve: 'basis',
            useMaxWidth: false,
            htmlLabels: true
          },
          sequence: {
            useMaxWidth: false,
            showSequenceNumbers: true,
            actorMargin: 50,
            boxMargin: 10,
            boxTextMargin: 5,
            noteMargin: 10,
            messageMargin: 35
          },
          er: { useMaxWidth: false },
          class: { useMaxWidth: false },
          state: { useMaxWidth: false }
        });
      }

      // 2. Render KaTeX ONLY on article prose, strictly excluding .mermaid and code blocks
      function initKatex() {
        if (typeof renderMathInElement === 'function') {
          const target = document.querySelector('.article-content') || document.querySelector('.markdown-body');
          if (target) {
            renderMathInElement(target, {
              delimiters: [
                { left: '$$', right: '$$', display: true },
                { left: '$', right: '$', display: false }
              ],
              ignoredClasses: ['mermaid', 'code-block-wrapper', 'hljs', 'katex-ignore', 'mermaid-viewport'],
              ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'svg'],
              throwOnError: false
            });
          }
        } else {
          setTimeout(initKatex, 100);
        }
      }
      initKatex();
    });
  </script>
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to content</a>
  <div id="progress-bar" class="reading-progress"></div>

  <!-- Top Navigation Header -->
  <header class="top-nav" role="banner">
    <button id="menu-btn" class="btn-menu" aria-label="Open chapter menu" aria-controls="chapter-nav" aria-expanded="false" title="Chapters"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="18" x2="21" y2="18"></line></svg></button>
    <a href="${rootRel}/index.html" class="brand">
      <span class="brand-badge">PBC 2026</span>
      <span>Master Preparation Guide</span>
    </a>
    <div class="header-controls">
      <div class="progress-stat-badge" title="Master Curriculum Progress">
        <span id="header-progress-text">0/${ALL_CHAPTERS.length} (0%)</span>
        <div class="progress-mini-bar"><div class="progress-mini-fill" id="header-progress-bar"></div></div>
      </div>
      <button id="header-mark-read-btn" class="btn-mark-read" onclick="toggleCurrentChapterRead()" title="Toggle Read Status">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"></circle></svg>
        <span>Mark as Read</span>
      </button>
      <div class="search-input-wrap">
        <svg class="search-icon" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>
        <input type="search" class="search-input" aria-label="Search all chapters" placeholder="Search all chapters ( / )" autocomplete="off" oninput="filterNav(this.value)">
        <div id="search-results" class="search-results" role="listbox" aria-label="Search results" hidden></div>
      </div>
      <a href="${pdfHref}" class="btn-pdf" target="_blank" title="Open compiled print PDF">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
        <span>Open PDF</span>
      </a>
      <button class="btn-icon" onclick="toggleTheme()" title="Toggle Dark/Light Mode">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>
      </button>
    </div>
  </header>

  <div class="app-container">
    <!-- Left Navigation Sidebar -->
    <nav class="sidebar" id="chapter-nav" aria-label="Chapters">
      ${sidebarHtml}
    </nav>
    <div id="nav-overlay" class="nav-overlay"></div>

    <!-- Main Content Reader -->
    <main class="main-wrapper" id="main-content" tabindex="-1">
      <div class="content-container">
        <article class="markdown-body">
          ${bodyHtml}
        </article>
        <div class="bottom-completion-wrap">
          <button id="bottom-mark-read-btn" class="btn-mark-read btn-mark-read-large" onclick="toggleCurrentChapterRead()">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"></circle></svg>
            <span>Mark as Read</span>
          </button>
        </div>
        ${navHtml}
      </div>
    </main>

    <!-- Right Table of Contents -->
    <aside class="toc-sidebar" aria-label="On this page">
      ${tocHtml}
    </aside>
  </div>

  <!-- High-Resolution Fullscreen Diagram & Image Modal -->
  <div id="pv-modal" class="pv-modal" onclick="closePvModal(event)">
    <div class="pv-modal-card" onclick="event.stopPropagation()">
      <div class="pv-modal-header">
        <span class="pv-modal-title">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
          <span id="pv-modal-title-text">High-Resolution Architecture Viewer</span>
        </span>
        <div class="pv-modal-tools">
          <button class="pv-btn" onclick="modalZoomStep(-0.25)" title="Zoom Out (-)">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="8" y1="11" x2="14" y2="11"></line></svg>
          </button>
          <span id="pv-zoom-val" class="pv-zoom-val">100%</span>
          <button class="pv-btn" onclick="modalZoomStep(0.25)" title="Zoom In (+)">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"></circle><line x1="11" y1="8" x2="11" y2="14"></line><line x1="8" y1="11" x2="14" y2="11"></line></svg>
          </button>
          <button class="pv-btn" onclick="modalReset()" title="Reset to Fit (100%)">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8"></path><polyline points="3 3 3 8 8 8"></polyline></svg>
          </button>
          <button class="pv-close-btn" onclick="closePvModal()" title="Close Viewer (Esc)">&times;</button>
        </div>
      </div>
      <div class="pv-modal-viewport" id="pv-modal-viewport">
        <div id="pv-modal-content" class="pv-modal-content"></div>
      </div>
    </div>
  </div>

  <script>window.CURRENT_PAGE = "${currentChapter.relHtml}";</script>
  <script>${PORTAL_JS}</script>
</body>
</html>`;
}

// Protect math ($...$ and $$...$$) from markdown processing (marked would eat backslash-underscore and backslash-dollar)
function protectMath(md) {
  const store = [];
  const re = /(```[\s\S]*?```|`[^`\n]+`)|(\$\$(?:\\.|[^$\\])+?\$\$)|(\$(?:\\.|[^$\\\n])+?\$)|(\\\$)/g;
  const out = md.replace(re, (m, code, disp, inl, esc) => {
    if (code || esc) return m;
    store.push(m);
    return '@@MATH' + (store.length - 1) + '@@';
  });
  return { md: out, store };
}
function restoreMath(html, store) {
  return html.replace(/@@MATH(\d+)@@/g, (m, i) => store[+i].replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'));
}

// Compile all chapters
function buildAllHtml() {
  console.log(`Starting Interactive HTML Portal Build for ${ALL_CHAPTERS.length} Books...`);

  // Ensure assets directory exists in output
  const outAssets = path.join(HTML_OUT_DIR, 'assets');
  if (!fs.existsSync(outAssets)) {
    fs.mkdirSync(outAssets, { recursive: true });
  }

  // Copy local mermaid.min.js to html/assets
  const srcMermaid = path.join(ASSETS_DIR, 'mermaid.min.js');
  const destMermaid = path.join(outAssets, 'mermaid.min.js');
  if (fs.existsSync(srcMermaid)) {
    fs.copyFileSync(srcMermaid, destMermaid);
    console.log(`  -> Copied offline mermaid.min.js to html/assets/`);
  }

  // Vendor KaTeX (offline): css + js + auto-render + fonts
  const kSrc = path.resolve(ROOT_DIR, 'node_modules', 'katex', 'dist');
  const kDst = path.join(outAssets, 'katex');
  if (fs.existsSync(kSrc)) {
    fs.mkdirSync(path.join(kDst, 'fonts'), { recursive: true });
    fs.copyFileSync(path.join(kSrc, 'katex.min.css'), path.join(kDst, 'katex.min.css'));
    fs.copyFileSync(path.join(kSrc, 'katex.min.js'), path.join(kDst, 'katex.min.js'));
    fs.copyFileSync(path.join(kSrc, 'contrib', 'auto-render.min.js'), path.join(kDst, 'auto-render.min.js'));
    fs.readdirSync(path.join(kSrc, 'fonts')).filter(f => f.endsWith('.woff2')).forEach(f =>
      fs.copyFileSync(path.join(kSrc, 'fonts', f), path.join(kDst, 'fonts', f)));
    console.log('  -> Vendored KaTeX into html/assets/katex/');
  }

  const searchIndex = [];
  let count = 0;
  ALL_CHAPTERS.forEach(chapter => {
    const srcMdPath = path.resolve(ROOT_DIR, chapter.relMd);
    if (!fs.existsSync(srcMdPath)) {
      console.warn(`  [MISSING] ${srcMdPath}`);
      return;
    }

    const rawMd = fs.readFileSync(srcMdPath, 'utf8');
    const pm = protectMath(rawMd);
    let parsedHtml = restoreMath(marked.parse(pm.md), pm.store);
    parsedHtml = transformCallouts(parsedHtml);

    // Transform internal markdown links to HTML links
    parsedHtml = parsedHtml.replace(/href="([^":]+?)\.md(#?[^"]*)"/g, (match, p1, p2) => {
      if (p1 === 'README') return `href="index.html${p2}"`;
      return `href="${p1}.html${p2}"`;
    });

    const tocItems = extractTOC(parsedHtml);
    const fullPageHtml = buildPageHtml(chapter, parsedHtml, tocItems);
    const destHtmlPath = path.resolve(HTML_OUT_DIR, chapter.relHtml);

    const destDir = path.dirname(destHtmlPath);
    if (!fs.existsSync(destDir)) {
      fs.mkdirSync(destDir, { recursive: true });
    }

    fs.writeFileSync(destHtmlPath, fullPageHtml, 'utf8');
    count++;

    // Section-level full-text index for client-side search
    const plain = h => h.replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/g, ' ').replace(/<[^>]+>/g, ' ')
      .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;/g, "'")
      .replace(/\s+/g, ' ').trim();
    const parts = parsedHtml.split(/(?=<h[23]\s+id=")/);
    const secs = [];
    parts.forEach((part, i) => {
      const m = /^<h[23]\s+id="([^"]+)">.*?<\/a>(.*?)<\/h[23]>/s.exec(part);
      const text = plain(part).toLowerCase().slice(0, 6000);
      if (m) secs.push({ id: m[1], h: plain(m[2]), x: text });
      else if (i === 0 && text) secs.push({ id: '', h: chapter.label, x: text });
    });
    searchIndex.push({ u: chapter.relHtml, t: chapter.label, s: secs });
  });

  fs.writeFileSync(path.join(outAssets, 'search-index.js'), 'window.SEARCH_INDEX=' + JSON.stringify(searchIndex) + ';', 'utf8');
  console.log('  -> Wrote full-text search index (' + searchIndex.length + ' chapters)');

  // Also create a copy of README.html as index.html in the html directory
  const readmeHtml = path.resolve(HTML_OUT_DIR, 'README.html');
  const indexHtml = path.resolve(HTML_OUT_DIR, 'index.html');
  if (fs.existsSync(readmeHtml)) {
    fs.copyFileSync(readmeHtml, indexHtml);
    console.log(`  -> Created master entry point: html/index.html`);
  }

  console.log(`Successfully compiled ${count} Interactive HTML books in ${HTML_OUT_DIR}!`);
}

buildAllHtml();
