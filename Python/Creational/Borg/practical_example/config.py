"""
Application configuration using Borg-style shared state.

The configuration fields are implemented with thread-safe descriptors
So that their values are shared across all instances of the Config class.
"""

from descriptors import SharedField


class Config:
    """
    Application configuration container.

    Multiple instances may exist, but all configuration
    values are shared through descriptors.
    """

    # Database connection string
    db_url = SharedField("postgresql://localhost:5432/app")

    # Enable/disable debug mode
    debug = SharedField(False)

    # API key for external services
    api_key = SharedField(None)

    # Network timeout (seconds)
    timeout = SharedField(30)

    # Maximum retry attempts
    max_retries = SharedField(3)

    def __repr__(self):
        # Helpful representation for debugging
        return (
            f"Config("
            f"db_url={self.db_url}, "
            f"debug={self.debug}, "
            f"timeout={self.timeout}, "
            f"max_retries={self.max_retries})"
        )
