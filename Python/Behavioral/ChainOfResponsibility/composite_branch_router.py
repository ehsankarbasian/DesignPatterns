"""
Hierarchical routing and verification of enterprise invoices across branches.

Composite nodes structure domain-specific verification subtrees while delegating
unmatched documents to successive composite branches along the root chain.

Trade-offs:
    Distributed branch composites eliminate monolithic router bottlenecks and decouple
    domains, but increase the number of coordinating links traversed during processing.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, auto
from typing import List, Optional


# Enterprise document classification determining departmental processing scope.
# Domain Taxonomy / Routing Discriminator
class DocumentCategory(Enum):

    DOMESTIC_OPERATIONAL = auto()
    CROSS_BORDER_IMPORT = auto()
    CAPITAL_EXPENDITURE = auto()


# Lifecycle status indicating verification stage of a processed enterprise document.
# State Indicator / Chain Termination Flag
class VerificationStatus(Enum):

    PENDING = auto()
    APPROVED = auto()
    REJECTED = auto()
    ESCALATED = auto()


# Immutable domain payload representing an enterprise invoice submitted for corporate review.
# Domain Payload / Request Carrier
@dataclass(frozen=True)
class InvoiceDocument:

    document_id: str
    category: DocumentCategory
    gross_amount: Decimal
    requires_customs_clearance: bool


# Stateful transaction carrier tracing verification history and decisions across nodes.
# Execution Context / Traversal Record
@dataclass
class ProcessingContext:

    document: InvoiceDocument
    status: VerificationStatus = VerificationStatus.PENDING
    assigned_handler: Optional[str] = None
    audit_trail: List[str] = None

    def __post_init__(self) -> None:
        if self.audit_trail is None:
            self.audit_trail = []

    def record_step(self, handler_name: str, note: str) -> None:
        self.audit_trail.append(f"{handler_name}: {note}")


# Common contract defining execution interface for leaf verifiers and composite branches.
# Component / Handler
class HandlerInterface(ABC):
    """
    Contract for invoice verification processors in composite chains.

    Trade-offs:
        Enforces uniform processing semantics across leaves and composites,
        but restricts handlers to a single shared execution context signature.
    """

    @abstractmethod
    def handle(self, context: ProcessingContext) -> None:
        pass


# Terminal boundary absorbing unhandled invoices and escalating to executive supervisors.
# Leaf / Terminal Null Object
class NullHandler(HandlerInterface):
    """
    Sentinel terminal escalating unhandled requests to prevent silent drop.

    Trade-offs:
        Eliminates null pointer exceptions and guarantees execution closure,
        but masks configuration oversights if unhandled events are not monitored.
    """

    def handle(self, context: ProcessingContext) -> None:
        if context.status == VerificationStatus.PENDING:
            context.status = VerificationStatus.ESCALATED
            context.record_step(
                "NullHandler",
                "No specialized node handled the invoice; escalated to supervisor.",
            )


# Forwarding base establishing single-link delegation to the next successor in line.
# Leaf / Forwarding Handler
class BaseHandler(HandlerInterface):
    """
    Base handler delegating unhandled requests to a designated successor.

    Trade-offs:
        Encapsulates link traversal mechanics to reduce boilerplate in leaves,
        but introduces implicit chain coupling between neighboring handlers.
    """

    def __init__(self, next_handler: Optional[HandlerInterface] = None) -> None:
        self._next_handler: HandlerInterface = (
            next_handler if next_handler is not None else NullHandler()
        )

    def handle(self, context: ProcessingContext) -> None:
        self._next_handler.handle(context)


# Leaf verifier handling low-value operational domestic expenses within corporate budget limits.
# Leaf / Concrete Handler
class LowValueOperationalApprovalHandler(BaseHandler):
    """
    Approves domestic operational invoices below a predefined threshold.

    Trade-offs:
        Provides rapid automated clearance for frequent low-risk domestic spend,
        but hardcodes threshold invariants that require deployment to reconfigure.
    """

    THRESHOLD: Decimal = Decimal("50000.00")

    def handle(self, context: ProcessingContext) -> None:
        doc = context.document
        if (
            doc.category == DocumentCategory.DOMESTIC_OPERATIONAL
            and doc.gross_amount <= self.THRESHOLD
        ):
            context.status = VerificationStatus.APPROVED
            context.assigned_handler = "LowValueOperationalApprovalHandler"
            context.record_step(
                "LowValueOperationalApprovalHandler",
                f"Auto-approved operational invoice {doc.document_id}.",
            )
            return

        context.record_step(
            "LowValueOperationalApprovalHandler",
            "Threshold or category mismatch; passing downstream.",
        )
        super().handle(context)


# Leaf verifier auditing cross-border compliance prerequisites and customs clearance declarations.
# Leaf / Concrete Handler
class CustomsComplianceHandler(BaseHandler):
    """
    Validates cross-border import invoices for explicit customs clearance declarations.

    Trade-offs:
        Strictly enforces regulatory compliance before financial commitment,
        but introduces binary rejection when clearances are delayed upstream.
    """

    def handle(self, context: ProcessingContext) -> None:
        doc = context.document
        if doc.category == DocumentCategory.CROSS_BORDER_IMPORT:
            if not doc.requires_customs_clearance:
                context.status = VerificationStatus.REJECTED
                context.assigned_handler = "CustomsComplianceHandler"
                context.record_step(
                    "CustomsComplianceHandler",
                    f"Rejected import invoice {doc.document_id} due to missing clearance.",
                )
                return

            context.status = VerificationStatus.APPROVED
            context.assigned_handler = "CustomsComplianceHandler"
            context.record_step(
                "CustomsComplianceHandler",
                f"Approved import invoice {doc.document_id} with customs validation.",
            )
            return

        context.record_step(
            "CustomsComplianceHandler",
            "Non-import invoice; passing downstream.",
        )
        super().handle(context)


# Leaf verifier reviewing capital expenditure requisitions requiring corporate board confirmation.
# Leaf / Concrete Handler
class BoardApprovalHandler(BaseHandler):
    """
    Confirms capital expenditure requisitions requiring executive board sign-off.

    Trade-offs:
        Secures authoritative corporate sign-off for heavy capital assets,
        but acts as a bottleneck requiring specialized downstream handlers.
    """

    def handle(self, context: ProcessingContext) -> None:
        doc = context.document
        if doc.category == DocumentCategory.CAPITAL_EXPENDITURE:
            context.status = VerificationStatus.APPROVED
            context.assigned_handler = "BoardApprovalHandler"
            context.record_step(
                "BoardApprovalHandler",
                f"Board confirmed capital expenditure for {doc.document_id}.",
            )
            return

        context.record_step(
            "BoardApprovalHandler",
            "Non-CapEx invoice; passing downstream.",
        )
        super().handle(context)


# Composite branch managing domestic invoice verifiers and forwarding foreign documents.
# Composite / Branch Handler
class DomesticExpenseComposite(HandlerInterface):
    """
    Manages domestic invoice verifiers and forwards unhandled documents.

    Trade-offs:
        Isolates domestic operational logic within a modular composite branch,
        but introduces multi-level dispatch overhead before reaching fallback.
    """

    def __init__(self, successor: Optional[HandlerInterface] = None) -> None:
        self._internal_chain: List[HandlerInterface] = []
        self._successor: HandlerInterface = (
            successor if successor is not None else NullHandler()
        )

    def add_handler(self, handler: HandlerInterface) -> "DomesticExpenseComposite":
        self._internal_chain.append(handler)
        return self

    def handle(self, context: ProcessingContext) -> None:
        if context.document.category == DocumentCategory.DOMESTIC_OPERATIONAL:
            context.record_step(
                "DomesticExpenseComposite",
                "Routing invoice into domestic evaluation chain.",
            )
            for handler in self._internal_chain:
                handler.handle(context)
                if context.status != VerificationStatus.PENDING:
                    return

        context.record_step(
            "DomesticExpenseComposite",
            "Out of domestic scope or unhandled; delegating to successor branch.",
        )
        self._successor.handle(context)


# Composite branch managing cross-border trade verifiers and forwarding unrelated documents.
# Composite / Branch Handler
class CrossBorderImportComposite(HandlerInterface):
    """
    Manages import verifiers and forwards non-import documents to successors.

    Trade-offs:
        Encapsulates cross-border compliance chains independently from domestic units,
        but adds intermediate traversal hops when handling downstream categories.
    """

    def __init__(self, successor: Optional[HandlerInterface] = None) -> None:
        self._internal_chain: List[HandlerInterface] = []
        self._successor: HandlerInterface = (
            successor if successor is not None else NullHandler()
        )

    def add_handler(self, handler: HandlerInterface) -> "CrossBorderImportComposite":
        self._internal_chain.append(handler)
        return self

    def handle(self, context: ProcessingContext) -> None:
        if context.document.category == DocumentCategory.CROSS_BORDER_IMPORT:
            context.record_step(
                "CrossBorderImportComposite",
                "Routing invoice into customs compliance chain.",
            )
            for handler in self._internal_chain:
                handler.handle(context)
                if context.status != VerificationStatus.PENDING:
                    return

        context.record_step(
            "CrossBorderImportComposite",
            "Out of import scope or unhandled; delegating to successor branch.",
        )
        self._successor.handle(context)


if __name__ == "__main__":
    # Assemble leaf handlers
    domestic_leaf = LowValueOperationalApprovalHandler()
    customs_leaf = CustomsComplianceHandler()
    board_fallback = BoardApprovalHandler()

    # Build distributed composite branches chained sequentially without a centralized router
    import_branch = CrossBorderImportComposite(successor=board_fallback)
    import_branch.add_handler(customs_leaf)

    domestic_branch = DomesticExpenseComposite(successor=import_branch)
    domestic_branch.add_handler(domestic_leaf)

    # Process domestic invoice within threshold
    domestic_invoice = InvoiceDocument(
        document_id="INV-DOM-2026",
        category=DocumentCategory.DOMESTIC_OPERATIONAL,
        gross_amount=Decimal("18200.00"),
        requires_customs_clearance=False,
    )
    ctx_1 = ProcessingContext(document=domestic_invoice)
    domestic_branch.handle(ctx_1)
    print(f"Result 1: Status={ctx_1.status.name}, Handler={ctx_1.assigned_handler}")
    for entry in ctx_1.audit_trail:
        print(f"  -> {entry}")

    # Process import invoice requiring customs validation
    import_invoice = InvoiceDocument(
        document_id="INV-IMP-4091",
        category=DocumentCategory.CROSS_BORDER_IMPORT,
        gross_amount=Decimal("120000.00"),
        requires_customs_clearance=True,
    )
    ctx_2 = ProcessingContext(document=import_invoice)
    domestic_branch.handle(ctx_2)
    print(f"\nResult 2: Status={ctx_2.status.name}, Handler={ctx_2.assigned_handler}")
    for entry in ctx_2.audit_trail:
        print(f"  -> {entry}")
