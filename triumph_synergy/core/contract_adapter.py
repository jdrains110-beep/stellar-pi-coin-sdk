"""
Triumph-Synergy Contract Adapter Interface

This module defines the base interface that all smart contract adapters must implement.
It ensures a consistent interaction pattern across all integrated contracts.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
import logging


class ContractAdapter(ABC):
    """
    Base class for all smart contract adapters in the Triumph-Synergy ecosystem.
    
    Each adapter wraps a specific smart contract implementation and provides
    a standardized interface for interaction without modifying the original contract.
    """
    
    def __init__(self, contract_id: str, network: str = "testnet", config: Optional[Dict[str, Any]] = None):
        """
        Initialize the contract adapter.
        
        Args:
            contract_id: The unique identifier for the smart contract
            network: The network environment ('testnet' or 'mainnet')
            config: Optional configuration dictionary for the adapter
        """
        self.contract_id = contract_id
        self.network = network
        self.config = config or {}
        self.logger = logging.getLogger(f"{self.__class__.__name__}")
        self._initialized = False
        
    @abstractmethod
    async def initialize(self) -> None:
        """
        Initialize the adapter and its underlying contract connection.
        Must be called before using the adapter.
        """
        pass
    
    @abstractmethod
    def get_contract_info(self) -> Dict[str, Any]:
        """
        Get information about the underlying smart contract.
        
        Returns:
            Dictionary containing contract metadata (name, version, description, etc.)
        """
        pass
    
    @abstractmethod
    async def call_function(self, function_name: str, parameters: Dict[str, Any]) -> Any:
        """
        Call a function on the underlying smart contract.
        
        Args:
            function_name: Name of the contract function to call
            parameters: Dictionary of parameters to pass to the function
            
        Returns:
            The result of the contract function call
        """
        pass
    
    @abstractmethod
    async def query_state(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> Any:
        """
        Query the state of the smart contract.
        
        Args:
            query: The state query identifier
            parameters: Optional parameters for the query
            
        Returns:
            The queried state data
        """
        pass
    
    def is_initialized(self) -> bool:
        """
        Check if the adapter has been initialized.
        
        Returns:
            True if initialized, False otherwise
        """
        return self._initialized
    
    def get_supported_functions(self) -> List[str]:
        """
        Get a list of functions supported by this adapter.
        
        Returns:
            List of function names available through this adapter
        """
        return []
    
    async def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the contract adapter.
        
        Returns:
            Dictionary containing health status information
        """
        return {
            "adapter": self.__class__.__name__,
            "contract_id": self.contract_id,
            "network": self.network,
            "initialized": self._initialized,
            "status": "healthy" if self._initialized else "not_initialized"
        }
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(contract_id='{self.contract_id}', network='{self.network}')"
