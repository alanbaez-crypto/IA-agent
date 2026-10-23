"""Copias consistentes y recuperación sin sobrescribir archivos existentes."""

import argparse
import sqlite3
from contextlib import closing
from pathlib import Path

from ia_agent.config import database_path


def verify(path: Path):
    with closing(sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)) as db:
        if db.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
            raise ValueError("La copia no supera integrity_check.")
        if db.execute("PRAGMA foreign_key_check").fetchall():
            raise ValueError("La copia contiene referencias inválidas.")
        if db.execute("PRAGMA user_version").fetchone()[0] != 1:
            raise ValueError("Versión de base no compatible.")
        db.execute("SELECT id, title, body, source, created_at FROM texts LIMIT 1")
        db.execute("SELECT id, text_id, prompt, answer, evidence, dimension, provider, created_at FROM questions LIMIT 1")


def copy_database(source: Path, destination: Path):
    verify(source)
    destination.parent.mkdir(parents=True, exist_ok=True)
    # Reserva exclusiva: nunca sobrescribir una base o copia previa.
    with destination.open("xb"):
        pass
    try:
        with closing(sqlite3.connect(source.resolve().as_uri() + "?mode=ro", uri=True)) as src:
            with closing(sqlite3.connect(destination)) as dst:
                src.backup(dst)
        verify(destination)
    except Exception:
        destination.unlink(missing_ok=True)
        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("backup", "verify", "restore"))
    parser.add_argument("file", type=Path, help="Ruta de la copia")
    args = parser.parse_args()
    try:
        if args.command == "verify":
            verify(args.file)
        elif args.command == "backup":
            copy_database(database_path(), args.file)
        else:
            copy_database(args.file, database_path())
    except (OSError, sqlite3.Error, ValueError) as exc:
        parser.exit(1, f"Error: {exc}\n")
    print("Operación completada y base verificada.")


if __name__ == "__main__":
    main()
