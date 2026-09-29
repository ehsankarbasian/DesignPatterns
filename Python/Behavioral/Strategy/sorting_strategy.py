"""
Strategy Design Pattern (GoF) — Simple Adaptive Sorting Example

Goal of this module:
- Keep the example simple and educational.
- Still demonstrate the real "Context" role (it can choose a strategy).
- Strategies are stateless so we can safely reuse shared instances (flyweight-like).

Architectural note (intentional deviation from pure GoF):
- In the pure GoF form, the client selects and injects the strategy.
- Here, the context performs adaptive selection based on input size.
  The client can still override the strategy explicitly.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, Sequence, TypeVar

T = TypeVar("T")


class SortStrategyInterface(ABC, Generic[T]):
    """Strategy interface: all sorting algorithms must implement this contract."""

    @abstractmethod
    def sort(self, data: Sequence[T]) -> list[T]:
        """Return a new sorted list (do not mutate the input)."""


class InsertionSortStrategy(SortStrategyInterface[T]):
    """Good for small collections due to low overhead."""

    def sort(self, data: Sequence[T]) -> list[T]:
        items = list(data)
        for i in range(1, len(items)):
            key = items[i]
            j = i - 1
            while j >= 0 and items[j] > key:
                items[j + 1] = items[j]
                j -= 1
            items[j + 1] = key
        return items


class QuickSortStrategy(SortStrategyInterface[T]):
    """
    A decent general-purpose in-memory sort for medium-size collections.

    Trade-off (intentional simplification):
    - Pivot selection is always the LAST element. On (nearly) sorted input this may
      degrade to O(n^2). Production-grade quicksort usually randomizes the pivot
      or uses median-of-three. We keep this version for clarity.
    """

    def sort(self, data: Sequence[T]) -> list[T]:
        items = list(data)
        self._quick_sort(items, 0, len(items) - 1)
        return items

    def _quick_sort(self, items: list[T], low: int, high: int) -> None:
        if low < high:
            pivot_index = self._partition(items, low, high)
            self._quick_sort(items, low, pivot_index - 1)
            self._quick_sort(items, pivot_index + 1, high)

    def _partition(self, items: list[T], low: int, high: int) -> int:
        pivot = items[high]
        i = low - 1
        for j in range(low, high):
            if items[j] <= pivot:
                i += 1
                items[i], items[j] = items[j], items[i]
        items[i + 1], items[high] = items[high], items[i + 1]
        return i + 1


class MergeSortStrategy(SortStrategyInterface[T]):
    """Stable sort with predictable performance; good for large collections."""

    def sort(self, data: Sequence[T]) -> list[T]:
        return self._merge_sort(list(data))

    def _merge_sort(self, items: list[T]) -> list[T]:
        if len(items) <= 1:
            return items

        mid = len(items) // 2
        left = self._merge_sort(items[:mid])
        right = self._merge_sort(items[mid:])
        return self._merge(left, right)

    def _merge(self, left: list[T], right: list[T]) -> list[T]:
        result: list[T] = []
        i = j = 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1

        result.extend(left[i:])
        result.extend(right[j:])
        return result


class SortingContext(Generic[T]):
    """
    Context:
    - Client calls `sort()`.
    - If no strategy is explicitly forced, the context chooses one based on input size.

    Notes:
    - Thresholds are educational and intentionally simple (not benchmark-based).
    - Selection is based only on input size (not on "sortedness" of the data).
    """

    SMALL_THRESHOLD = 10
    MEDIUM_THRESHOLD = 1000

    # Shared stateless strategies (safe to reuse across contexts)
    _INSERTION_SORT_STRATEGY: SortStrategyInterface[T] = InsertionSortStrategy()
    _QUICK_SORT_STRATEGY: SortStrategyInterface[T] = QuickSortStrategy()
    _MERGE_SORT_STRATEGY: SortStrategyInterface[T] = MergeSortStrategy()

    def __init__(self, strategy: SortStrategyInterface[T] | None = None) -> None:
        self._strategy = strategy

    @property
    def strategy(self) -> SortStrategyInterface[T] | None:
        return self._strategy

    @strategy.setter
    def strategy(self, strategy: SortStrategyInterface[T] | None) -> None:
        self._strategy = strategy

    def _choose_strategy(self, size: int) -> SortStrategyInterface[T]:
        # Context encapsulates the selection logic (the key point of this example).
        if size <= self.SMALL_THRESHOLD:
            return self._INSERTION_SORT_STRATEGY
        if size <= self.MEDIUM_THRESHOLD:
            return self._QUICK_SORT_STRATEGY
        return self._MERGE_SORT_STRATEGY

    def sort(self, data: Sequence[T]) -> list[T]:
        selected = self._strategy or self._choose_strategy(len(data))
        return selected.sort(data)


if __name__ == "__main__":
    context = SortingContext[int]()  # adaptive
    print(context.sort([5, 1, 4, 2, 3]))

    context.strategy = MergeSortStrategy()  # forced
    print(context.sort([5, 1, 4, 2, 3]))
