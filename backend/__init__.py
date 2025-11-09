"""
Telecom Complaints Backend
A backend system for categorizing and analyzing telecom complaints.
"""

from .backend import ComplaintBackend, create_backend
from .data_loader import DataLoader
from .categorizer import ComplaintCategorizer
from .data_processor import DataProcessor

__all__ = [
    'ComplaintBackend',
    'create_backend',
    'DataLoader',
    'ComplaintCategorizer',
    'DataProcessor'
]

__version__ = '1.0.0'

