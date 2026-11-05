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
  C_{k-1}, C_{k-2}, ..., C_1 in REVERSE order to semantically undo preceding side effects.

CRITICAL ARCHITECTURAL DISTINCTIONS:
===================================
1. Compensations Are Business Correctives, NOT Mathematical Rollbacks:
   - Preceding transactions have ALREADY committed their local ACID transactions.
   - External systems may have already observed side effects (e.g. credit card charged,
     email receipt dispatched, hotel room reserved).
   - A compensation CANNOT "un-send" an email or undo a database transaction.
   - Instead, a compensation executes an inverse business operation (e.g. issuing a refund,
     dispatching a cancellation email, re-crediting loyalty points).
   - Because networks fail and orchestrators restart, EVERY step and compensation MUST be
     strictly IDEMPOTENT.

2. In-Memory Simulator vs. Production Durable Log:
   - `InMemorySagaLog`: In-memory thread-safe state store used for simulation and unit testing.
   - Production Durable Log: Requires WAL (Write-Ahead Logging) to an ACID SQL or Kafka store
     so an orchestrator crash can resume or compensate active sagas without state loss.

3. Non-Blocking Async Execution:
   - Fully supports asynchronous workflows (`execute_async`) using `asyncio.sleep` to avoid
     blocking the event loop during step or compensation retries.
