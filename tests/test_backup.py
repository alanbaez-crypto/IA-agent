import sqlite3
import pytest

from ia_agent.backup import copy_database, verify
from ia_agent.storage import Store


def test_backup_and_restore_preserve_data(tmp_path):
    source = Store(tmp_path / "source.sqlite3")
    source.initialize()
    key = source.add_text("Lluvia", "La lluvia aporta agua.")
    source.add_question(key, "¿Qué aporta?", "Agua", "agua")
    backup, restored = tmp_path / "backup.sqlite3", tmp_path / "restored.sqlite3"
    copy_database(source.path, backup)
    copy_database(backup, restored)
    verify(restored)
    assert Store(restored).texts() == source.texts()
    assert Store(restored).questions(key) == source.questions(key)
    with pytest.raises(FileExistsError):
        copy_database(source.path, restored)
    assert Store(restored).questions(key) == source.questions(key)


def test_missing_source_not_created(tmp_path):
    missing = tmp_path / "missing.sqlite3"
    with pytest.raises(sqlite3.Error):
        copy_database(missing, tmp_path / "backup.sqlite3")
    assert not missing.exists()


def test_invalid_backup_rejected(tmp_path):
    bad = tmp_path / "bad.sqlite3"
    bad.write_text("no es SQLite", encoding="utf-8")
    with pytest.raises(sqlite3.Error):
        verify(bad)


def test_empty_sqlite_not_accepted(tmp_path):
    bad = tmp_path / "empty.sqlite3"
    with sqlite3.connect(bad):
        pass
    with pytest.raises(ValueError, match="Versión"):
        verify(bad)
