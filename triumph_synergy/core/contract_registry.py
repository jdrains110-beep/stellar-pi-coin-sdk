"""
Triumph-Synergy Contract Registry

This module manages the registry of all smart contracts integrated into the
Triumph-Synergy ecosystem. It handles contract registration, discovery, and lifecycle management.
"""

import json
import logging
from typing import Dict, Optional, Any, List
from pathlib import Path


class ContractRegistry:
    """
    Registry for managing smart contracts in the Triumph-Synergy ecosystem.
    
    The registry maintains metadata about all integrated contracts and provides
    methods for contract discovery and configuration management.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the contract registry.
        
        Args:
            config_path: Path to the contracts configuration file
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.contracts: Dict[str, Dict[str, Any]] = {}
        self.config_path = config_path or self._get_default_config_path()
        self._load_contracts()
        
    def _get_default_config_path(self) -> str:
        """Get the default configuration file path."""
        return str(Path(__file__).parent.parent / "config" / "contracts.json")
    
    def _load_contracts(self) -> None:
        """Load contract configurations from the JSON file."""
        try:
            with open(self.config_path, 'r') as f:
                data = json.load(f)
                self.contracts = data.get("contracts", {})
                self.logger.info(f"Loaded {len(self.contracts)} contract(s) from registry")
        except FileNotFoundError:
            self.logger.warning(f"Contract registry file not found at {self.config_path}. Starting with empty registry.")
            self.contracts = {}
        except json.JSONDecodeError as e:
            self.logger.error(f"Error parsing contract registry: {e}")
            self.contracts = {}
    
    def register_contract(self, name: str, contract_info: Dict[str, Any]) -> None:
        """
        Register a new smart contract in the registry.
        
        Args:
            name: Unique name for the contract
            contract_info: Dictionary containing contract metadata
        """
        self.contracts[name] = contract_info
        self.logger.info(f"Registered contract: {name}")
        self._save_contracts()
    
    def unregister_contract(self, name: str) -> bool:
        """
        Unregister a smart contract from the registry.
        
        Args:
            name: Name of the contract to unregister
            
        Returns:
            True if contract was unregistered, False if not found
        """
        if name in self.contracts:
            del self.contracts[name]
            self.logger.info(f"Unregistered contract: {name}")
            self._save_contracts()
            return True
        return False
    
    def get_contract(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get contract information by name.
        
        Args:
            name: Name of the contract
            
        Returns:
            Contract information dictionary or None if not found
        """
        return self.contracts.get(name)
    
    def list_contracts(self) -> List[str]:
        """
        Get a list of all registered contract names.
        
        Returns:
            List of contract names
        """
        return list(self.contracts.keys())
    
    def get_contracts_by_type(self, contract_type: str) -> List[str]:
        """
        Get contracts filtered by type.
        
        Args:
            contract_type: Type of contract (e.g., 'stablecoin', 'defi', 'governance')
            
        Returns:
            List of contract names matching the type
        """
        return [
            name for name, info in self.contracts.items()
            if info.get("type") == contract_type
        ]
    
    def update_contract(self, name: str, updates: Dict[str, Any]) -> bool:
        """
        Update contract information.
        
        Args:
            name: Name of the contract to update
            updates: Dictionary of fields to update
            
        Returns:
            True if updated, False if contract not found
        """
        if name in self.contracts:
            self.contracts[name].update(updates)
            self.logger.info(f"Updated contract: {name}")
            self._save_contracts()
            return True
        return False
    
    def _save_contracts(self) -> None:
        """Save the current registry to the configuration file."""
        try:
            Path(self.config_path).parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump({"contracts": self.contracts}, f, indent=2)
            self.logger.debug("Registry saved to disk")
        except Exception as e:
            self.logger.error(f"Error saving registry: {e}")
    
    def get_registry_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the contract registry.
        
        Returns:
            Dictionary containing registry statistics
        """
        types = {}
        for info in self.contracts.values():
            contract_type = info.get("type", "unknown")
            types[contract_type] = types.get(contract_type, 0) + 1
        
        return {
            "total_contracts": len(self.contracts),
            "contracts_by_type": types,
            "contract_names": self.list_contracts()
        }
    
    def __repr__(self) -> str:
        return f"ContractRegistry(contracts={len(self.contracts)})"
