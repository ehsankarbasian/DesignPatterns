from abc import ABC, abstractmethod

# Step Builder (a.k.a. Staged / Type-Safe Builder)
#
# Intent:
#   Enforce a strict step-by-step construction workflow where each phase
#   is handled by a distinct builder object exposing ONLY the methods
#   valid for that exact stage.
#
# Why separate classes instead of returning self?
#   Returning 'self' from a single multi-interface class leaks methods at
#   runtime (e.g. bypassing static checks to call add_column before table).
#   Separate step classes guarantee both static type-safety AND runtime isolation.


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


class _ColumnStepBuilder(ColumnStepInterface):

    def __init__(self, table_name: str) -> None:
        self._table_name: str = table_name
        self._columns: list[str] = []

    def add_column(self, name: str, data_type: str) -> ColumnStepInterface:
        self._columns.append(f'{name} {data_type}')
        return self

    def done(self) -> str:
        columns_part = ', '.join(self._columns)
        return f'CREATE TABLE {self._table_name} ({columns_part});'


class _TableStepBuilder(TableStepInterface):

    def table(self, table_name: str) -> ColumnStepInterface:
        # Step transition: Spawns the next stage builder only when table is provided.
        # This completely isolates the two stages.
        return _ColumnStepBuilder(table_name=table_name)


def create_table() -> TableStepInterface:
    return _TableStepBuilder()


if __name__ == '__main__':
    # Stage 1: create_table() yields _TableStepBuilder (TableStepInterface).
    # Trying to call .add_column() or .done() here raises AttributeError at runtime.
    table_builder = create_table()

    # Stage 2: Calling .table() transitions to _ColumnStepBuilder (ColumnStepInterface).
    # Once transitioned, calling .table() again is impossible (AttributeError).
    query = (
        table_builder
        .table('users')
        .add_column('id', 'INT')
        .add_column('username', 'VARCHAR(50)')
        .done()
    )

    print(query)
