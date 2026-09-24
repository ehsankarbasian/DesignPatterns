from abc import ABC, abstractmethod

# Step Builder (Staged / Type-Safe Builder)
# 
# Intent:
#   Enforce a strict step-by-step construction workflow where the
#   IDE/Type-checker limits methods based on the current stage via
#   Return-Type Hinting.


class ColumnStepInterface(ABC):

    @abstractmethod
    def add_column(self, name: str, data_type: str) -> 'ColumnStepInterface':
        pass

    @abstractmethod
    def done(self) -> str:
        pass


class TableStepInterface(ABC):

    @abstractmethod
    def table(self, table_name: str) -> ColumnStepInterface:
        pass


class SQLBuilder(TableStepInterface, ColumnStepInterface):
    """
    A single concrete builder that manages the internal state
    while exposing different interfaces via type hints.
    """

    def __init__(self) -> None:
        self._table_name: str = ""
        self._columns: list[str] = []

    def table(self, table_name: str) -> ColumnStepInterface:
        self._table_name = table_name
        return self

    def add_column(self, name: str, data_type: str) -> ColumnStepInterface:
        self._columns.append(f'{name} {data_type}')
        return self

    def done(self) -> str:
        columns_part = ', '.join(self._columns)
        return f'CREATE TABLE {self._table_name} ({columns_part});'


if __name__ == '__main__':
    # Usage:
    # 1. Start with the builder. IDE suggests .table().
    # 2. After .table(), IDE suggests .add_column() or .done().
    
    query = (
        SQLBuilder()
        .table('users')
        .add_column('id', 'INT')
        .add_column('username', 'VARCHAR(50)')
        .done()
    )

    print(query)
