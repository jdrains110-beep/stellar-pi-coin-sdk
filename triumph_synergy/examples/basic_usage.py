"""
Triumph-Synergy Basic Usage Example

This example demonstrates how to use the Triumph-Synergy integration layer
to interact with the Stellar Pi Coin smart contract.
"""

import asyncio
import logging
from pathlib import Path
import sys

# Add the triumph-synergy module to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from triumph_synergy import IntegrationManager
from triumph_synergy.adapters import StellarPiAdapter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)


async def main():
    """Main example demonstrating Triumph-Synergy usage."""
    
    logger.info("=" * 60)
    logger.info("Triumph-Synergy Integration Layer - Basic Usage Example")
    logger.info("=" * 60)
    
    # Step 1: Initialize the Integration Manager
    logger.info("\n1. Initializing Integration Manager...")
    manager = IntegrationManager()
    logger.info(f"   Created: {manager}")
    
    # Step 2: Create and Register the Stellar Pi Coin Adapter
    logger.info("\n2. Creating Stellar Pi Coin Adapter...")
    
    # Note: Replace with your actual contract ID
    contract_id = "YOUR_PI_COIN_CONTRACT_ID"
    network = "testnet"
    
    pi_adapter = StellarPiAdapter(
        contract_id=contract_id,
        network=network,
        config={
            "password": "singularity_pass",
            "ai_alert_email": None  # Optional: add email for alerts
        }
    )
    logger.info(f"   Created: {pi_adapter}")
    
    # Register the adapter
    manager.register_adapter("stellar-pi-coin", pi_adapter)
    logger.info("   Registered adapter: stellar-pi-coin")
    
    # Step 3: Initialize the Adapter
    logger.info("\n3. Initializing Stellar Pi Coin Adapter...")
    success = await manager.initialize_adapter("stellar-pi-coin")
    if success:
        logger.info("   ✓ Adapter initialized successfully")
    else:
        logger.error("   ✗ Failed to initialize adapter")
        return
    
    # Step 4: Get Contract Information
    logger.info("\n4. Retrieving Contract Information...")
    pi_coin = manager.get_contract("stellar-pi-coin")
    contract_info = pi_coin.get_contract_info()
    
    logger.info(f"   Name: {contract_info['name']}")
    logger.info(f"   Symbol: {contract_info['symbol']}")
    logger.info(f"   Type: {contract_info['type']}")
    logger.info(f"   Fixed Peg: {contract_info['fixed_peg']}")
    logger.info(f"   Total Supply: {contract_info['total_supply']}")
    logger.info(f"   Features: {', '.join(contract_info['features'])}")
    
    # Step 5: Mint Pi Coins
    logger.info("\n5. Minting Pi Coins...")
    try:
        mint_result = await pi_coin.mint(
            amount=1000,
            source="mining"
        )
        logger.info(f"   ✓ Mint result: {mint_result}")
    except Exception as e:
        logger.error(f"   ✗ Mint failed: {e}")
    
    # Step 6: Query Ecosystem State
    logger.info("\n6. Querying Ecosystem State...")
    try:
        ecosystem = pi_coin.get_ecosystem()
        logger.info(f"   Balance: {ecosystem.get('balance', 'N/A')}")
        logger.info(f"   AI Level: {ecosystem.get('ai_level', 'N/A')}")
        logger.info(f"   Status: {ecosystem.get('status', 'N/A')}")
    except Exception as e:
        logger.error(f"   ✗ Query failed: {e}")
    
    # Step 7: Transfer Pi Coins
    logger.info("\n7. Transferring Pi Coins...")
    try:
        transfer_result = await pi_coin.transfer(
            to_address="GA_EXAMPLE_RECIPIENT_ADDRESS",
            amount=500,
            coin_id=b"example_coin_id"
        )
        logger.info(f"   ✓ Transfer result: {transfer_result}")
    except Exception as e:
        logger.error(f"   ✗ Transfer failed: {e}")
    
    # Step 8: Bridge to Another Chain
    logger.info("\n8. Bridging to Ethereum...")
    try:
        bridge_result = await pi_coin.bridge_to(
            dimension="ETH",
            amount=200,
            to="0xEXAMPLE_ETH_ADDRESS"
        )
        logger.info(f"   ✓ Bridge result: {bridge_result}")
    except Exception as e:
        logger.error(f"   ✗ Bridge failed: {e}")
    
    # Step 9: Health Check
    logger.info("\n9. Performing Health Check...")
    try:
        health = await pi_coin.health_check()
        logger.info(f"   Adapter: {health['adapter']}")
        logger.info(f"   Status: {health['status']}")
        logger.info(f"   Initialized: {health['initialized']}")
    except Exception as e:
        logger.error(f"   ✗ Health check failed: {e}")
    
    # Step 10: Ecosystem-wide Health Check
    logger.info("\n10. Checking Entire Ecosystem...")
    try:
        ecosystem_health = await manager.health_check()
        logger.info(f"   Manager Status: {ecosystem_health['manager']}")
        logger.info(f"   Total Adapters: {ecosystem_health['total_adapters']}")
        logger.info(f"   Total Contracts: {ecosystem_health['total_contracts']}")
        
        for adapter_name, status in ecosystem_health['adapters'].items():
            logger.info(f"   {adapter_name}: {status['status']}")
    except Exception as e:
        logger.error(f"   ✗ Ecosystem check failed: {e}")
    
    # Step 11: Get Ecosystem Info
    logger.info("\n11. Getting Ecosystem Information...")
    ecosystem_info = manager.get_ecosystem_info()
    logger.info(f"   Integration Manager: {ecosystem_info['integration_manager']}")
    logger.info(f"   Version: {ecosystem_info['version']}")
    logger.info(f"   Adapters: {list(ecosystem_info['adapters'].keys())}")
    
    # Step 12: Alternative: Call Functions Through Manager
    logger.info("\n12. Alternative: Using Manager to Call Functions...")
    try:
        result = await manager.call_contract_function(
            contract_name="stellar-pi-coin",
            function_name="mint",
            parameters={"amount": 250, "source": "rewards"}
        )
        logger.info(f"   ✓ Manager call result: {result}")
    except Exception as e:
        logger.error(f"   ✗ Manager call failed: {e}")
    
    logger.info("\n" + "=" * 60)
    logger.info("Example completed successfully!")
    logger.info("=" * 60)


