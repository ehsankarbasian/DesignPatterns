
# Products
class PostgresConnection:
    pass

class PostgresCursor:
    pass

class MySQLConnection:
    pass

class MySQLCursor:
    pass


# concrete factories as functions
def postgres_factory():
    return {
        "connection": PostgresConnection,
        "cursor": PostgresCursor
    }


def mysql_factory():
    return {
        "connection": MySQLConnection,
        "cursor": MySQLCursor
    }


# Client
factory = postgres_factory()

connection = factory["connection"]()
cursor = factory["cursor"]()
