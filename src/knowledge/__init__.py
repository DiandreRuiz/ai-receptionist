"""Static knowledge assets (FAQ, regional jobs, ZIP coverage) for the receptionist agent."""

from .loaders import KnowledgeBundle, load_knowledge_dir

__all__ = ["KnowledgeBundle", "load_knowledge_dir"]
