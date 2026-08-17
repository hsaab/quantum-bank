"""
Split.io configuration and client initialization
"""

from splitio import get_factory
from splitio.exceptions import TimeoutException
import os

# Split.io API key - loaded from environment variable
# Make sure to set SPLIT_API_KEY in your .env file
SPLIT_API_KEY = os.environ.get("SPLIT_API_KEY")

if not SPLIT_API_KEY:
    print("⚠ WARNING: SPLIT_API_KEY not found in environment variables!")
    print("   Please set it in your .env file or environment")

# Initialize Split.io factory
split_factory = None
split_client = None


def init_split():
    """Initialize Split.io client"""
    global split_factory, split_client

    try:
        # Create factory with API key and config
        config = {"impressionsMode": "optimized"}
        split_factory = get_factory(SPLIT_API_KEY, config=config)

        # Get client instance
        split_client = split_factory.client()

        # Wait for SDK to be ready (with timeout)
        try:
            split_factory.block_until_ready(5)  # 5 second timeout
            print("✓ Split.io client initialized successfully")
        except TimeoutException:
            print(
                "⚠ Split.io client initialization timed out, using default treatments"
            )

    except Exception as e:
        print(f"✗ Failed to initialize Split.io: {e}")
        split_client = None

    return split_client


def get_split_client():
    """Get the Split.io client instance"""
    global split_client
    if split_client is None:
        init_split()
    return split_client


def destroy_split():
    """Clean up Split.io client"""
    global split_factory, split_client
    if split_client:
        split_client.destroy()
        split_client = None
    if split_factory:
        split_factory = None
