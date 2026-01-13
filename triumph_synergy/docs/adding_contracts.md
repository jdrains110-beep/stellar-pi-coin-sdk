# Adding New Smart Contracts to Triumph-Synergy

This guide walks you through the process of integrating a new smart contract into the Triumph-Synergy ecosystem.

## Prerequisites

Before adding a new contract, ensure you have:
- The smart contract deployed and its contract ID
- Access to the contract's SDK or API
- Understanding of the contract's functions and state queries
- Contract documentation

## Step-by-Step Guide

### Step 1: Create a Contract Adapter

Create a new file in `triumph-synergy/adapters/` for your contract adapter.

```python
# triumph-synergy/adapters/my_contract_adapter.py

import sys
from pathlib import Path
from typing import Any, Dict, Optional, List

# Add paths as needed for importing the original contract SDK
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from triumph_synergy.core.contract_adapter import ContractAdapter


class MyContractAdapter(ContractAdapter):
    """
    Adapter for My Smart Contract.
    
    This adapter wraps the MyContract SDK and provides integration
    with the Triumph-Synergy ecosystem.
    """
    
    def __init__(
        self, 
        contract_id: str, 
        network: str = "testnet",
        config: Optional[Dict[str, Any]] = None
    ):
        super().__init__(contract_id, network, config)
        self.sdk = None
        
    async def initialize(self) -> None:
        """Initialize the adapter and underlying SDK."""
        try:
            # Import your contract's SDK
            from my_contract_sdk import MyContractSDK
            
            # Initialize the SDK
            self.sdk = MyContractSDK(
                contract_id=self.contract_id,
                network=self.network,
                # Add any config parameters
                **self.config
            )
            
            # Perform any necessary setup
            await self.sdk.setup()
            
            self._initialized = True
            self.logger.info("My Contract adapter initialized")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize adapter: {e}")
            raise
    
    def get_contract_info(self) -> Dict[str, Any]:
        """Get contract metadata."""
        return {
            "name": "My Smart Contract",
            "symbol": "MSC",
            "type": "defi",  # or "stablecoin", "governance", "nft", etc.
            "version": "1.0.0",
            "description": "Description of what your contract does",
            "contract_id": self.contract_id,
            "network": self.network,
            "original_author": "Author Name",
            "repository": "https://github.com/...",
            "features": [
                "Feature 1",
                "Feature 2",
            ]
        }
    
    async def call_function(
        self, 
        function_name: str, 
        parameters: Dict[str, Any]
    ) -> Any:
        """Call a function on the contract."""
        if not self.is_initialized():
            raise RuntimeError("Adapter not initialized")
        
        # Map function names to SDK methods
        function_map = {
            "my_function": self._my_function,
            "another_function": self._another_function,
        }
        
        if function_name not in function_map:
            raise ValueError(f"Unknown function: {function_name}")
        
        return await function_map[function_name](parameters)
    
    async def _my_function(self, params: Dict[str, Any]) -> Any:
        """Execute my_function."""
        # Extract parameters
        param1 = params.get("param1")
        param2 = params.get("param2")
        
        # Call the original SDK
        return await self.sdk.my_function(param1, param2)
    
    async def _another_function(self, params: Dict[str, Any]) -> Any:
        """Execute another_function."""
        return await self.sdk.another_function(**params)
    
    async def query_state(
        self, 
        query: str, 
        parameters: Optional[Dict[str, Any]] = None
    ) -> Any:
        """Query contract state."""
        if not self.is_initialized():
            raise RuntimeError("Adapter not initialized")
        
        query_map = {
            "balance": lambda: self.sdk.get_balance(),
            "status": lambda: self.sdk.get_status(),
        }
        
        if query not in query_map:
            raise ValueError(f"Unknown query: {query}")
        
        return query_map[query]()
    
    def get_supported_functions(self) -> List[str]:
        """List supported functions."""
        return ["my_function", "another_function"]
    
    # Optional: Add convenience methods for better usability
    async def my_function(self, param1: str, param2: int) -> Any:
        """Convenience method with type hints."""
        return await self.call_function("my_function", {
            "param1": param1,
            "param2": param2
        })
```

### Step 2: Update the Adapters Module

Add your adapter to `triumph-synergy/adapters/__init__.py`:

```python
from .stellar_pi_adapter import StellarPiAdapter
from .my_contract_adapter import MyContractAdapter

__all__ = [
    'StellarPiAdapter',
    'MyContractAdapter',
]
```

### Step 3: Register in Configuration

Add your contract to `triumph-synergy/config/contracts.json`:

