class EntityDoesNotExist(Exception):
    """Raised when an entity was not found in the database."""

    pass


class DatabaseConnectionError(Exception):
    """Raised when there's a connection error to the database."""

    pass


class DatabaseInteractionError(Exception):
    """Raised when there's an error interacting with the database."""

    pass


class SQLSyntaxError(DatabaseInteractionError):
    """Raised when there's a syntax error in the SQL command."""

    pass


class TableOrColumnNotFoundError(DatabaseInteractionError):
    """Raised when a specified table or column does not exist in the database."""

    pass


class ParameterMismatchError(DatabaseInteractionError):
    """Raised when there's a mismatch between the parameters provided and what's expected by the SQL command."""

    pass
