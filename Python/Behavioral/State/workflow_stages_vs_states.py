"""
Models a workflow pipeline using stages and steps, kept separate from domain states.

State
    A domain state is a stable business classification owned by the aggregate.
    It describes what the aggregate is right now in business terms, independent of how it got there.
    A state is not a pipeline, not an execution plan, and not a checklist.

Stage
    A stage is an execution boundary inside a workflow pipeline representing a single operational leg.
    A stage groups related verification work so that the pipeline remains readable and changeable.
    A stage is not a domain state; it is a processing unit that can succeed or fail for a given context.

Step
    A step is the smallest executable verification unit in the pipeline belonging to a stage.
    A step reads input from the context and returns a boolean outcome.
    A step must not mutate the domain model; it is intended to be decision logic, not state transition logic.

Differences
    States are business classifications owned by the aggregate.
    Stages and steps are processing structure owned by the workflow.
    A state change may be triggered by a workflow outcome, but the workflow itself is not the state model.

Ownership and placement
    The context belongs to the domain layer and represents the data required for decisions.
    The workflow reads the context and produces a result.
    Demo wiring in __main__ should construct the domain context and run the workflow, but the context type itself
    must not live inside the demo block.

Invariants
    Money values are represented with Decimal.
    Monetary values used for decision making must be non-negative.

Trade-offs:
    - Separating workflow structure from domain states improves clarity and avoids state type explosion,
      but it adds an extra modeling dimension that must be kept consistent with the aggregate's transitions.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Iterable, List


class StateInterface(ABC):
    """
    Contract for domain states describing stable business classifications.
    """

    @abstractmethod
    def id(self) -> str:
        """Return state identifier string."""
        raise NotImplementedError

    @abstractmethod
    def handle_stage_completion(self, context: Context, stage_name: str, success: bool) -> None:
        """Process stage execution outcome."""
        raise NotImplementedError

    @abstractmethod
    def handle_applicant_confirmation(self, context: Context) -> None:
        """Process applicant confirmation request."""
        raise NotImplementedError


# Concrete State
class InitialState(StateInterface):
    """
    Domain state indicating the loan application is newly created.
    """

    def id(self) -> str:
        return "pending"

    def handle_stage_completion(self, context: Context, stage_name: str, success: bool) -> None:
        if not success:
            context.transition_to(RejectedState(stage_name))
            return
        context.record_audit(f"completed_stage:{stage_name}")
        context.transition_to(InternalReviewState())

    def handle_applicant_confirmation(self, context: Context) -> None:
        context.record_audit("ignored_confirmation:before_internal_review")


# Concrete State
class InternalReviewState(StateInterface):
    """
    Domain state indicating the loan application is undergoing internal organizational review.
    """

    def id(self) -> str:
        return "internal_review"

    def handle_stage_completion(self, context: Context, stage_name: str, success: bool) -> None:
        if not success:
            context.transition_to(RejectedState(stage_name))
            return
        context.record_audit(f"subsequent_completed_stage:{stage_name}")

    def handle_applicant_confirmation(self, context: Context) -> None:
        context.record_audit("ignored_confirmation:during_internal_review")


# Concrete State
class ApplicantConfirmationState(StateInterface):
    """
    Domain state indicating internal checks passed and awaiting applicant confirmation.
    """

    def id(self) -> str:
        return "awaiting_applicant_confirmation"

    def handle_stage_completion(self, context: Context, stage_name: str, success: bool) -> None:
        context.record_audit(f"ignored_stage_completion:{stage_name}")

    def handle_applicant_confirmation(self, context: Context) -> None:
        context.record_audit("applicant_confirmed_offer")
        context.transition_to(ApprovedState())


# Concrete State
class ApprovedState(StateInterface):
    """
    Domain state indicating the loan application has successfully passed all stages and confirmation.
    """

    def id(self) -> str:
        return "approved"

    def handle_stage_completion(self, context: Context, stage_name: str, success: bool) -> None:
        pass

    def handle_applicant_confirmation(self, context: Context) -> None:
        pass


# Concrete State
class RejectedState(StateInterface):
    """
    Domain state indicating the loan application failed verification.
    """

    def __init__(self, stage_name: str) -> None:
        self._stage_name = stage_name

    def id(self) -> str:
        return "rejected"

    def handle_stage_completion(self, context: Context, stage_name: str, success: bool) -> None:
        pass

    def handle_applicant_confirmation(self, context: Context) -> None:
        pass


@dataclass
class Context:
    """
    Domain context carrying decision inputs and current domain state for the workflow.
    """

    applicant_score: int
    requested_amount: Decimal
    _state: StateInterface = field(default_factory=InitialState)
    _audit_log: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.applicant_score < 0:
            raise ValueError("applicant_score must be non-negative.")
        if self.requested_amount < Decimal("0"):
            raise ValueError("requested_amount must be non-negative.")

    @property
    def applicant_score_value(self) -> int:
        return self.applicant_score

    @property
    def requested_amount_value(self) -> Decimal:
        return self.requested_amount

    def transition_to(self, new_state: StateInterface) -> None:
        self._state = new_state

    @property
    def state(self) -> StateInterface:
        return self._state

    def record_audit(self, message: str) -> None:
        self._audit_log.append(message)

    @property
    def audit_log(self) -> List[str]:
        return self._audit_log

    def on_stage_completion(self, stage_name: str, success: bool) -> None:
        self._state.handle_stage_completion(self, stage_name, success)

    def on_applicant_confirmation(self) -> None:
        self._state.handle_applicant_confirmation(self)


class StepInterface(ABC):
    """
    Executable decision unit in a stage.
    """

    @abstractmethod
    def execute(self, context: Context) -> bool:
        """Return True when this step passes for the given context."""
        raise NotImplementedError


# Concrete Step
class ExpertApprovalStep(StepInterface):
    """
    Step validating applicant background score against expert criteria.
    """

    def execute(self, context: Context) -> bool:
        return context.applicant_score_value >= 70


# Concrete Step
class FinancialManagerApprovalStep(StepInterface):
    """
    Step validating requested loan amount against financial limits.
    """

    def execute(self, context: Context) -> bool:
        return context.requested_amount_value <= Decimal("50000.00")


class StageInterface(ABC):
    """
    Contract for pipeline execution stages.
    """

    @abstractmethod
    def name(self) -> str:
        """Return stage name identifier."""
        raise NotImplementedError

    @abstractmethod
    def execute(self, context: Context) -> bool:
        """Execute stage verification steps against context."""
        raise NotImplementedError


# Concrete Stage
class VerificationStage(StageInterface):
    """
    Stage executing steps sequentially and producing an overall outcome.
    """

    def __init__(self, steps: Iterable[StepInterface]) -> None:
        self._steps = tuple(steps)

    def name(self) -> str:
        return "verification"

    def execute(self, context: Context) -> bool:
        for step in self._steps:
            if not step.execute(context):
                return False
        return True


if __name__ == "__main__":
    verification_stage = VerificationStage(
        steps=[
            ExpertApprovalStep(),
            FinancialManagerApprovalStep(),
        ],
    )

    # Add (workflow_stages_vs_states_refactored.py) to the project repository for the successful scenario
    successful_context = Context(
        applicant_score=85,
        requested_amount=Decimal("40000.00"),
    )
    success_ok = verification_stage.execute(successful_context)
    successful_context.on_stage_completion(verification_stage.name(), success_ok)
    print("Success Scenario State:", successful_context.state.id())
    print("Success Scenario Audit Log:", successful_context.audit_log)

    # Add (workflow_stages_vs_states_refactored.py) to the project repository for the failed scenario
    failed_context = Context(
        applicant_score=50,
        requested_amount=Decimal("60000.00"),
    )
    fail_ok = verification_stage.execute(failed_context)
    failed_context.on_stage_completion(verification_stage.name(), fail_ok)
    print("Failure Scenario State:", failed_context.state.id())
    print("Failure Scenario Audit Log:", failed_context.audit_log)
