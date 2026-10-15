"""
Demonstrates the Disposable Subscription Token pattern in Observer architecture.

Problem: The Lapsed Listener and Strong Coupling Problem
In event-driven architectures, unregistering observers typically faces three design choices:
1. Subject-Centric De-registration (subject.unsubscribe(observer)):
   - Forces the client to maintain persistent references to both Subject and Observer.
   - High coupling; violates Single Responsibility and interface segregation.
2. Observer-Centric De-registration (observer.unsubscribe()):
   - Forces the Observer to either retain Subject references or limits it to a single Subject.
   - Degrades cohesion and breaks multi-subject subscription topologies.
3. Subscription Token Abstraction (Subscription Object):
   - Decouples both parties by introducing a first-class intermediate lifecycle token.
   - The token acts as an associative entity encapsulating an idempotent unregistration closure.

Memory Leak (Lapsed Listener) Vector:
    Subjects retain strong references to registered observers. Discarding observer
    references without explicit unregistration causes cumulative memory leaks, as the
    garbage collector is prevented from reclaiming unreachable listener instances.

Solution: Subscription Token (Disposable) Protocol
Instead of returning None, subscribe() yields a Subscription token implementing
deterministic cleanup and Python context management protocols (__enter__ / __exit__).

Pros:
    - Decouples unregistration mechanics completely from subject and observer identities.
    - Enables scoped temporary subscriptions using 'with' context manager blocks.
    - Guarantees idempotent disposal, safely ignoring redundant unregister calls.
    - Breaks reference retention cycles by nullifying closures upon disposal.

Cons:
    - Incurs a lightweight intermediate object allocation per subscription.
    - Requires callers to retain the token when managing non-scoped lifecycles.

Trade-offs
    Trades minor per-subscription allocation overhead for strict lifecycle safety,
    deterministic memory reclamation, and decoupled architectural boundaries.
"""


"""
Relational Algebra Perspective:
    1. Relationship Topology:
       Models subscriptions as an explicit many-to-many (M:N) relation between
       Subject and Observer domains, avoiding hard coupling across boundaries.

    2. Associative Entity (Join Table):
       The Subscription token materializes this link as an independent entity,
       converting implicit behavioral dependencies into a discrete relation record.

    3. Deterministic Lifecycle:
       Disposal directly mirrors tuple deletion in relational algebra, enabling
       isolated, idempotent lifecycle management without leaking domain references.
"""


from abc import ABC, abstractmethod
from typing import Callable, List, Optional


# Declares contract for subscription disposal and context management.
# Subscription Token Interface
class SubscriptionInterface(ABC):
    """
    Contract for managing subscription lifecycle and cleanup.

    Trade-offs
        Adds an intermediate token allocation per subscription,
        yet decouples unregistration from direct subject reference.
    """

    @abstractmethod
    def dispose(self) -> None:
        pass

    @abstractmethod
    def __enter__(self) -> "SubscriptionInterface":
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        pass


# Manages unregistration callback and context manager lifecycle.
# Concrete Subscription Token Component
class Subscription(SubscriptionInterface):
    """
    Encapsulates unregistration hook and prevents memory leaks via disposal.

    Trade-offs
        Requires careful reference cleanup inside dispose to avoid retention cycles.
    """

    def __init__(self, unsubscribe_action: Callable[[], None]) -> None:
        self._unsubscribe_action: Optional[Callable[[], None]] = unsubscribe_action
        self._is_disposed: bool = False

    def dispose(self) -> None:
        if self._is_disposed:
            return
        if self._unsubscribe_action is not None:
            self._unsubscribe_action()
            self._unsubscribe_action = None
        self._is_disposed = True

    def __enter__(self) -> "SubscriptionInterface":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.dispose()


# Declares contract for registering subscribers and exposing pull query state.
# Subject Interface
class PublisherInterface(ABC):
    """
    Contract for publishers managing subscribers and exposing pull query state.
    """

    @abstractmethod
    def subscribe(self, subscriber: "SubscriberInterface") -> SubscriptionInterface:
        pass

    @abstractmethod
    def notify_subscribers(self) -> None:
        pass

    @property
    @abstractmethod
    def latest_not_notified(self) -> List[str]:
        pass


