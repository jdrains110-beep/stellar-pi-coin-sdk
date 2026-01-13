"""
Triumph-Synergy Integration Layer

A modular financial ecosystem for integrating multiple smart contracts
without modifying their original implementations.
"""

__version__ = "1.0.0"

from .core import IntegrationManager, ContractAdapter, ContractRegistry

__all__ = [
    'IntegrationManager',
    'ContractAdapter', 
    'ContractRegistry',
]
