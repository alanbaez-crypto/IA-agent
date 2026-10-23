"""Persistencia SQLite; cada operación abre y cierra su propia conexión."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

DIMENSIONS = ("literal", "cohesión", "macroestructura", "inferencia")


def required(value: str, name: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError(f"{name} no puede estar vacío.")
    return value


class Store:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    @contextmanager
    def connect(self):
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        try:
            with connection:
                yield connection
        finally:
            connection.close()

    def initialize(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            version = db.execute("PRAGMA user_version").fetchone()[0]
            if version not in (0, 1):
                raise ValueError("Versión de base no compatible. Conserva una copia antes de migrar.")
            db.execute("""CREATE TABLE IF NOT EXISTS texts (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL CHECK(length(trim(title)) > 0),
                body TEXT NOT NULL CHECK(length(trim(body)) > 0),
                source TEXT NOT NULL DEFAULT '',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )""")
            db.execute("""CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                text_id INTEGER NOT NULL REFERENCES texts(id),
                prompt TEXT NOT NULL CHECK(length(trim(prompt)) > 0),
                answer TEXT NOT NULL CHECK(length(trim(answer)) > 0),
                evidence TEXT NOT NULL CHECK(length(trim(evidence)) > 0),
                dimension TEXT NOT NULL CHECK(dimension IN
                    ('literal', 'cohesión', 'macroestructura', 'inferencia')),
                provider TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )""")
            db.execute("PRAGMA user_version = 1")

    def add_text(self, title: str, body: str, source: str = "") -> int:
        title, body = required(title, "Título"), required(body, "Texto")
        with self.connect() as db:
            return db.execute(
                "INSERT INTO texts(title, body, source) VALUES (?, ?, ?)",
                (title, body, source.strip()),
            ).lastrowid

    def texts(self) -> list[dict]:
        with self.connect() as db:
            return [dict(row) for row in db.execute("SELECT * FROM texts ORDER BY id DESC")]

    def add_question(self, text_id: int, prompt: str, answer: str, evidence: str,
                     dimension: str = "literal", provider: str = "manual") -> int:
        prompt = required(prompt, "Pregunta")
        answer = required(answer, "Respuesta")
        evidence = required(evidence, "Evidencia")
        if dimension not in DIMENSIONS:
            raise ValueError("Dimensión no válida.")
        with self.connect() as db:
            row = db.execute("SELECT body FROM texts WHERE id = ?", (text_id,)).fetchone()
            if row is None:
                raise ValueError("El texto no existe.")
            if evidence not in row["body"]:
                raise ValueError("La evidencia debe ser una cita literal del texto.")
            return db.execute(
                """INSERT INTO questions(text_id, prompt, answer, evidence, dimension, provider)
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (text_id, prompt, answer, evidence, dimension, provider),
            ).lastrowid

    def questions(self, text_id: int) -> list[dict]:
        with self.connect() as db:
            return [dict(row) for row in db.execute(
                "SELECT * FROM questions WHERE text_id = ? ORDER BY id DESC", (text_id,)
            )]