# Implements reusable subscriber registration and subscription token generation.
# Simple Observable Base Component
class SimpleObservable(ABC):
    """
    Encapsulates subscriber management logic using disposable tokens.

    Trade-offs
        Subclasses inherit clean subscription hooks but manage notification states.
    """

    def __init__(self) -> None:
        self._subscribers: List["SubscriberInterface"] = []

    def subscribe(self, subscriber: "SubscriberInterface") -> SubscriptionInterface:
        self._subscribers.append(subscriber)

        def unsubscribe() -> None:
            if subscriber in self._subscribers:
                self._subscribers.remove(subscriber)

        return Subscription(unsubscribe)

    def notify_subscribers(self) -> None:
        for subscriber in self._subscribers:
            subscriber.update(self)

    @property
    def subscribers(self) -> List[str]:
        return [type(s).__name__ for s in self._subscribers]


# Manages published books and provides state query for pulling observers.
# Concrete Subject Component
class PublisherBook(SimpleObservable, PublisherInterface):
    """
    Book publisher notifying registered subscribers with subject reference.
    """

    def __init__(self) -> None:
        super().__init__()
        self._latest_books: List[str] = []
        self._all_books: List[str] = []

    def notify_subscribers(self) -> None:
        super().notify_subscribers()
        self._clear_latest_books()

    def _clear_latest_books(self) -> None:
        self._latest_books = []

    def add_book(self, book: str) -> None:
        self._all_books.append(book)
        self._latest_books.append(book)

    @property
    def all_books(self) -> List[str]:
        return self._all_books

    @property
    def latest_not_notified(self) -> List[str]:
        return self._latest_books


# Declares observer contract receiving subject reference to pull state.
# Observer Interface
class SubscriberInterface(ABC):
    """
    Subscriber interface receiving the publisher reference to query updates.
    """

    @abstractmethod
    def update(self, subject: PublisherInterface) -> None:
        pass


# Receives publisher reference and pulls latest books for SMS delivery.
# Concrete Observer Component
class SMSSubscriber(SubscriberInterface):
    """
    SMS delivery subscriber pulling latest unnotified entries from subject.
    """

    def update(self, subject: PublisherInterface) -> None:
        publisher = type(subject).__name__
        subscriber = type(self).__name__
        print(f'Update from "{publisher}" to "{subscriber}":')
        print(subject.latest_not_notified, "\n")


# Receives publisher reference and pulls latest books for Email delivery.
# Concrete Observer Component
class EmailSubscriber(SubscriberInterface):
    """
    Email delivery subscriber pulling latest unnotified entries from subject.
    """

    def update(self, subject: PublisherInterface) -> None:
        publisher = type(subject).__name__
        subscriber = type(self).__name__
        print(f'Update from "{publisher}" to "{subscriber}":')
        print(subject.latest_not_notified, "\n")


if __name__ == "__main__":
    sms_subscriber = SMSSubscriber()
    email_subscriber = EmailSubscriber()

    publisher_book = PublisherBook()

    # Permanent subscription using token disposal
    token_email = publisher_book.subscribe(email_subscriber)
    print("Subscribers after email subscribe:", publisher_book.subscribers)

    publisher_book.add_book("Python Architecture")
    publisher_book.notify_subscribers()

    # Manual disposal via token
    token_email.dispose()
    print("Subscribers after manual token disposal:", publisher_book.subscribers)

    publisher_book.add_book("Clean Architecture")
    publisher_book.notify_subscribers()

    # Temporary subscription using Context Manager
    print("Entering context manager block for SMS subscriber...")
    with publisher_book.subscribe(sms_subscriber):
        print("Subscribers inside context:", publisher_book.subscribers)
        publisher_book.add_book("Domain-Driven Design")
        publisher_book.notify_subscribers()

    print("Exited context manager block.")
    print("Subscribers outside context:", publisher_book.subscribers)

    publisher_book.add_book("Enterprise Patterns")
    publisher_book.notify_subscribers()
