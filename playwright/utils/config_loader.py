import os

def get_config():
    env = os.getenv("ENV", "dev").lower()

    if env == "dev":
        from config.dev_config import DevConfig
        return DevConfig()
    elif env == "qa":
        from config.qa_config import QAConfig
        return QAConfig()
    elif env == "stg":
        from config.stg_config import StgConfig
        return StgConfig()
    else:
        raise ValueError(f"Invalid environment provided: {env}. Try again with a valid environment (dev, qa, stg).")
    