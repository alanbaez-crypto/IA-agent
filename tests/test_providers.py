import json
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from ia_agent.providers import MockProvider, OllamaProvider, ProviderError, configured_provider


def test_mock_grounded_and_deterministic():
    text = "La lectura relaciona ideas del texto."
    question = MockProvider().generate(text)
    assert question == MockProvider().generate(text)
    assert question.evidence in text
    assert question.answer == text
    assert question.dimension == "literal"


def test_default_needs_no_credentials(monkeypatch):
    monkeypatch.delenv("IA_AGENT_PROVIDER", raising=False)
    assert isinstance(configured_provider(), MockProvider)


def test_configuration_errors(monkeypatch):
    monkeypatch.setenv("IA_AGENT_PROVIDER", "paid-api")
    with pytest.raises(ProviderError):
        configured_provider()
    with pytest.raises(ProviderError):
        OllamaProvider("")


@pytest.mark.parametrize("url", ["https://example.com", "http://example.com",
    "http://user:password@localhost:11434", "http://localhost/api", "file:///tmp/model"])
def test_remote_ollama_rejected(url):
    with pytest.raises(ProviderError):
        OllamaProvider("existing-model", url)


@pytest.fixture
def server():
    state = {"status": 200, "body": {}, "request": None, "path": None}

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):
            state["path"] = self.path
            state["request"] = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
            self.send_response(state["status"])
            self.end_headers()
            self.wfile.write(json.dumps(state["body"]).encode())

        def log_message(self, *_):
            pass

    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    worker = threading.Thread(target=httpd.serve_forever, daemon=True)
    worker.start()
    yield state, f"http://127.0.0.1:{httpd.server_port}"
    httpd.shutdown()
    httpd.server_close()
    worker.join()


def test_ollama_http_contract(server):
    state, url = server
    state["body"] = {"response": json.dumps(dict(prompt="¿Qué se relaciona?",
        answer="Ideas", evidence="ideas", dimension="cohesión"))}
    result = OllamaProvider("existing-model", url).generate("El texto relaciona ideas.")
    assert result.answer == "Ideas"
    assert state["path"] == "/api/generate"
    assert state["request"]["model"] == "existing-model"
    assert state["request"]["stream"] is False
    assert state["request"]["format"] == "json"
    assert state["request"]["prompt"] == "El texto relaciona ideas."


@pytest.mark.parametrize("body", [{}, {"response": "no JSON"}, {"response": "[]"},
    {"response": json.dumps(dict(prompt="q", answer="a", evidence="inventada", dimension="literal"))},
    {"response": json.dumps(dict(prompt="q", answer="a", evidence="texto", dimension="otra"))},
    {"response": json.dumps(dict(prompt="q", answer=3, evidence="texto", dimension="literal"))}])
def test_invalid_ollama_response(server, body):
    state, url = server
    state["body"] = body
    with pytest.raises(ProviderError, match="JSON válida"):
        OllamaProvider("existing-model", url).generate("texto")


def test_missing_model_http_error(server):
    state, url = server
    state["status"] = 404
    with pytest.raises(ProviderError, match="404"):
        OllamaProvider("missing", url).generate("texto")
