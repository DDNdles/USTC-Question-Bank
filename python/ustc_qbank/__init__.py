"""Zero-dependency Python API for USTC-Question-Bank."""

from .loader import Course, Question, QuestionBank, TaxonomyNode
from .sqlite_builder import build_sqlite

__all__ = [
    "Course",
    "Question",
    "QuestionBank",
    "TaxonomyNode",
    "build_sqlite",
]

__version__ = "0.1.0"
