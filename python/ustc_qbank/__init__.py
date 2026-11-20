"""Zero-dependency Python API for USTC-Question-Bank."""

from .loader import Course, FigureRef, Question, QuestionBank, QuestionOption, TaxonomyNode
from .sqlite_builder import build_sqlite

__all__ = [
    "Course",
    "FigureRef",
    "Question",
    "QuestionBank",
    "QuestionOption",
    "TaxonomyNode",
    "build_sqlite",
]

__version__ = "0.1.0"
