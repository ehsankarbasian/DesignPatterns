"""
Implements an aggregated pull-model observer topology that relays originating subject
references across intermediate layers, enabling downstream consumers to dynamically
identify and query mutated entities within aggregated clusters.

Architectural Context and Push vs. Pull Trade-offs:
    In complex event pipelines, intermediate nodes aggregate multiple discrete subjects
    to present a unified notification boundary. A naive push model transmits raw values
    through these nodes, discarding the originating subject context. Downstream observers
    become oblivious to which specific entity mutated, preventing contextual handling,
    state inspection, and selective processing across heterogeneous subjects.

    Adopting a pull-model protocol where subjects pass their own reference solves this
    architectural limitation by preserving source identity across intermediate layers.

Pros of the Aggregated Pull Model:
    - Source Identity Preservation: Observers inspect the concrete subject directly,
      distinguishing between individual cluster members without centralized routers.
    - Minimal Subject Assumptions: Subjects remain ignorant of consumer data requirements,
      exposing only state queries rather than forcing payload contracts.
    - Selective State Querying: Observers fetch only the attributes pertinent to their
      specific domain concerns, reducing transmission of unused data fields.

Cons of the Aggregated Pull Model:
    - Query Overhead: Requires secondary call invocations back to the subject following
      notification receipt rather than receiving immediate payload data.
    - Type Resolution Coupling: Downstream observers must perform runtime type checks or
      rely on common query interfaces to interact safely with varied subject types.
    - Consistency Vulnerability: Observers depend on the subject remaining internally
      consistent and accessible throughout the duration of the query phase.
"""

from abc import ABC, abstractmethod
from typing import List, Optional


# Observable contract establishing pull notification and registration protocols
# Subject participant in observer hierarchy and event source in notification chain
class ObservableInterface(ABC):
    """
    Defines subscription lifecycle and pull-oriented event dispatch contract.
    """

    @abstractmethod
    def subscribe(self, observer: "ObserverInterface") -> None:
        pass

    @abstractmethod
    def unsubscribe(self, observer: "ObserverInterface") -> None:
        pass

    @abstractmethod
    def notify_observers(self, changed_source: Optional["ObservableInterface"] = None) -> None:
        pass


# Observer contract defining pull consumption signature with subject reference
# Observer participant in event pipeline and terminal consumer in notification chain
class ObserverInterface(ABC):
    """
    Defines event callback interface receiving originating subject reference.
    """

    @abstractmethod
    def update(self, subject: ObservableInterface) -> None:
        pass


# Base observable managing subscriber registries and propagating subject references
# Base observable component in tree topology and dispatcher in responsibility chain
class SimpleObservable(ObservableInterface):
    """
    Maintains subscriber collections and broadcasts originating subject references.
    """

    def __init__(self) -> None:
        self._observers: List[ObserverInterface] = []

    def subscribe(self, observer: ObserverInterface) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: ObserverInterface) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, changed_source: Optional[ObservableInterface] = None) -> None:
        source = changed_source if changed_source is not None else self
        for observer in list(self._observers):
            observer.update(source)


# Discrete leaf subject tracking internal state and broadcasting identity upon modification
# Leaf participant in aggregation hierarchy and source handler in event chain
class Sensor(SimpleObservable):
    """
    Encapsulates physical sensor readings and notifies observers with self reference.

    Trade-offs:
        - Frees sensor from knowing observer payload formatting dependencies.
        - Exposes internal state query properties to external observer inspection.
    """

    def __init__(self, name: str) -> None:
        super().__init__()
        self._name: str = name
        self._value: int = 0

    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> int:
        return self._value

    def change_value(self, value: int) -> None:
        self._value = value
        self.notify_observers(self)


# Aggregating intermediate node observing multiple subjects and forwarding original sources
# Aggregating intermediate node in topology and transparent forwarding handler in chain
class SensorBatch(SimpleObservable, ObserverInterface):
    """
    Aggregates notifications from discrete subjects and relays original source references.

    Trade-offs:
        - Bridges distinct subject scopes without obscuring originating source identity.
        - Adds an indirection hop and forwards notifications without local payload caching.
    """

    def update(self, subject: ObservableInterface) -> None:
        self.notify_observers(changed_source=subject)


# Concrete observer inspecting originating subject instances to format diagnostic output
# Terminal consumer observer and terminal sink handler in notification chain
class NumericDisplay(ObserverInterface):
    """
    Queries concrete subject state dynamically following pull notification dispatch.

    Trade-offs:
        - Discerns exact originating sensor within aggregated batches dynamically.
        - Depends on runtime type introspection to safely query concrete subject APIs.
    """

    def __init__(self, display_id: str) -> None:
        self._display_id: str = display_id

    def update(self, subject: ObservableInterface) -> None:
        if isinstance(subject, Sensor):
            print(f"[{self._display_id}] Sensor '{subject.name}' changed to: {subject.value}")
        else:
            print(f"[{self._display_id}] Received notification from subject: {subject}")


if __name__ == "__main__":
    sensor1 = Sensor("Temperature-Rack-A")
    sensor2 = Sensor("Temperature-Rack-B")

    batch = SensorBatch()
    sensor1.subscribe(batch)
    sensor2.subscribe(batch)

    display = NumericDisplay("MasterConsole")
    batch.subscribe(display)

    sensor1.change_value(26)
    sensor2.change_value(31)
