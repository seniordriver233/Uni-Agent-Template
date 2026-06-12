"""UniAds-compatible modular agent template."""

from .agent import DomainAgent
from .config import Settings, load_settings

__all__ = ["DomainAgent", "Settings", "load_settings"]
