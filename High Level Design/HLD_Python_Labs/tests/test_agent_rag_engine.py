"""Tests for Enterprise RAG Engine with Authoritative Zanzibar ReBAC & Outbox (Workshop 13)."""
import pytest
from workshop_rag_agents.agent_rag_engine import (
    AgentRAGEngine,
    DocumentChunk,
    AgentQueryRequest,
)


def test_agent_rag_rebac_filtering():
    engine = AgentRAGEngine()

    # Index two documents
    # Doc 1: Confidential Financials
    chunk1 = DocumentChunk(
        chunk_id="chunk_fin_1",
        doc_id="financials_2026",
        content="Confidential revenue projections for Q4 are 50 million.",
        embedding=[1.0, 0.0],
    )
    # Doc 2: Public Engineering Specs
    chunk2 = DocumentChunk(
        chunk_id="chunk_eng_1",
        doc_id="specs_public",
        content="Kubernetes deployment guidelines and cluster configurations.",
        embedding=[0.9, 0.1],
    )

    engine.index_chunk(chunk1)
    engine.index_chunk(chunk2)

    # ReBAC Access Rules:
    # Alice can view both documents
    engine.grant_document_access("financials_2026", "viewer", "user:alice")
    engine.grant_document_access("specs_public", "viewer", "user:alice")

    # Bob can ONLY view public specs, NOT financials!
    engine.grant_document_access("specs_public", "viewer", "user:bob")

    # 1. Alice queries -> Should see both or the financials chunk
    req_alice = AgentQueryRequest(
        user_id="user:alice",
        query="revenue and cluster guidelines",
        query_embedding=[1.0, 0.0],
        top_k=2,
        execute_tools=False,
    )
    res_alice = engine.query(req_alice)
    alice_chunk_ids = [c.doc_id for c in res_alice.authorized_chunks]
    assert "chunk_fin_1" in alice_chunk_ids

    # 2. Bob queries -> Financials chunk MUST be strictly eliminated by Zanzibar!
    req_bob = AgentQueryRequest(
        user_id="user:bob",
        query="revenue and cluster guidelines",
        query_embedding=[1.0, 0.0],
        top_k=2,
        execute_tools=False,
    )
    res_bob = engine.query(req_bob)
    bob_chunk_ids = [c.doc_id for c in res_bob.authorized_chunks]

    # Security check: Bob never sees chunk_fin_1
    assert "chunk_fin_1" not in bob_chunk_ids
    assert "chunk_eng_1" in bob_chunk_ids
    assert res_bob.filtered_chunks_count >= 1


def test_agent_tool_execution_with_transactional_outbox():
    engine = AgentRAGEngine()
    tool_invoked = False

    def audit_tool(payload):
        nonlocal tool_invoked
        tool_invoked = True
        return {"audit_status": "RECORDED"}

    engine.register_tool("audit_log", audit_tool)

    req = AgentQueryRequest(
        user_id="user:auditor",
        query="system health",
        query_embedding=[0.5, 0.5],
        top_k=1,
        execute_tools=True,
    )

    response = engine.query(req)

    assert tool_invoked is True
    assert len(response.tool_executions) == 1
    tool_exec = response.tool_executions[0]
    assert tool_exec.tool_name == "audit_log"
    assert tool_exec.outbox_event_id is not None

    # Verify atomic outbox entry exists in simulated RDBMS
    outbox_table = engine.rdbms.outbox_table
    assert tool_exec.outbox_event_id in outbox_table
    outbox_rec = outbox_table[tool_exec.outbox_event_id]
    assert outbox_rec.event_type == "RAGQueryExecuted"
