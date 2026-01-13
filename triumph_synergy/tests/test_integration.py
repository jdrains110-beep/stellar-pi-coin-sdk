"""
Tests for Triumph-Synergy Integration Layer

This module contains tests for the core integration components and
the Stellar Pi Coin adapter.
"""

import pytest
import asyncio
from pathlib import Path
import sys

# Add triumph-synergy to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from triumph_synergy.core import ContractAdapter, ContractRegistry, IntegrationManager
from triumph_synergy.adapters import StellarPiAdapter


class TestContractRegistry:
    """Tests for the ContractRegistry."""
    
    def test_registry_initialization(self):
        """Test that registry initializes correctly."""
        registry = ContractRegistry()
        assert registry is not None
        assert isinstance(registry.contracts, dict)


class TestStellarPiAdapter:
    """Tests for the StellarPiAdapter."""
    
    def test_adapter_creation(self):
        """Test creating a Stellar Pi adapter."""
        adapter = StellarPiAdapter(
            contract_id="test_contract_id",
            network="testnet"
        )
        
        assert adapter is not None
        assert adapter.contract_id == "test_contract_id"
        assert adapter.network == "testnet"
        assert not adapter.is_initialized()
    
    @pytest.mark.asyncio
    async def test_adapter_initialization(self):
        """Test initializing the adapter."""
        adapter = StellarPiAdapter(
            contract_id="test_contract_id",
            network="testnet",
            config={"password": "test_pass"}
        )
        
        # Initialize (will use mock SDK if real SDK not available)
        await adapter.initialize()
        
        assert adapter.is_initialized()
        assert adapter.sdk is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
