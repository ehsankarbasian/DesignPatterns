from __future__ import annotations
from typing import Optional
from abc import ABC, abstractmethod


class Status:
    locked = True
    alarm_on = True
    light_on = False


class CheckerInterface(ABC):
    
    @abstractmethod
    def set_next(self, checker: CheckerInterface) -> CheckerInterface:
        pass
    
    @abstractmethod
    def check(self, status: Status) -> Optional[str]:
        pass


class NullChecker(CheckerInterface):
    """
    Design goal:
        Terminate the validation chain without requiring conditional null checks.
    Key decisions:
        Implement the CheckerInterface to provide a no-op fallback behavior.
    Trade-offs:
        Requires an explicit terminal class instead of relying on NoneType sentinels.
    """

    def set_next(self, checker: CheckerInterface) -> CheckerInterface:
        return checker

    def check(self, status: Status) -> Optional[str]:
        return None


class AbstractChecker(CheckerInterface):
    """
    Design goal:
        Provide standard successor management initialized with a Null Object terminal.
    Key decisions:
        Initialize _next_checker to NullChecker to eliminate None checks during traversal.
    Trade-offs:
        Instantiates a default terminal handler for each concrete checker instance.
    """

    def __init__(self) -> None:
        self._next_checker: CheckerInterface = NullChecker()

    def set_next(self, checker: CheckerInterface) -> CheckerInterface:
        self._next_checker = checker
        return checker
    
    def check(self, status: Status) -> Optional[str]:
        return self._next_checker.check(status)


class LockChecker(AbstractChecker):
    
    def check(self, status: Status) -> Optional[str]:
        if not status.locked:
            print("The door is not locked")
            return "Door unlocked"
        
        print("Lock (OK)")
        return super().check(status)


class AlarmChecker(AbstractChecker):
    
    def check(self, status: Status) -> Optional[str]:
        if not status.alarm_on:
            print("The alarm is not on")
            return "Alarm off"
        
        print("Alarm (OK)")
        return super().check(status)


class LightChecker(AbstractChecker):
    
    def check(self, status: Status) -> Optional[str]:
        if status.light_on:
            print("The light is not off")
            return "Light on"
        
        print("Light (OK)")
        return super().check(status)


if __name__ == "__main__":
    print()
    
    lock = LockChecker()
    alarm = AlarmChecker()
    light = LightChecker()

    lock.set_next(alarm).set_next(light)

    print("Chain: Lock > Alarm > Light\n")
    
    print("First check:")
    lock.check(Status)
    
    print("\nTurn the light on")
    Status.light_on = True
    lock.check(Status)
    
    print("\nTurn the lock open")
    Status.locked = False
    lock.check(Status)
    
    print("\n")
    print("Reset the status to (OK) state\n\n")
    Status.locked = True
    Status.light_on = False
    
    print("Subchain: Alarm > Light\n")
    
    print("First check:")
    alarm.check(Status)
    
    print("\nTurn the lock open")
    Status.locked = False
    alarm.check(Status)
    
    print("\nTurn the light on")
    Status.light_on = True
    alarm.check(Status)
