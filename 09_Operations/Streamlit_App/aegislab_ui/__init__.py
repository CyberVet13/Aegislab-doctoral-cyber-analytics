# AegisLab UI - Operational console for doctoral research environment
# Committee-defensible, auditable agent management and LLM session execution

__version__ = "1.0.0"

from .config import get_root, get_path, load_env
from .repo_validator import RepoValidator
from .templates_loader import TemplatesLoader
from .router import Router
from .model_gateway import ModelGateway
from .logging_audit import LoggingAudit
from .metadata import inject_frontmatter, parse_frontmatter
from .safety import SafetyGuard

__all__ = [
    "get_root",
    "get_path",
    "load_env",
    "RepoValidator",
    "TemplatesLoader",
    "Router",
    "ModelGateway",
    "LoggingAudit",
    "inject_frontmatter",
    "parse_frontmatter",
    "SafetyGuard",
]
