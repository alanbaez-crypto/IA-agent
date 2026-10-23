"""Configuración explícita, sin secretos ni dependencia de servicios externos."""

import os
from pathlib import Path


def database_path() -> Path:
    return Path(os.environ.get("IA_AGENT_DB", "data/ia_agent.sqlite3"))
