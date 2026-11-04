"""Orchestrated Saga Execution Engine for Multi-Step Distributed Workflows.

Architectural Context:
----------------------
In microservice architectures, distributed transactions across heterogeneous databases
cannot rely on 2PC (Two-Phase Commit) due to blocking latency, coordinator single points
of failure, and lack of XA support in modern NoSQL/Cloud stores.

The Saga Pattern:
-----------------
A Saga is a sequence of local transactions:
- Each step T_i executes a local transaction in Service_i.
- If step T_k fails: the orchestrator executes compensating transactions
  C_{k-1}, C_{k-2}, ..., C_1 in reverse order to semantically undo preceding side effects.
- Guaranteed properties:
  1. Forward idempotent execution
  2. Durable state logging for failure recovery
  3. Reverse compensation ordering
  4. Transient retry with backoff before aborting
"""

from __future__ import annotations
import copy
import enum
import logging
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional

logger = logging.getLogger("saga_orchestrator")


class SagaStatus(str, enum.Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    COMPENSATING = "COMPENSATING"
    COMPENSATED = "COMPENSATED"
    FAILED = "FAILED"


@dataclass
class SagaLogEntry:
    timestamp: float
    saga_id: str
    step_name: str
    action_type: str  # "FORWARD" or "COMPENSATION"
    status: str       # "STARTED", "COMPLETED", "FAILED"
    payload: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@dataclass
class SagaContext:
    saga_id: str
    payload: Dict[str, Any]
    step_results: Dict[str, Any] = field(default_factory=dict)
    compensations_run: List[str] = field(default_factory=list)


@dataclass
class SagaResult:
    saga_id: str
    status: SagaStatus
    step_results: Dict[str, Any]
    error: Optional[str] = None
    execution_log: List[SagaLogEntry] = field(default_factory=list)


class SagaStep:
    """Definition of an individual Saga step with its forward action and compensating rollback action."""

    def __init__(
        self,
        name: str,
        forward_action: Callable[[SagaContext], Any],
        compensating_action: Optional[Callable[[SagaContext], Any]] = None,
        max_retries: int = 0,
        retry_delay_seconds: float = 0.05,
    ) -> None:
        self.name = name
        self.forward_action = forward_action
        self.compensating_action = compensating_action or (lambda ctx: None)
        self.max_retries = max_retries
        self.retry_delay_seconds = retry_delay_seconds


class SagaOrchestrator:
    """Production-grade orchestrator executing steps and reverse compensations."""

    def __init__(self, name: str = "OrderSaga") -> None:
        self.name = name
        self.steps: List[SagaStep] = []
        self._lock = threading.Lock()
        self.execution_logs: Dict[str, List[SagaLogEntry]] = {}

    def add_step(self, step: SagaStep) -> SagaOrchestrator:
        self.steps.append(step)
        return self

    def _log(
        self,
        saga_id: str,
        step_name: str,
        action_type: str,
        status: str,
        payload: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ) -> None:
        entry = SagaLogEntry(
            timestamp=time.time(),
            saga_id=saga_id,
            step_name=step_name,
            action_type=action_type,
            status=status,
            payload=copy.deepcopy(payload) if payload else None,
            error=error,
        )
        with self._lock:
            if saga_id not in self.execution_logs:
                self.execution_logs[saga_id] = []
            self.execution_logs[saga_id].append(entry)

    def execute(
        self,
        initial_payload: Dict[str, Any],
        saga_id: Optional[str] = None,
    ) -> SagaResult:
        """Executes saga steps sequentially; executes compensations in reverse on failure."""
        if not saga_id:
            saga_id = str(uuid.uuid4())

        context = SagaContext(
            saga_id=saga_id,
            payload=copy.deepcopy(initial_payload),
        )

        completed_steps: List[SagaStep] = []
        failed_step: Optional[SagaStep] = None
        failure_exception: Optional[Exception] = None

        self._log(saga_id, "SAGA", "ORCHESTRATOR", SagaStatus.IN_PROGRESS)

        # 1. Forward Execution Phase
        for step in self.steps:
            attempt = 0
            step_success = False
            last_err = None

            while attempt <= step.max_retries:
                try:
                    self._log(saga_id, step.name, "FORWARD", "STARTED")
                    result = step.forward_action(context)
                    context.step_results[step.name] = result
                    self._log(saga_id, step.name, "FORWARD", "COMPLETED")
                    completed_steps.append(step)
                    step_success = True
                    break
                except Exception as ex:
                    last_err = ex
                    attempt += 1
                    self._log(
                        saga_id,
                        step.name,
                        "FORWARD",
                        "ATTEMPT_FAILED",
                        error=str(ex),
                    )
                    if attempt <= step.max_retries:
                        time.sleep(step.retry_delay_seconds)

            if not step_success:
                failed_step = step
                failure_exception = last_err
                self._log(
                    saga_id,
                    step.name,
                    "FORWARD",
                    "FAILED",
                    error=str(last_err),
                )
                break

        # 2. If all steps completed successfully
        if failed_step is None:
            self._log(saga_id, "SAGA", "ORCHESTRATOR", SagaStatus.COMPLETED)
            return SagaResult(
                saga_id=saga_id,
                status=SagaStatus.COMPLETED,
                step_results=context.step_results,
                execution_log=self.execution_logs[saga_id],
            )

        # 3. Compensation Phase (Reverse Order)
        self._log(
            saga_id,
            "SAGA",
            "ORCHESTRATOR",
            SagaStatus.COMPENSATING,
            error=str(failure_exception),
        )

        compensation_failures: List[str] = []

        # Compensate completed steps in reverse: k-1 down to 1
        for step in reversed(completed_steps):
            try:
                self._log(saga_id, step.name, "COMPENSATION", "STARTED")
                step.compensating_action(context)
                context.compensations_run.append(step.name)
                self._log(saga_id, step.name, "COMPENSATION", "COMPLETED")
            except Exception as comp_ex:
                compensation_failures.append(f"{step.name}: {str(comp_ex)}")
                self._log(
                    saga_id,
                    step.name,
                    "COMPENSATION",
                    "FAILED",
                    error=str(comp_ex),
                )

        final_status = (
            SagaStatus.COMPENSATED if not compensation_failures else SagaStatus.FAILED
        )
        self._log(saga_id, "SAGA", "ORCHESTRATOR", final_status)

        err_msg = f"Step '{failed_step.name}' failed: {failure_exception}"
        if compensation_failures:
            err_msg += f" | Compensations failed: {'; '.join(compensation_failures)}"

        return SagaResult(
            saga_id=saga_id,
            status=final_status,
            step_results=context.step_results,
            error=err_msg,
            execution_log=self.execution_logs[saga_id],
        )
