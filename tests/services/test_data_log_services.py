import pytest
from app import create_app
from app.services.data_log_services import get_latest_record_by_object, get_production_file_url, get_data_from_embrapa
from app.extensions import db


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_latest_record_by_object_not_found(client):
    with client.application.app_context():  # Garante que o contexto de aplicação está ativo
        resultado = get_latest_record_by_object('exemplo_inexistente')
        assert resultado is None
        print("Nenhum registro encontrado para o objeto: exemplo_inexistente")

def test_get_production_file_url_producao(monkeypatch):
    monkeypatch.setenv('EMBRAPA_URL', 'http://vitibrasil.cnpuv.embrapa.br/download/')
    monkeypatch.setenv('PRODUCAO_FILE', 'Producao.csv')

    production_url = get_production_file_url('producao')
    assert production_url == 'http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv'
    print(f"URL para o arquivo de produção: {production_url}")

def test_get_data_from_embrapa_producao(monkeypatch, client):
    monkeypatch.setenv('EMBRAPA_URL', 'http://vitibrasil.cnpuv.embrapa.br/download/')
    monkeypatch.setenv('PRODUCAO_FILE', 'Producao.csv')

    with client.application.app_context():  # Garante que o contexto de aplicação está ativo
        last_modified = get_data_from_embrapa('producao')
        assert last_modified is not None, "A função não retornou Last-Modified."
        print(f"Data de modificação capturada: {last_modified}")


