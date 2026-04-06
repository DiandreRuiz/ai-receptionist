"""Static knowledge assets (FAQ, Cartesia TTS notes, regional jobs, ZIP coverage)."""

from .loaders import KnowledgeBundle, load_knowledge_dir

__all__ = ["KnowledgeBundle", "load_knowledge_dir"]
