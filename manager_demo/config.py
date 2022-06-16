from pathlib import Path

def get_config(config="debug"):
    """Return the config file."""
    return str(Path(__file__).parents[1] / "manager_demo_configs" / f"{config}.json")
