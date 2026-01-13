"""
Triumph-Synergy Core Module

This module provides the core functionality for the Triumph-Synergy integration layer.
"""

from .contract_adapter import ContractAdapter
from .contract_registry import ContractRegistry
from .integration_manager import IntegrationManager

__all__ = [
    'ContractAdapter',
    'ContractRegistry',
    'IntegrationManager',
]
