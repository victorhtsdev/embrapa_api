import base64
from datetime import datetime
import os
import requests
import traceback
from flask import current_app
from sqlalchemy.exc import NoResultFound
from uuid import uuid1

from app.extensions import db
from app.models.data_log import DataLog
from app.management.file_manager import download_file
from app.management.init_variables import get_latest_record_by_object
from app.services.comercio_services import insert_comercio_by_uuid
from app.services.exportacao_services import insert_exportacao_by_uuid
from app.services.importacao_services import insert_importacao_by_uuid
from app.services.producao_services import insert_producao_by_uuid
from app.management.log_manager import log_register

def get_file_url(objeto):
    try:
        base_url = os.getenv('EMBRAPA_URL')
        if not base_url:
            raise EnvironmentError("Variável de ambiente EMBRAPA_URL não está definida.")

        file_env_var = f"{objeto.upper()}_FILE"
        file_name = os.getenv(file_env_var)
        if not file_name:
            raise EnvironmentError(f"Variável de ambiente {file_env_var} não está definida.")

        full_url = f"{base_url}{file_name}"
        return full_url

    except EnvironmentError as e:
        log_register(objeto, f"Erro de ambiente ao obter URL de {objeto}: {e}\n{traceback.format_exc()}")
        raise RuntimeError(f"Erro de ambiente ao obter URL de {objeto}: {e}")
    except Exception as e:
        log_register(objeto, f"Erro inesperado ao obter URL de {objeto}: {e}\n{traceback.format_exc()}")
        raise RuntimeError(f"Erro inesperado ao obter URL de {objeto}: {e}")

def get_data_from_embrapa(objeto):
    try:
        latest_record = get_latest_record_by_object(objeto)
        object_modified_date = None

        if latest_record:
            object_modified_date = latest_record.object_modified_date

        url = get_file_url(objeto)
        if not url:
            raise ValueError(f"URL para o objeto {objeto} não pôde ser construída.")

        response = requests.head(url)
        response.raise_for_status()

        http_modified = response.headers.get('Last-Modified')
        if not http_modified:
            raise ValueError(f"Data de modificação não encontrada para o objeto: {objeto}")

        http_modified = datetime.strptime(http_modified, '%a, %d %b %Y %H:%M:%S %Z')

        if object_modified_date and http_modified <= object_modified_date:
            return latest_record

        new_uuid = str(uuid1())
        destination = os.path.join('app', 'trace', objeto, f"{new_uuid}.csv")

        download_file(url, destination)

        if objeto == 'producao':
            insert_producao_by_uuid(new_uuid)
        elif objeto.startswith('exportacao'):
            insert_exportacao_by_uuid(new_uuid, objeto)
        elif objeto.startswith('importacao'):
            insert_importacao_by_uuid(new_uuid, objeto)
        elif objeto == 'comercio':
            insert_comercio_by_uuid(new_uuid)

        new_record = DataLog(
            uuid=new_uuid,
            object=objeto,
            record_date=datetime.utcnow(),
            object_modified_date=http_modified
        )
        db.session.add(new_record)
        db.session.commit()

        return new_record

    except requests.exceptions.RequestException as e:
        log_register(objeto, f"Erro ao obter dados do arquivo {objeto}: {e}\n{traceback.format_exc()}")
        raise RuntimeError(f"Erro ao obter dados do arquivo {objeto}: {e}")
    except ValueError as e:
        log_register(objeto, f"Erro de valor ao processar {objeto}: {e}\n{traceback.format_exc()}")
        raise RuntimeError(f"Erro de valor ao processar {objeto}: {e}")
    except Exception as e:
        log_register(objeto, f"Erro inesperado ao processar {objeto}: {e}\n{traceback.format_exc()}")
        raise RuntimeError(f"Erro inesperado ao processar {objeto}: {e}")

def get_data_log_by_uuid(uuid):
    try:
        data_log = db.session.query(DataLog).filter_by(uuid=uuid).one()
        file_path = os.path.join(current_app.root_path, 'trace', data_log.object, f"{uuid}.csv")

        try:
            with open(file_path, 'rb') as file:
                file_content = file.read()
                data_source_base64 = base64.b64encode(file_content).decode()
        except FileNotFoundError:
            data_source_base64 = ""

        result = {
            'uuid': data_log.uuid,
            'object': data_log.object,
            'record_date': data_log.record_date.strftime('%Y-%m-%dT%H:%M:%S'),
            'object_modified_date': data_log.object_modified_date.strftime('%Y-%m-%dT%H:%M:%S') if data_log.object_modified_date else None,
            'data_source': data_source_base64
        }

        return result

    except NoResultFound as e:
        raise ValueError(f"Nenhum registro encontrado para o UUID: {uuid}")
    except Exception as e:
        log_register('data_log', f"Erro ao acessar o banco de dados: {e}\n{traceback.format_exc()}")
        raise RuntimeError(f"Erro ao acessar o banco de dados: {e}")