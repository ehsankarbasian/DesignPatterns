from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

T = TypeVar("T")


# Defines observer contract accepting pushed state payload directly.
# Target Observer Interface
class ObserverInterface(Generic[T], ABC):
    """
    Abstract subscriber receiving domain state payload directly upon updates.
    """

    @abstractmethod
    def update(self, value: T) -> None:
        pass


# Defines core subscription management and push notification mechanism.
# Simple Observable Base Component
class SimpleObservable(Generic[T]):
    """
    Maintains subscriber collection and broadcasts state changes to registered observers.

    Trade-offs
        Relies on direct synchronous broadcast which blocks the notifier during heavy subscriber execution.
    """

    def __init__(self) -> None:
        self._observers: List[ObserverInterface[T]] = []

    def attach(self, observer: ObserverInterface[T]) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: ObserverInterface[T]) -> None:
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self, value: T) -> None:
        for observer in self._observers:
            observer.update(value)


# Generates temperature measurements and dispatches updates via push mechanics.
# Concrete Subject Component
class Sensor(SimpleObservable[int]):
    """
    Domain sensor component tracking internal temperature and pushing readings to observers.
    """

    def __init__(self, location: str) -> None:
        super().__init__()
        self._location: str = location
        self._current_temperature: int = 0

    @property
    def location(self) -> str:
        return self._location

    @property
    def current_temperature(self) -> int:
        return self._current_temperature

    def update_temperature(self, new_temperature: int) -> None:
        self._current_temperature = new_temperature
        self.notify(self._current_temperature)


# Displays pushed sensor readings numerically to console output.
# Concrete Observer Component
class NumericDisplay(ObserverInterface[int]):
    """
    Subscriber that formats and displays raw numerical sensor updates.
    """

    def __init__(self, display_id: str) -> None:
        self._display_id: str = display_id

    def update(self, value: int) -> None:
        print(f"[NumericDisplay {self._display_id}] Pushed temperature reading: {value}°C")


# Evaluates pushed temperature readings against critical threshold limit.
# Concrete Observer Component
class GaugeAlert(ObserverInterface[int]):
    """
    Subscriber that monitors temperature thresholds and triggers warning alerts.
    """

    def __init__(self, warning_threshold: int) -> None:
        self._warning_threshold = warning_threshold

    def update(self, value: int) -> None:
        if value >= self._warning_threshold:
            print(f"[GaugeAlert] WARNING: Critical threshold exceeded! Current value: {value}°C")
        else:
            print(f"[GaugeAlert] Temperature within normal parameters: {value}°C")


if __name__ == "__main__":
    temperature_sensor = Sensor(location="Server Room 01")

    display = NumericDisplay(display_id="D-101")
    alert = GaugeAlert(warning_threshold=30)

    temperature_sensor.attach(display)
    temperature_sensor.attach(alert)

    print("--- Simulating First Temperature Update ---")
    temperature_sensor.update_temperature(24)

    print("\n--- Simulating High Temperature Spike ---")
    temperature_sensor.update_temperature(35)

    print("\n--- Detaching Display Observer ---")
    temperature_sensor.detach(display)

    print("\n--- Simulating Third Temperature Update ---")
    temperature_sensor.update_temperature(31)