```json
{
  "contracts": {
    "stellar-pi-coin": {
      // ... existing stellar pi coin config ...
    },
    "my-contract": {
      "name": "My Smart Contract",
      "type": "defi",
      "version": "1.0.0",
      "description": "Description of your contract",
      "contract_id": "YOUR_CONTRACT_ID",
      "network": "testnet",
      "adapter_class": "triumph_synergy.adapters.my_contract_adapter.MyContractAdapter",
      "original_author": "Your Name",
      "repository": "https://github.com/yourrepo/...",
      "enabled": true,
      "features": [
        "Feature 1",
        "Feature 2"
      ],
      "config": {
        "setting1": "value1",
        "setting2": "value2"
      }
    }
  }
}
```

### Step 4: Use Your Contract

Now you can use your contract through the integration manager:

```python
from triumph_synergy import IntegrationManager
from triumph_synergy.adapters import MyContractAdapter

# Initialize the manager
manager = IntegrationManager()

# Create and register your adapter
my_adapter = MyContractAdapter(
    contract_id="YOUR_CONTRACT_ID",
    network="testnet",
    config={"setting1": "value1"}
)
manager.register_adapter("my-contract", my_adapter)

# Initialize the adapter
await manager.initialize_adapter("my-contract")

# Use the contract
result = await manager.call_contract_function(
    "my-contract",
    "my_function",
    {"param1": "value", "param2": 123}
)

# Or use the adapter directly
my_contract = manager.get_contract("my-contract")
result = await my_contract.my_function("value", 123)
```

## Best Practices

### 1. Error Handling
Always handle errors gracefully and log appropriately:

```python
async def _my_function(self, params: Dict[str, Any]) -> Any:
    try:
        result = await self.sdk.my_function(**params)
        return result
    except Exception as e:
        self.logger.error(f"Error calling my_function: {e}")
        raise
```

### 2. Input Validation
Validate parameters before passing to the contract:

```python
async def _my_function(self, params: Dict[str, Any]) -> Any:
    amount = params.get("amount")
    if amount is None or amount <= 0:
        raise ValueError("Amount must be positive")
    
    return await self.sdk.my_function(amount)
```

### 3. Type Hints
Use type hints for better IDE support and documentation:

```python
async def my_function(self, param1: str, param2: int) -> Dict[str, Any]:
    """
    Execute my_function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Dictionary containing the result
    """
    return await self.call_function("my_function", {
        "param1": param1,
        "param2": param2
    })
```

### 4. Documentation
Document your adapter thoroughly:
- Add docstrings to all methods
- Explain parameter meanings
- Document return value structures
- Include usage examples

### 5. Testing
Create tests for your adapter:

```python
import pytest
from triumph_synergy.adapters import MyContractAdapter

@pytest.mark.asyncio
async def test_my_contract_adapter():
    adapter = MyContractAdapter(
        contract_id="test_id",
        network="testnet"
    )
    await adapter.initialize()
    
    result = await adapter.my_function("test", 123)
    assert result["status"] == "success"
```

## Contract Types

When registering your contract, use one of these standard types:

- `stablecoin`: Stablecoin implementations
- `defi`: DeFi protocols (lending, borrowing, etc.)
- `dex`: Decentralized exchanges
- `governance`: Governance and voting contracts
- `nft`: NFT and collectibles
- `oracle`: Price feeds and oracles
- `bridge`: Cross-chain bridges
- `identity`: Identity and KYC contracts
- `utility`: General utility contracts
- `other`: Other contract types

## Advanced Features

### Mock SDK for Testing

Provide a mock implementation for testing:

```python
def _create_mock_sdk(self):
    """Create a mock SDK when the real one is unavailable."""
    class MockSDK:
        async def my_function(self, param1, param2):
            return {"status": "success", "mock": True}
    
    return MockSDK()
```

### Health Checks

Override the health_check method if needed:

```python
async def health_check(self) -> Dict[str, Any]:
    """Perform contract-specific health checks."""
    base_health = await super().health_check()
    
    # Add custom checks
    if self.is_initialized():
        try:
            status = await self.sdk.get_status()
            base_health["contract_status"] = status
        except Exception as e:
            base_health["status"] = "unhealthy"
            base_health["error"] = str(e)
    
    return base_health
```

## Troubleshooting

### Import Errors
If you get import errors for the original SDK:
- Ensure the SDK is installed: `pip install your-sdk`
- Check the Python path in your adapter
- Provide a mock implementation for testing

### Initialization Failures
If adapter initialization fails:
- Check contract ID is correct
- Verify network settings
- Ensure all required configuration is provided
- Check logs for detailed error messages

### Function Call Errors
If contract function calls fail:
- Verify function name spelling
- Check parameter types and values
- Ensure adapter is initialized
- Review original SDK documentation

## Example: Complete Adapter

See `stellar_pi_adapter.py` for a complete, production-ready example of a contract adapter integrating Kosasih's stellar-pi-coin-sdk.

## Support

For questions or issues:
1. Check the [Architecture Documentation](architecture.md)
2. Review existing adapters for examples
3. Create an issue in the repository
