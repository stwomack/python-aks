import os
from pathlib import Path

def load_config():
    """
    Load configuration from config.env file
    Returns a dictionary with all configuration values
    """
    config_file = Path("config.env")
    
    if not config_file.exists():
        raise FileNotFoundError(f"Configuration file {config_file} not found!")
    
    config = {}
    
    with open(config_file, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line.startswith('#') or not line:
                continue
            
            # Parse key=value pairs
            if '=' in line:
                key, value = line.split('=', 1)
                config[key.strip()] = value.strip()
    
    return config

def get_env_var(key, default=None):
    """
    Get environment variable, with fallback to config file
    """
    # First try to get from environment
    value = os.environ.get(key)
    if value is not None:
        return value
    
    # Fallback to config file
    try:
        config = load_config()
        return config.get(key, default)
    except FileNotFoundError:
        return default

# Load configuration on module import
try:
    CONFIG = load_config()
except FileNotFoundError:
    CONFIG = {}

# Export commonly used variables
TEMPORAL_ADDRESS = get_env_var("TEMPORAL_ADDRESS", "localhost:7233")
TEMPORAL_NAMESPACE = get_env_var("TEMPORAL_NAMESPACE", "default")
TEMPORAL_TASK_QUEUE = get_env_var("TEMPORAL_TASK_QUEUE", "test-task-queue")
TEMPORAL_API_KEY = get_env_var("TEMPORAL_API_KEY", "demo-api-key")
KEYVAULT_URL = os.environ["KEYVAULT_URL"]
KEYVAULT_SECRET_NAME = os.environ["KEYVAULT_SECRET_NAME"] 