"""

from __future__ import annotations
import asyncio
import copy
import enum
import logging
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Union

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
    status: str       # "STARTED", "COMPLETED", "FAILED", "ATTEMPT_FAILED"
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
    """Definition of an individual Saga step with forward and compensating actions."""

    def __init__(
        self,
        name: str,
        forward_action: Callable[[SagaContext], Any],
        compensating_action: Optional[Callable[[SagaContext], Any]] = None,
        max_retries: int = 0,
        compensation_retries: int = 2,
        retry_delay_seconds: float = 0.01,
    ) -> None:
        self.name = name
        self.forward_action = forward_action
        self.compensating_action = compensating_action or (lambda ctx: None)
        self.max_retries = max(0, max_retries)
        self.compensation_retries = max(0, compensation_retries)
        self.retry_delay_seconds = max(0.0, retry_delay_seconds)

    @property
    def action(self) -> Callable[[SagaContext], Any]:
        return self.forward_action

    @action.setter
    def action(self, val: Callable[[SagaContext], Any]) -> None:
        self.forward_action = val

    @property
    def compensation(self) -> Callable[[SagaContext], Any]:
        return self.compensating_action

    @compensation.setter
    def compensation(self, val: Callable[[SagaContext], Any]) -> None:
        self.compensating_action = val


class InMemorySagaLog:
    """In-memory thread-safe state log simulator for Sagas."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.logs: Dict[str, List[SagaLogEntry]] = {}

    def log(
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
            if saga_id not in self.logs:
                self.logs[saga_id] = []
            self.logs[saga_id].append(entry)

    def get_log(self, saga_id: str) -> List[SagaLogEntry]:
        with self._lock:
            return list(self.logs.get(saga_id, []))


class SagaOrchestrator:
    """Educational Architecture Simulator & Saga Reference Pattern executing steps and reverse compensations."""

    def __init__(self, name: str = "OrderSaga", log_store: Optional[InMemorySagaLog] = None) -> None:
        self.name = name
        self.steps: List[SagaStep] = []
        self.log_store = log_store or InMemorySagaLog()

    @property
    def execution_logs(self) -> Dict[str, List[SagaLogEntry]]:
        """Backwards compatibility accessor for execution logs."""
        return self.log_store.logs

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
        self.log_store.log(saga_id, step_name, action_type, status, payload=payload, error=error)

    def execute(
        self,
        initial_payload: Dict[str, Any],
        saga_id: Optional[str] = None,
    ) -> SagaResult:
        """Synchronously execute saga steps and reverse compensations."""
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
                    self._log(saga_id, step.name, "FORWARD", "ATTEMPT_FAILED", error=str(ex))
                    if attempt <= step.max_retries and step.retry_delay_seconds > 0:
                        time.sleep(step.retry_delay_seconds)

            if not step_success:
                failed_step = step
                failure_exception = last_err
                self._log(saga_id, step.name, "FORWARD", "FAILED", error=str(last_err))
                break

        # 2. If all steps completed successfully
        if failed_step is None:
            self._log(saga_id, "SAGA", "ORCHESTRATOR", SagaStatus.COMPLETED)
            return SagaResult(
                saga_id=saga_id,
                status=SagaStatus.COMPLETED,
                step_results=context.step_results,
                execution_log=self.log_store.get_log(saga_id),
            )

        # 3. Compensation Phase (Reverse Order with Retry Support)
        self._log(
            saga_id,
            "SAGA",
            "ORCHESTRATOR",
            SagaStatus.COMPENSATING,
            error=str(failure_exception),
        )

        compensation_failures: List[str] = []

        for step in reversed(completed_steps):
            comp_attempt = 0
            comp_success = False
            comp_last_err = None

            while comp_attempt <= step.compensation_retries:
                try:
                    self._log(saga_id, step.name, "COMPENSATION", "STARTED")
                    step.compensating_action(context)
                    context.compensations_run.append(step.name)
                    self._log(saga_id, step.name, "COMPENSATION", "COMPLETED")
                    comp_success = True
                    break
                except Exception as comp_ex:
                    comp_last_err = comp_ex
                    comp_attempt += 1
                    self._log(saga_id, step.name, "COMPENSATION", "ATTEMPT_FAILED", error=str(comp_ex))
                    if comp_attempt <= step.compensation_retries and step.retry_delay_seconds > 0:
                        time.sleep(step.retry_delay_seconds)

            if not comp_success:
                compensation_failures.append(f"{step.name}: {str(comp_last_err)}")
                self._log(saga_id, step.name, "COMPENSATION", "FAILED", error=str(comp_last_err))

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
            execution_log=self.log_store.get_log(saga_id),
        )

    async def execute_async(
        self,
        initial_payload: Dict[str, Any],
        saga_id: Optional[str] = None,
    ) -> SagaResult:
        """Asynchronously execute saga steps with non-blocking asyncio.sleep."""
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
                    action_fn = step.action
                    if asyncio.iscoroutinefunction(action_fn):
                        result = await action_fn(context)
                    else:
                        result = await asyncio.to_thread(action_fn, context)
                    context.step_results[step.name] = result
                    self._log(saga_id, step.name, "FORWARD", "COMPLETED")
                    completed_steps.append(step)
                    step_success = True
                    break
                except Exception as ex:
                    last_err = ex
                    attempt += 1
                    self._log(saga_id, step.name, "FORWARD", "ATTEMPT_FAILED", error=str(ex))
                    if attempt <= step.max_retries and step.retry_delay_seconds > 0:
                        await asyncio.sleep(step.retry_delay_seconds)

            if not step_success:
                failed_step = step
                failure_exception = last_err
                self._log(saga_id, step.name, "FORWARD", "FAILED", error=str(last_err))
                break

        if failed_step is None:
            self._log(saga_id, "SAGA", "ORCHESTRATOR", SagaStatus.COMPLETED)
            return SagaResult(
                saga_id=saga_id,
                status=SagaStatus.COMPLETED,
                step_results=context.step_results,
                execution_log=self.log_store.get_log(saga_id),
            )

        # 2. Compensation Phase
        self._log(
            saga_id,
            "SAGA",
            "ORCHESTRATOR",
            SagaStatus.COMPENSATING,
            error=str(failure_exception),
        )

        compensation_failures: List[str] = []

        for step in reversed(completed_steps):
            comp_attempt = 0
            comp_success = False
            comp_last_err = None

            while comp_attempt <= step.compensation_retries:
                try:
                    self._log(saga_id, step.name, "COMPENSATION", "STARTED")
                    comp_fn = step.compensation
                    if asyncio.iscoroutinefunction(comp_fn):
                        await comp_fn(context)
                    else:
                        await asyncio.to_thread(comp_fn, context)
                    context.compensations_run.append(step.name)
                    self._log(saga_id, step.name, "COMPENSATION", "COMPLETED")
                    comp_success = True
                    break
                except Exception as comp_ex:
                    comp_last_err = comp_ex
                    comp_attempt += 1
                    self._log(saga_id, step.name, "COMPENSATION", "ATTEMPT_FAILED", error=str(comp_ex))
                    if comp_attempt <= step.compensation_retries and step.retry_delay_seconds > 0:
                        await asyncio.sleep(step.retry_delay_seconds)

            if not comp_success:
                compensation_failures.append(f"{step.name}: {str(comp_last_err)}")
                self._log(saga_id, step.name, "COMPENSATION", "FAILED", error=str(comp_last_err))

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
            execution_log=self.log_store.get_log(saga_id),
        )
