import os
import pandas as pd
from app.extensions import db
from app.management.init_variables import get_latest_record_by_object
from app.management.log_manager import log_register
from app.models.processamento import Processamento
import traceback

def insert_processamento_by_uuid(uuid, objeto):
    try:
        file_trace = os.path.join('app', 'trace', objeto)
        file_path = os.path.join(file_trace, f"{uuid}.csv")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo {uuid}.csv não encontrado na pasta {file_trace}")

        df = pd.read_csv(file_path, delimiter=';', index_col=False)
        df.replace({"**": 0, "nd": 0, "*": 0}, inplace=True)

        df = df.fillna(0)

        numeric_column = [col for col in df.columns if col.isdigit()]
        df[numeric_column] = df[numeric_column].map(lambda x: str(x).replace(',', '.') if isinstance(x, str) else x)

        totalizador = ''

        for _, row in df.iterrows():
            id = row['id']
            control = row['control']
            cultivar = row['cultivar']

            if cultivar.isupper():
                tipo = 'T'
                totalizador = cultivar
            else:
                tipo = 'I'

            anos_colunas = [col for col in df.columns if col.isdigit()]

            for ano in anos_colunas:
                quantidade = float(row[ano]) if isinstance(row[ano], str) else row[ano]

                novo_registro = Processamento(
                    uuid=uuid,
                    id=id,
                    control=control,
                    object=objeto,
                    cultivar=cultivar,
                    ano=int(ano),
                    quantidade=quantidade,
                    tipo=tipo,
                    totalizador=totalizador if tipo == 'I' else ''
                )
                db.session.add(novo_registro)

        db.session.commit()

    except FileNotFoundError as e:
        log_register(objeto, f"Erro: {e}\n{traceback.format_exc()}")
        raise
    except Exception as e:
        log_register(objeto, f"Erro ao processar o arquivo {uuid}.csv: {e}\n{traceback.format_exc()}")
        raise RuntimeError(f"Erro ao processar o arquivo {uuid}.csv: {e}")

def get_processamento(objeto, ano=None):
    try:
        latest_record = get_latest_record_by_object(objeto)

        uuid = latest_record.uuid
        record_date = latest_record.record_date
        object_modified_date = latest_record.object_modified_date

        query = db.session.query(Processamento).filter(Processamento.uuid == uuid, Processamento.object == objeto)

        if ano:
            query = query.filter(Processamento.ano == ano)

        tipos_cultivar = query.filter(Processamento.tipo == 'T').order_by(Processamento.id.asc(), Processamento.ano.desc()).all()

        result = {
            'last_uuid': uuid,
            'record_date': record_date.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'object_modified_data': object_modified_date.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'processamento': []
        }

        for tipo_cultivar in tipos_cultivar:
            ano_key = str(tipo_cultivar.ano)

            ano_json = next((item for item in result['processamento'] if item['ano'] == ano_key), None)

            if not ano_json:
                ano_json = {
                    'ano': ano_key,
                    'quantidade_total_kg': 0,
                    'tipos': []
                }
                result['processamento'].append(ano_json)

            ano_json['quantidade_total_kg'] += tipo_cultivar.quantidade

            tipo_cultivar_json = {
                'tipo_cultivar': tipo_cultivar.cultivar,
                'itens': [],
                'quantidade_tipo_kg': tipo_cultivar.quantidade
            }

            item_query = db.session.query(Processamento).filter(
                Processamento.uuid == uuid,
                Processamento.ano == tipo_cultivar.ano,
                Processamento.totalizador == tipo_cultivar.cultivar,
                Processamento.tipo == 'I'
            ).all()

            for item in item_query:
                item_data = {
                    'cultivar': item.cultivar,
                    'quantidade_cultivar_kg': item.quantidade
                }
                tipo_cultivar_json['itens'].append(item_data)

            ano_json['tipos'].append(tipo_cultivar_json)

        return result

    except Exception as e:
        log_register(objeto, f"Erro ao consultar {objeto}: {e}\n{traceback.format_exc()}")
        raise RuntimeError(f"Erro ao consultar {objeto}: {e}")
