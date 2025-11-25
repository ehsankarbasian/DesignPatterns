from __future__ import annotations
from typing import Any

from abc import ABC, abstractmethod


class CheckerInterface(ABC):
    
    @abstractmethod
    def set_next(self, checker: CheckerInterface) -> CheckerInterface:
        pass
    
    @abstractmethod
    def check(self, status: Status):
        pass


class AbstractChecker(CheckerInterface):
    
    _next_checker: CheckerInterface = None

    def set_next(self, checker: CheckerInterface) -> CheckerInterface:
        self._next_checker = checker
        return checker
    
    @abstractmethod
    def check(self, status: Any):
        if self._next_checker:
            return self._next_checker.check(status)

        return None


class LockChecker(AbstractChecker):
    
    def check(self, status):
        if not status.locked:
            print('The door is not locked')
        else:
            print('Lock (OK)')
            return super().check(status)


class AlarmChecker(AbstractChecker):
    
    def check(self, status):
        if not status.alarm_on:
            print('The alarm is not on')
        else:
            print('Alarm (OK)')
            return super().check(status)


class LightChecker(AbstractChecker):
    
    def check(self, status):
        if status.light_on:
            print('The light is not off')
        else:
            print('Light (OK)')
            return super().check(status)


class Status:
    locked = True
    alarm_on = True
    light_on = False


if __name__ == "__main__":
    print()
    
    lock = LockChecker()
    alarm = AlarmChecker()
    light = LightChecker()

    lock.set_next(alarm).set_next(light)

    print("Chain: Lock > Alarm > Light\n")
    
    print('First ckeck:')
    lock.check(Status)
    
    print('\nTurn the light on')
    Status.light_on = True
    lock.check(Status)
    
    print('\nTurn the lock open')
    Status.locked = False
    lock.check(Status)
    
    print("\n")
    print('Reset the status to (OK) state\n\n')
    Status.locked = True
    Status.light_on = False
    
    print("Subchain: Alarm > Light\n")
    
    print('First ckeck:')
    alarm.check(Status)
    
    print('\nTurn the lock open')
    Status.locked = False
    alarm.check(Status)
    
    print('\nTurn the light on')
    Status.light_on = True
    alarm.check(Status)
