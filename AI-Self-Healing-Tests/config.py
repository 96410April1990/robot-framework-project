"""
Simple Configuration for AI Self-Healing Tests
==============================================

This file contains basic configuration for the tutorial tests.
For advanced AI features, you would integrate with your existing
Walmart Corporate AI infrastructure.
"""

# Basic test configuration
BROWSER_TYPE = "chrome"
IMPLICIT_WAIT = 10  # seconds
PAGE_LOAD_TIMEOUT = 30  # seconds

# AI Configuration (for advanced steps)
# Note: Replace with your actual Walmart Corporate AI credentials
AI_CONFIG = {
    'api_key': 'eyJzZ252ZXIiOiIxIiwiYWxnIjoiSFMyNTYiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiIxMTA5MiIsInN1YiI6IjE3IiwiaXNzIjoiV01UTExNR0FURVdBWS1TVEciLCJhY3QiOiJyMG4wMWd1IiwidHlwZSI6IlVTUiIsImlhdCI6MTc2ODkxNzU2MiwiZXhwIjoxNzc0MTAxNTYyfQ.n9lfkbdUjrkNQEit3VxUGoTBKMLrFsJw6eELs05zMZ4',  # Replace with your actual JWT token
    'endpoints': [
        'https://wmtllmgateway.stage.walmart.com/wmtllmgateway/openai/deployments/gpt-4o/chat/completions'
    ],
    'model': 'gpt-4o',
    'max_tokens': 150,
    'temperature': 0.1
}

# Test data
TEST_DATA = {
    'email': 'test@example.com',
    'password': 'password123',
    'country': 'us'
}

# Healing configuration
HEALING_CONFIG = {
    'max_strategies_per_element': 10,
    'strategy_timeout': 2,  # seconds to wait for each strategy
    'learning_enabled': True,
    'verbose_logging': True
}

def get_ai_enabled():
    """Check if AI features are properly configured"""
    return AI_CONFIG['api_key'] != 'eyJzZ252ZXIiOiIxIiwiYWxnIjoiSFMyNTYiLCJ0eXAiOiJKV1QifQ.eyJqdGkiOiIxMTA5MiIsInN1YiI6IjE3IiwiaXNzIjoiV01UTExNR0FURVdBWS1TVEciLCJhY3QiOiJyMG4wMWd1IiwidHlwZSI6IlVTUiIsImlhdCI6MTc2ODkxNzU2MiwiZXhwIjoxNzc0MTAxNTYyfQ.n9lfkbdUjrkNQEit3VxUGoTBKMLrFsJw6eELs05zMZ4'
def print_config_status():
    """Print current configuration status"""
    print("📋 Configuration Status:")
    print(f"   Browser: {BROWSER_TYPE}")
    print(f"   AI Enabled: {'✅ Yes' if get_ai_enabled() else '❌ No (demo mode)'}")
    print(f"   Learning Enabled: {'✅ Yes' if HEALING_CONFIG['learning_enabled'] else '❌ No'}")