async def demonstrate_multiple_contracts():
    """
    Demonstrate managing multiple contracts.
    
    This example shows how you would manage multiple smart contracts
    in the Triumph-Synergy ecosystem.
    """
    logger.info("\n\nDemonstrating Multiple Contracts...")
    logger.info("=" * 60)
    
    manager = IntegrationManager()
    
    # Register first contract (Stellar Pi Coin)
    pi_adapter = StellarPiAdapter(
        contract_id="PI_CONTRACT_ID",
        network="testnet"
    )
    manager.register_adapter("stellar-pi-coin", pi_adapter)
    
    # In a real scenario, you would register additional contracts here:
    # defi_adapter = DeFiAdapter(contract_id="DEFI_CONTRACT_ID")
    # manager.register_adapter("defi-protocol", defi_adapter)
    
    # nft_adapter = NFTAdapter(contract_id="NFT_CONTRACT_ID")
    # manager.register_adapter("nft-marketplace", nft_adapter)
    
    # Initialize all adapters
    logger.info("Initializing all adapters...")
    results = await manager.initialize_all_adapters()
    
    for adapter_name, success in results.items():
        status = "✓" if success else "✗"
        logger.info(f"   {status} {adapter_name}: {'initialized' if success else 'failed'}")
    
    # List all contracts
    logger.info("\nRegistered contracts:")
    for contract_name in manager.list_adapters():
        adapter = manager.get_adapter(contract_name)
        logger.info(f"   - {contract_name} ({adapter.network})")
    
    # You could then interact with multiple contracts:
    # pi_coin = manager.get_contract("stellar-pi-coin")
    # defi = manager.get_contract("defi-protocol")
    # nft = manager.get_contract("nft-marketplace")
    
    logger.info("=" * 60)


if __name__ == "__main__":
    # Run the main example
    asyncio.run(main())
    
    # Uncomment to run the multiple contracts example:
    # asyncio.run(demonstrate_multiple_contracts())
