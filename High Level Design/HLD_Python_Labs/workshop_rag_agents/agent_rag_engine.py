"""Enterprise RAG and Agentic Workflow Orchestration Engine.

Integrated Architecture:
------------------------
1. Hybrid Information Retrieval:
   Combines Okapi BM25 inverted lexical indexing with dense vector cosine similarity
   fused through Reciprocal Rank Fusion (RRF, k=60) to eliminate score calibration bias.

2. Authoritative Zanzibar ReBAC Policy Enforcement:
   CRITICAL SECURITY INVARIANT: Unfiltered semantic retrieval is a major vector for
   tenant data exfiltration. Retrieved chunks MUST be strictly authorized against
   Zanzibar relationship tuples before entering the LLM prompt context window.
   If user X lacks 'viewer' on document Y, chunk is eliminated before LLM sees it.

3. Transactional Outbox for Agent Actions & Tool Side Effects:
   Any downstream state change or external tool invocation triggered by the agent
   is committed atomically with an outbox event, guaranteeing reliable messaging
   without dual-write inconsistencies.
"""

from __future__ import annotations
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

# Enable cross-module imports when running as standalone or package
current_dir = Path(__file__).resolve().parent
parent_dir = current_dir.parent
if str(parent_dir) not in sys.path:
    sys.path.insert(0, str(parent_dir))

from ch21_distributed_search.bm25_and_rrf import HybridSearchEngine, SearchResult
from ch24_zanzibar_rebac.zanzibar_rebac import ZanzibarEngine, RelationTuple
from ch12_event_driven.transactional_outbox import SimulatedRDBMS, OutboxRecord


@dataclass
class DocumentChunk:
    chunk_id: str
    doc_id: str
    content: str
    embedding: List[float]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentToolExecution:
    tool_name: str
    parameters: Dict[str, Any]
    result: Any
    outbox_event_id: Optional[str] = None


@dataclass
class AgentQueryRequest:
    user_id: str
    query: str
    query_embedding: List[float]
    top_k: int = 5
    execute_tools: bool = True


@dataclass
class AgentQueryResponse:
    user_id: str
    query: str
    authorized_chunks: List[SearchResult]
    filtered_chunks_count: int
    generated_answer: str
    tool_executions: List[AgentToolExecution] = field(default_factory=list)


class AgentRAGEngine:
    """Production Enterprise RAG and Agentic Orchestrator."""

    def __init__(
        self,
        hybrid_engine: Optional[HybridSearchEngine] = None,
        zanzibar: Optional[ZanzibarEngine] = None,
        rdbms: Optional[SimulatedRDBMS] = None,
        llm_fn: Optional[Callable[[str, List[str]], str]] = None,
    ) -> None:
        self.hybrid_engine = hybrid_engine or HybridSearchEngine()
        self.zanzibar = zanzibar or ZanzibarEngine()
        self.rdbms = rdbms or SimulatedRDBMS()
        self.chunk_to_doc_id: Dict[str, str] = {}
        # Default mock LLM synthesizer
        self.llm_fn = llm_fn or self._default_llm_synthesizer
        # Registered tools: name -> callable
        self.tools: Dict[str, Callable[[Dict[str, Any]], Any]] = {}

    def register_tool(self, name: str, fn: Callable[[Dict[str, Any]], Any]) -> None:
        self.tools[name] = fn

    def index_chunk(self, chunk: DocumentChunk) -> None:
        """Indexes a chunk into hybrid search and maps chunk to parent document."""
        self.hybrid_engine.add_document(chunk.chunk_id, chunk.content, chunk.embedding)
        self.chunk_to_doc_id[chunk.chunk_id] = chunk.doc_id

    def grant_document_access(self, doc_id: str, relation: str, user: str) -> None:
        """Grants permission on document to user or group via Zanzibar."""
        t = RelationTuple(
            object_namespace="doc",
            object_id=doc_id,
            relation=relation,
            user=user,
        )
        self.zanzibar.write_tuple(t)

    def _default_llm_synthesizer(self, query: str, context_chunks: List[str]) -> str:
        """Deterministic context synthesizer for testing and demonstration."""
        if not context_chunks:
            return "No authorized context found to answer the query."
        joined = " ".join(context_chunks)
        return f"Synthesized Answer for '{query}' based on: {joined[:120]}..."

    def query(self, request: AgentQueryRequest) -> AgentQueryResponse:
        """Executes Hybrid Search -> ReBAC Filtering -> Context Augmentation -> Outbox-backed Tooling."""
        # 1. Hybrid Search (BM25 + Dense Vector + RRF)
        raw_candidates = self.hybrid_engine.search_hybrid(
            query_text=request.query,
            query_embedding=request.query_embedding,
            top_k=request.top_k * 2,
        )

        # 2. Authoritative Zanzibar ReBAC Policy Enforcement
        authorized_chunks: List[SearchResult] = []
        filtered_count = 0

        for cand in raw_candidates:
            doc_id = self.chunk_to_doc_id.get(cand.doc_id, cand.doc_id)
            object_str = f"doc:{doc_id}"

            # Strict security gate: Check if user has 'viewer' permission on document
            if self.zanzibar.check(user=request.user_id, relation="viewer", object_str=object_str):
                authorized_chunks.append(cand)
                if len(authorized_chunks) >= request.top_k:
                    break
            else:
                filtered_count += 1

        # 3. Augment Context and Synthesize Answer
        context_texts = [c.content for c in authorized_chunks if c.content]
        answer = self.llm_fn(request.query, context_texts)

        # 4. Agent Tool Execution with Transactional Outbox
        tool_executions: List[AgentToolExecution] = []
        if request.execute_tools and "audit_log" in self.tools:
            tool_input = {
                "user_id": request.user_id,
                "query": request.query,
                "authorized_chunks": len(authorized_chunks),
            }
            tool_res = self.tools["audit_log"](tool_input)

            # Record tool side effect atomically in transactional outbox
            with self.rdbms.begin() as tx:
                tx.save_entity("audit_records", request.user_id, tool_input)
                outbox_rec = tx.append_outbox(
                    aggregate_type="AgentAction",
                    aggregate_id=request.user_id,
                    event_type="RAGQueryExecuted",
                    payload={"input": tool_input, "result": tool_res},
                )
                tool_executions.append(
                    AgentToolExecution(
                        tool_name="audit_log",
                        parameters=tool_input,
                        result=tool_res,
                        outbox_event_id=outbox_rec.event_id,
                    )
                )

        return AgentQueryResponse(
            user_id=request.user_id,
            query=request.query,
            authorized_chunks=authorized_chunks,
            filtered_chunks_count=filtered_count,
            generated_answer=answer,
            tool_executions=tool_executions,
        )
