"""
Implements the Composite Observable pattern to unify multiple subjects into a single
transparent observable node, bridging lower-level sensor data with higher-level displays.
"""

from abc import ABC, abstractmethod
from typing import List


# Subject contract defining registration and notification mechanics
# Observable subject in notification pipeline and request source in notification chain
class ObservableInterface(ABC):
    """
    Defines interface for subjects that maintain observer subscriptions and emit events.
    """

    @abstractmethod
    def subscribe(self, observer: "ObserverInterface") -> None:
        pass

    @abstractmethod
    def unsubscribe(self, observer: "ObserverInterface") -> None:
        pass

    @abstractmethod
    def notify_observers(self, value: int) -> None:
        pass


# Observer contract defining event reception mechanics
# Concrete receiver in subscription model and terminal handler in propagation chain
class ObserverInterface(ABC):
    """
    Defines interface for entities receiving event notifications from subjects.
    """

    @abstractmethod
    def update(self, value: int) -> None:
        pass


# Reusable subject implementation managing subscriber registries
# Base observable component and propagation origin in event dispatch chain
class SimpleObservable(ObservableInterface):
    """
    Provides default subscription management and sequential notification dispatch.
    """

    def __init__(self) -> None:
        self._observers: List[ObserverInterface] = []

    def subscribe(self, observer: ObserverInterface) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def unsubscribe(self, observer: ObserverInterface) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify_observers(self, value: int) -> None:
        for observer in list(self._observers):
            observer.update(value)


# Concrete leaf subject producing discrete sensor data readings
# Leaf subject in composite hierarchy and event producer in notification chain
class Sensor(SimpleObservable):
    """
    Simulates physical sensor state transitions and dispatches observed metrics.
    """

    def change_value(self, value: int) -> None:
        self.notify_observers(value)


# Intermediate composite node propagating observed events across tiers
# Composite node aggregating subjects and intermediate forwarding handler in chain
class SensorBatch(SimpleObservable, ObserverInterface):
    """
    Aggregates notifications from multiple sensor sources and relays them uniformly.

    Trade-offs:
        - Encapsulates sensor cluster topologies while presenting a single observable source.
        - Adds an extra forwarding indirection layer and propagates all source notifications indiscriminately.
    """

    def update(self, value: int) -> None:
        self.notify_observers(value)


# Concrete observer rendering received metric updates
# Leaf observer client and terminal consumer handler in notification chain
class NumericDisplay(ObserverInterface):
    """
    Consumes numeric sensor updates and outputs formatted reading records.
    """

    def __init__(self, name: str) -> None:
        self._name = name

    def update(self, value: int) -> None:
        print(f"[{self._name}] Received value: {value}")


if __name__ == "__main__":
    sensor1 = Sensor()
    sensor2 = Sensor()

    batch = SensorBatch()
    sensor1.subscribe(batch)
    sensor2.subscribe(batch)

    display = NumericDisplay("PrimaryDisplay")
    batch.subscribe(display)

    sensor1.change_value(42)
    sensor2.change_value(84)
