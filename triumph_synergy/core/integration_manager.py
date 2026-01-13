"""
Triumph-Synergy Integration Manager

This module provides the central integration manager for the Triumph-Synergy ecosystem.
It coordinates all contract adapters and provides a unified interface for interacting
with multiple smart contracts.
"""

import logging
from typing import Dict, Optional, Any, List
from .contract_registry import ContractRegistry
from .contract_adapter import ContractAdapter


class IntegrationManager:
    """
    Central manager for the Triumph-Synergy ecosystem.
    
    The IntegrationManager coordinates all integrated smart contracts through their
    adapters and provides a unified interface for the entire ecosystem.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the integration manager.
        
        Args:
            config_path: Optional path to the contracts configuration file
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.registry = ContractRegistry(config_path)
        self.adapters: Dict[str, ContractAdapter] = {}
        self.logger.info("Triumph-Synergy Integration Manager initialized")
    
    def register_adapter(self, name: str, adapter: ContractAdapter) -> None:
        """
        Register a contract adapter with the integration manager.
        
        Args:
            name: Unique name for the adapter
            adapter: The ContractAdapter instance
        """
        self.adapters[name] = adapter
        self.logger.info(f"Registered adapter: {name}")
    
    def get_adapter(self, name: str) -> Optional[ContractAdapter]:
        """
        Get a registered adapter by name.
        
        Args:
            name: Name of the adapter
            
        Returns:
            The ContractAdapter instance or None if not found
        """
        return self.adapters.get(name)
    
    async def initialize_adapter(self, name: str) -> bool:
        """
        Initialize a specific adapter.
        
        Args:
            name: Name of the adapter to initialize
            
        Returns:
            True if initialization succeeded, False otherwise
        """
        adapter = self.get_adapter(name)
        if adapter:
            try:
                await adapter.initialize()
                self.logger.info(f"Initialized adapter: {name}")
                return True
            except Exception as e:
                self.logger.error(f"Failed to initialize adapter {name}: {e}")
                return False
        else:
            self.logger.error(f"Adapter not found: {name}")
            return False
    
    async def initialize_all_adapters(self) -> Dict[str, bool]:
        """
        Initialize all registered adapters.
        
        Returns:
            Dictionary mapping adapter names to initialization success status
        """
        results = {}
        for name in self.adapters.keys():
            results[name] = await self.initialize_adapter(name)
        return results
    
    def get_contract(self, name: str) -> Optional[ContractAdapter]:
        """
        Get a contract adapter (alias for get_adapter for convenience).
        
        Args:
            name: Name of the contract
            
        Returns:
            The ContractAdapter instance or None if not found
        """
        return self.get_adapter(name)
    
    def list_adapters(self) -> List[str]:
        """
        Get a list of all registered adapter names.
        
        Returns:
            List of adapter names
        """
        return list(self.adapters.keys())
    
    def list_contracts(self) -> List[str]:
        """
        Get a list of all contracts in the registry.
        
        Returns:
            List of contract names from the registry
        """
        return self.registry.list_contracts()
    
    async def call_contract_function(
        self, 
        contract_name: str, 
        function_name: str, 
        parameters: Dict[str, Any]
    ) -> Any:
        """
        Call a function on a contract through its adapter.
        
        Args:
            contract_name: Name of the contract
            function_name: Name of the function to call
            parameters: Parameters to pass to the function
            
        Returns:
            Result of the contract function call
            
        Raises:
            ValueError: If contract not found or not initialized
        """
        adapter = self.get_adapter(contract_name)
        if not adapter:
            raise ValueError(f"Contract adapter not found: {contract_name}")
        
        if not adapter.is_initialized():
            raise ValueError(f"Contract adapter not initialized: {contract_name}")
        
        return await adapter.call_function(function_name, parameters)
    
    async def query_contract_state(
        self,
        contract_name: str,
        query: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Query the state of a contract through its adapter.
        
        Args:
            contract_name: Name of the contract
            query: The state query identifier
            parameters: Optional parameters for the query
            
        Returns:
            The queried state data
            
        Raises:
            ValueError: If contract not found or not initialized
        """
        adapter = self.get_adapter(contract_name)
        if not adapter:
            raise ValueError(f"Contract adapter not found: {contract_name}")
        
        if not adapter.is_initialized():
            raise ValueError(f"Contract adapter not initialized: {contract_name}")
        
        return await adapter.query_state(query, parameters)
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on all adapters.
        
        Returns:
            Dictionary containing health status for all adapters
        """
        health_status = {
            "manager": "healthy",
            "total_adapters": len(self.adapters),
            "total_contracts": len(self.registry.list_contracts()),
            "adapters": {}
        }
        
        for name, adapter in self.adapters.items():
            try:
                health_status["adapters"][name] = await adapter.health_check()
            except Exception as e:
                health_status["adapters"][name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return health_status
    
    def get_ecosystem_info(self) -> Dict[str, Any]:
        """
        Get comprehensive information about the ecosystem.
        
        Returns:
            Dictionary containing ecosystem information
        """
        return {
            "integration_manager": "Triumph-Synergy",
            "version": "1.0.0",
            "adapters": {
                name: {
                    "initialized": adapter.is_initialized(),
                    "contract_id": adapter.contract_id,
                    "network": adapter.network
                }
                for name, adapter in self.adapters.items()
            },
            "registry_stats": self.registry.get_registry_stats()
        }
    
    def __repr__(self) -> str:
        return f"IntegrationManager(adapters={len(self.adapters)}, contracts={len(self.registry.list_contracts())})"
