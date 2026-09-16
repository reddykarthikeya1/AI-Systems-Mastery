"""Colang Dialogue Flow State Machine and Llama Guard Safety Classifier."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class SafetyAuditResult:
    is_safe: bool
    violated_category: Optional[str] = None
    reason: Optional[str] = None


@dataclass
class FlowResponse:
    action: str  # "RESPOND", "DIVERT", or "DELEGATE_LLM"
    text: Optional[str] = None
    canonical_intent: Optional[str] = None


class LlamaGuardClassifier:
    """Simulates Llama Guard MLCommons hazard classification (S1-S6)."""

    HAZARD_KEYWORDS = {
        "S1": ["bomb", "kill", "assassinate", "violence"],
        "S2": ["steal", "counterfeit", "shoplift"],
        "S3": ["non-consensual", "harassment"],
        "S4": ["csam", "child exploitation"],
        "S5": ["hate speech", "racial slur"],
        "S6": ["ddos attack", "ransomware", "exploit payload", "malware script"],
    }

    def audit(self, text: str) -> SafetyAuditResult:
        """Audits input against S1-S6 taxonomy."""
        text_lower = text.lower()
        for cat, keywords in self.HAZARD_KEYWORDS.items():
            for kw in keywords:
                if kw in text_lower:
                    return SafetyAuditResult(
                        is_safe=False,
                        violated_category=cat,
                        reason=f"Matched hazard pattern '{kw}' under category {cat}",
                    )
        return SafetyAuditResult(is_safe=True)


class NeMoColangEngine:
    """Colang Dialogue State Machine enforcing deterministic dialog flows."""

    def __init__(self) -> None:
        self.llama_guard = LlamaGuardClassifier()
        self.flows: Dict[str, str] = {
            "ask_politics": "I am an enterprise AI assistant. I cannot discuss politics or elections.",
            "ask_medical": "I am not a licensed medical professional. Please consult a physician.",
            "greeting": "Hello! How can I assist your technical team today?",
        }

    def classify_intent(self, text: str) -> str:
        """Extracts canonical intent from natural language."""
        lower = text.lower()
        if any(w in lower for w in ["election", "president", "vote", "senator", "political"]):
            return "ask_politics"
        elif any(w in lower for w in ["symptoms", "diagnose", "prescription", "cure cancer"]):
            return "ask_medical"
        elif any(w in lower for w in ["hello", "hi", "hey", "good morning"]):
            return "greeting"
        return "general_domain_query"

    def process_turn(self, user_text: str) -> FlowResponse:
        """Processes conversational turn through Llama Guard and Colang flows."""
        # Step 1: Llama Guard Safety Audit
        safety = self.llama_guard.audit(user_text)
        if not safety.is_safe:
            return FlowResponse(
                action="RESPOND",
                text=f"Request blocked by safety policy ({safety.violated_category}).",
                canonical_intent="safety_violation",
            )

        # Step 2: Colang Canonical Intent Classification
        intent = self.classify_intent(user_text)

        # Step 3: Flow Routing
        if intent in self.flows:
            return FlowResponse(
                action="DIVERT",
                text=self.flows[intent],
                canonical_intent=intent,
            )

        # Step 4: Delegate to LLM
        return FlowResponse(
            action="DELEGATE_LLM",
            text=None,
            canonical_intent=intent,
        )
