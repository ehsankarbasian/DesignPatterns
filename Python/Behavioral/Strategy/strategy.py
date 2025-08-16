from __future__ import annotations
from abc import ABC, abstractmethod


class SortStrategy(ABC):
    
    @abstractmethod
    def sort(self, array):
        pass


class BubbleSortStrategy(SortStrategy):
    
    def sort(self, array):
        for n in range(len(array) - 1, 0, -1):
            swapped = False  
            for i in range(n):
                if array[i] > array[i + 1]:
                    array[i], array[i + 1] = array[i + 1], array[i]
                    swapped = True
            if not swapped:
                return array


class QuickSortStrategy(SortStrategy):
    
    def sort(self, array):
        return self.__quickSort(array, 0, len(array)-1)

    def __quickSort(self, array, low, high):
        if low < high:
            pi = self.__partition(array, low, high)
            self.__quickSort(array, low, pi - 1)
            self.__quickSort(array, pi + 1, high)
        return array
    
    def __partition(self, array, low, high):
        pivot = array[high]
        i = low - 1
        for j in range(low, high):
            if array[j] <= pivot:
                i = i + 1
                (array[i], array[j]) = (array[j], array[i])

        (array[i + 1], array[high]) = (array[high], array[i + 1])
        return i + 1


class Context():
    
    def __init__(self, sort_strategy: SortStrategy) -> None:
        self._sort_strategy = sort_strategy

    @property
    def sort_strategy(self) -> SortStrategy:
        return self._sort_strategy

    @sort_strategy.setter
    def sort_strategy(self, sort_strategy: SortStrategy) -> None:
        self._sort_strategy = sort_strategy

    def do_sort_logic(self, array):
        result = self._sort_strategy.sort(array)
        print(result)


array = [7, 6, 8, 2, 9, 5, 1, 4, 3]
context_1 = Context(BubbleSortStrategy())
context_2 = Context(QuickSortStrategy())
context_1.do_sort_logic(array)
context_2.do_sort_logic(array)
