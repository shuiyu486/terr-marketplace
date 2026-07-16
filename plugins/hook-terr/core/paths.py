import os


def claude_config_dir() -> str:
    configured = str(os.environ.get("CLAUDE_CONFIG_DIR", "")).strip()
    if configured:
        return os.path.abspath(os.path.expandvars(os.path.expanduser(configured)))
    return os.path.join(os.path.expanduser("~"), ".claude")


def hook_terr_dir() -> str:
    return os.path.join(claude_config_dir(), "hook-terr")
