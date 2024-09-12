import pytest
from app import create_app
from app.services.data_log_services import get_latest_record_by_object, get_production_file_url, get_data_from_embrapa
from app.extensions import db
from app.services.producao_services import insert_producao_by_uuid

pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()

@pytest.fixture
def client(app):
    return app.test_client()

def test_consultar_produto_por_uuid(monkeypatch, client):
    monkeypatch.setenv('EMBRAPA_URL', 'http://vitibrasil.cnpuv.embrapa.br/download/')
    monkeypatch.setenv('PRODUCAO_FILE', 'Producao.csv')

    insert_producao_by_uuid('75614be6-6d27-11ef-94d3-c8cb9ee39576')
