"""Lead import service boundary.

Phase 1 will implement CSV parsing, validation, duplicate detection, and import summaries here.
"""


def describe_service() -> str:
    """Return the service responsibility."""
    return "Validates and normalizes incoming lead rows."
