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


def test_agent_rag_fail_closed_on_rebac_unavailability():
    """Fail-Closed Security Guarantee:
    If Zanzibar authorization service is unavailable, all retrieved chunks must be DENIED.
    Never leak unauthorized chunks into the LLM context!
    """
    engine = AgentRAGEngine()
    chunk = DocumentChunk(
        chunk_id="chunk_secret",
        doc_id="secret_payroll",
        content="CEO salary and executive bonus structures.",
        embedding=[1.0, 0.0],
    )
    engine.index_chunk(chunk)
    engine.grant_document_access("secret_payroll", "viewer", "user:alice")

    # Simulate ReBAC authorization service outage
    engine.zanzibar.is_available = False

    req = AgentQueryRequest(
        user_id="user:alice",
        query="salary bonus",
        query_embedding=[1.0, 0.0],
        top_k=1,
        execute_tools=False,
    )
    res = engine.query(req)

    # Fail closed: Alice is denied even though tuple exists, because service is unavailable
    assert len(res.authorized_chunks) == 0
    assert res.filtered_chunks_count == 1
    assert "No authorized context found" in res.generated_answer


def test_cross_tenant_isolation():
    """Verify complete isolation between multi-tenant documents."""
    engine = AgentRAGEngine()

    # Tenant A doc
    chunk_a = DocumentChunk(
        chunk_id="tenant_a_doc1",
        doc_id="doc_tenant_a",
        content="Acme Corp proprietary strategy.",
        embedding=[1.0, 0.0],
    )
    # Tenant B doc
    chunk_b = DocumentChunk(
        chunk_id="tenant_b_doc1",
        doc_id="doc_tenant_b",
        content="Beta Corp confidential roadmap.",
        embedding=[0.95, 0.05],
    )
    engine.index_chunk(chunk_a)
    engine.index_chunk(chunk_b)

    engine.grant_document_access("doc_tenant_a", "viewer", "user:acme_user")
    engine.grant_document_access("doc_tenant_b", "viewer", "user:beta_user")

    # Acme user query
    res_acme = engine.query(
        AgentQueryRequest(
            user_id="user:acme_user",
            query="strategy and roadmap",
            query_embedding=[1.0, 0.0],
            top_k=5,
            execute_tools=False,
        )
    )
    acme_chunk_ids = [c.doc_id for c in res_acme.authorized_chunks]
    assert "tenant_a_doc1" in acme_chunk_ids
    assert "tenant_b_doc1" not in acme_chunk_ids

    # Beta user query
    res_beta = engine.query(
        AgentQueryRequest(
            user_id="user:beta_user",
            query="strategy and roadmap",
            query_embedding=[1.0, 0.0],
            top_k=5,
            execute_tools=False,
        )
    )
    beta_chunk_ids = [c.doc_id for c in res_beta.authorized_chunks]
    assert "tenant_b_doc1" in beta_chunk_ids
    assert "tenant_a_doc1" not in beta_chunk_ids


def test_revoked_permissions_immediate_effect():
    """Revoking access tuple immediately prevents chunk retrieval."""
    engine = AgentRAGEngine()
    chunk = DocumentChunk(
        chunk_id="chunk_patent",
        doc_id="patent_pending",
        content="Quantum resistance cryptographic algorithm details.",
        embedding=[1.0, 0.0],
    )
    engine.index_chunk(chunk)
    engine.grant_document_access("patent_pending", "viewer", "user:contractor")

    # 1st query: contractor has access
    res1 = engine.query(
        AgentQueryRequest(
            user_id="user:contractor",
            query="quantum algorithm",
            query_embedding=[1.0, 0.0],
            top_k=1,
            execute_tools=False,
        )
    )
    assert len(res1.authorized_chunks) == 1

    # Revoke access
    engine.revoke_document_access("patent_pending", "viewer", "user:contractor")

    # 2nd query: contractor access is immediately denied
    res2 = engine.query(
        AgentQueryRequest(
            user_id="user:contractor",
            query="quantum algorithm",
            query_embedding=[1.0, 0.0],
            top_k=1,
            execute_tools=False,
        )
    )
    assert len(res2.authorized_chunks) == 0
    assert res2.filtered_chunks_count == 1


def test_nested_group_membership_authorization():
    """Verify transitive group membership resolution:
    doc -> group:global_eng#member -> group:core_infra#member -> user:dave
    """
    engine = AgentRAGEngine()
    from ch24_zanzibar_rebac.zanzibar_rebac import RelationTuple

    chunk = DocumentChunk(
        chunk_id="chunk_k8s",
        doc_id="infra_architecture",
        content="Global Kubernetes control plane runbook.",
        embedding=[1.0, 0.0],
    )
    engine.index_chunk(chunk)

    # Document visible to global_eng
    engine.grant_document_access("infra_architecture", "viewer", "group:global_eng#member")
    # core_infra is a member of global_eng
    engine.zanzibar.write_tuple(RelationTuple("group", "global_eng", "member", "group:core_infra#member"))
    # Dave is member of core_infra
    engine.zanzibar.write_tuple(RelationTuple("group", "core_infra", "member", "user:dave"))

    # Dave queries -> authorized via nested group expansion
    res_dave = engine.query(
        AgentQueryRequest(
            user_id="user:dave",
            query="kubernetes runbook",
            query_embedding=[1.0, 0.0],
            top_k=1,
            execute_tools=False,
        )
    )
    assert len(res_dave.authorized_chunks) == 1

    # Eve queries -> not a member -> denied
    res_eve = engine.query(
        AgentQueryRequest(
            user_id="user:eve",
            query="kubernetes runbook",
            query_embedding=[1.0, 0.0],
            top_k=1,
            execute_tools=False,
        )
    )
    assert len(res_eve.authorized_chunks) == 0


def test_outbox_intent_persisted_before_external_side_effect():
    """Critical Architectural Invariant:
    The tool execution intent MUST be committed to the DB outbox BEFORE invoking external side effects.
    If the external tool raises an exception, the intent record still exists in the outbox!
    """
    engine = AgentRAGEngine()

    def failing_tool(payload):
        raise ConnectionResetError("External payment gateway unreachable")

    engine.register_tool("payment_gateway", failing_tool)

    # Invoking the failing tool
    with pytest.raises(ConnectionResetError):
        engine.dispatch_tool_with_outbox(
            tool_name="payment_gateway",
            tool_input={"amount": 100, "currency": "USD"},
            user_id="user:shopper",
        )

    # Invariant Verification: Outbox table MUST contain the intent record despite the external failure!
    outbox_table = engine.rdbms.outbox_table
    assert len(outbox_table) == 1
    intent_record = next(iter(outbox_table.values()))
    assert intent_record.aggregate_id == "user:shopper"
    assert intent_record.payload["status"] == "INTENT_RECORDED"
    assert intent_record.payload["input"]["amount"] == 100
    assert "idempotency_token" in intent_record.payload

