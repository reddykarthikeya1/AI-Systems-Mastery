"""Educational Architecture Simulator & Reference Pattern: Enterprise RAG and Agentic Workflow Orchestration Engine.

Integrated Architecture & Architectural Guarantees:
----------------------------------------------------
Educational Simulator vs. Production Enterprise Architecture:
- Logical Simulation (This Module):
  Demonstrates secure, tenant-isolated Retrieval-Augmented Generation (RAG) by
  combining hybrid lexical/semantic retrieval (BM25 + Cosine RRF), authoritative
  fail-closed Google Zanzibar ReBAC authorization filtering, and transactional outbox
  intent recording for agentic tool side effects in Python.
- Production Deployment Considerations & Boundaries:
  1. Authoritative ReBAC ACL Evaluation:
     Retrieved chunks are filtered before prompt synthesis. In production, this relies on
     globally distributed Spanner instances with TrueTime snapshot tokens (Zookies) and
     offline reachability indexes (Leopard) rather than live in-memory BFS graph traversals.
  2. Transactional Outbox Tool Execution:
     Tool intent is recorded to durable relational storage with an idempotency token before
     external side effects are dispatched, preventing distributed dual-write inconsistency.
  3. Hybrid Retrieval:
     BM25 inverted index and vector search are fused using Reciprocal Rank Fusion (RRF, k=60).
"""

from __future__ import annotations
import sys
import uuid
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
    """Educational Architecture Simulator & Reference Pattern: Enterprise RAG and Agentic Orchestrator."""

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

    def revoke_document_access(self, doc_id: str, relation: str, user: str) -> None:
        """Revokes permission on document from user or group via Zanzibar."""
        t = RelationTuple(
            object_namespace="doc",
            object_id=doc_id,
            relation=relation,
            user=user,
        )
        self.zanzibar.delete_tuple(t)

    def _default_llm_synthesizer(self, query: str, context_chunks: List[str]) -> str:
        """Deterministic context synthesizer for testing and demonstration."""
        if not context_chunks:
            return "No authorized context found to answer the query."
        joined = " ".join(context_chunks)
        return f"Synthesized Answer for '{query}' based on: {joined[:120]}..."

    def dispatch_tool_with_outbox(
        self, tool_name: str, tool_input: Dict[str, Any], user_id: str
    ) -> AgentToolExecution:
        """Executes a tool with strict transactional outbox sequence:
        
        1. Record Intent in DB Outbox: Commits intent to outbox BEFORE external execution.
        2. Worker Dispatches Tool: Invocations pass idempotency token to target tool.
        3. External Confirmation: External side effect confirms execution.
        4. Record Verified Outcome: Persists verified outcome to entity store and confirms outbox.
        """
        idempotency_token = f"tool_idem_{uuid.uuid4()}"
        intent_payload = {
            "input": dict(tool_input),
            "idempotency_token": idempotency_token,
            "status": "INTENT_RECORDED",
        }

        # Step 1: Record intent in DB outbox BEFORE invoking external side effects
        with self.rdbms.begin() as tx:
            tx.save_entity("tool_intents", idempotency_token, intent_payload)
            outbox_rec = tx.append_outbox(
                aggregate_type="AgentAction",
                aggregate_id=user_id,
                event_type="RAGQueryExecuted",
                payload=intent_payload,
            )

        # Step 2: Worker dispatches tool request with idempotency token
        dispatch_payload = dict(tool_input)
        dispatch_payload["idempotency_token"] = idempotency_token

        # Step 3: External confirmation (invoking external side effect)
        tool_fn = self.tools[tool_name]
        tool_res = tool_fn(dispatch_payload)

        # Step 4: Record verified outcome in DB
        with self.rdbms.begin() as tx:
            tx.save_entity("audit_records", user_id, {
                **tool_input,
                "result": tool_res,
                "idempotency_token": idempotency_token,
                "status": "CONFIRMED",
            })
            with self.rdbms._lock:
                if outbox_rec.event_id in self.rdbms.outbox_table:
                    entry = self.rdbms.outbox_table[outbox_rec.event_id]
                    entry.payload["result"] = tool_res
                    entry.payload["status"] = "CONFIRMED"

        return AgentToolExecution(
            tool_name=tool_name,
            parameters=tool_input,
            result=tool_res,
            outbox_event_id=outbox_rec.event_id,
        )

    def query(self, request: AgentQueryRequest) -> AgentQueryResponse:
        """Executes Hybrid Search -> ReBAC Filtering -> Context Augmentation -> Outbox-backed Tooling."""
        # 1. Hybrid Search (BM25 + Dense Vector + RRF)
        raw_candidates = self.hybrid_engine.search_hybrid(
            query_text=request.query,
            query_embedding=request.query_embedding,
            top_k=request.top_k * 2,
        )

        # 2. Authoritative Fail-Closed Zanzibar ReBAC Policy Enforcement
        authorized_chunks: List[SearchResult] = []
        filtered_count = 0

        for cand in raw_candidates:
            doc_id = self.chunk_to_doc_id.get(cand.doc_id, cand.doc_id)
            object_str = f"doc:{doc_id}"

            # Strict fail-closed security gate:
            # If Zanzibar is down or raises an error, deny access. Never include unauthorized chunks!
            is_authorized = False
            try:
                if self.zanzibar and getattr(self.zanzibar, "is_available", True):
                    is_authorized = self.zanzibar.check(
                        user=request.user_id, relation="viewer", object_str=object_str
                    )
            except Exception:
                is_authorized = False

            if is_authorized:
                authorized_chunks.append(cand)
                if len(authorized_chunks) >= request.top_k:
                    break
            else:
                filtered_count += 1

        # 3. Augment Context and Synthesize Answer
        context_texts = [c.content for c in authorized_chunks if c.content]
        answer = self.llm_fn(request.query, context_texts)

        # 4. Agent Tool Execution with Transactional Outbox (Intent committed before side effects)
        tool_executions: List[AgentToolExecution] = []
        if request.execute_tools and "audit_log" in self.tools:
            tool_input = {
                "user_id": request.user_id,
                "query": request.query,
                "authorized_chunks": len(authorized_chunks),
            }
            exec_record = self.dispatch_tool_with_outbox(
                tool_name="audit_log",
                tool_input=tool_input,
                user_id=request.user_id,
            )
            tool_executions.append(exec_record)

        return AgentQueryResponse(
            user_id=request.user_id,
            query=request.query,
            authorized_chunks=authorized_chunks,
            filtered_chunks_count=filtered_count,
            generated_answer=answer,
            tool_executions=tool_executions,
        )
