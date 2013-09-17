from __future__ import unicode_literals

class SpyglassError(Exception):
    """Any error raised by the spyglass library."""

class ConfigurationError(SpyglassError):
    """Raised when configuration options are invalid or conflicting."""
