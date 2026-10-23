import sqlite3

import pytest

from ia_agent.storage import Store


@pytest.fixture
def store(tmp_path):
    result = Store(tmp_path / "data" / "test.sqlite3")
    result.initialize()
    return result


def test_persistence_and_repeatable_initialization(store):
    text_id = store.add_text(" Agua ", "El agua cambia de estado.", "Fuente propia")
    question_id = store.add_question(text_id, "¿Qué cambia?", "El agua.", "El agua")
    reopened = Store(store.path)
    reopened.initialize()
    assert reopened.texts()[0]["title"] == "Agua"
    assert reopened.texts()[0]["source"] == "Fuente propia"
    question = reopened.questions(text_id)[0]
    assert question["id"] == question_id
    assert question["answer"] == "El agua."
    assert question["evidence"] == "El agua"
    assert question["provider"] == "manual"


@pytest.mark.parametrize("title,body", [(" ", "texto"), ("título", "\n")])
def test_empty_text_rejected(store, title, body):
    with pytest.raises(ValueError):
        store.add_text(title, body)
    assert store.texts() == []


@pytest.mark.parametrize("changes", [
    {"prompt": " "}, {"answer": ""}, {"evidence": ""},
    {"evidence": "Inventado"}, {"dimension": "desconocida"}, {"text_id": 999},
])
def test_invalid_question_rejected(store, changes):
    text_id = store.add_text("Texto", "Texto verificable.")
    args = dict(text_id=text_id, prompt="¿Qué?", answer="Texto", evidence="Texto")
    args.update(changes)
    with pytest.raises(ValueError):
        store.add_question(**args)
    assert store.questions(text_id) == []


def test_parameterized_sql_and_text_isolation(store):
    body = "Robert'); DROP TABLE texts;--"
    first = store.add_text(body, body)
    second = store.add_text("Otro", "Otro texto")
    store.add_question(first, body, body, body)
    assert len(store.texts()) == 2
    assert store.questions(second) == []


def test_foreign_keys_enabled(store):
    with pytest.raises(sqlite3.IntegrityError), store.connect() as db:
        db.execute("""INSERT INTO questions(text_id,prompt,answer,evidence,dimension,provider)
                      VALUES (99,'q','a','e','literal','manual')""")


def test_future_schema_not_modified(store):
    with store.connect() as db:
        db.execute("PRAGMA user_version = 2")
    with pytest.raises(ValueError, match="Versión"):
        store.initialize()
