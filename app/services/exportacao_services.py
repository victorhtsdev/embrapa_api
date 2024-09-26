import os
import pandas as pd
from app.extensions import db
from app.management.init_variables import get_latest_record_by_object
from app.models.exportacao import Exportacao
from app.management.log_manager import log_register
import traceback

def insert_exportacao_by_uuid(uuid, objeto):
    try:
        file_trace = os.path.join('app', 'trace', objeto)
        file_path = os.path.join(file_trace, f"{uuid}.csv")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo {uuid}.csv não encontrado na pasta {file_trace}")

        df = pd.read_csv(file_path, delimiter=';')

        df = df.fillna(0)

        colunas = df.columns
        index_inicio = colunas.get_loc('País') + 1

        anos_colunas = colunas[index_inicio:]

        for _, row in df.iterrows():
            id = row['Id']
            pais = row['País']

            # No CSV existem 2 colunas de ano, uma representa a quantidade outra o valor em U$
            for i in range(0, len(anos_colunas), 2):
                ano_quantidade = anos_colunas[i]
                ano_valor = anos_colunas[i + 1] if i + 1 < len(anos_colunas) else None

                quantidade = row[ano_quantidade]
                valor = row[ano_valor] if ano_valor else 0

                novo_registro = Exportacao(
                    uuid=uuid,
                    id=id,
                    object=objeto,
                    pais=pais,
                    ano=int(ano_quantidade),
                    quantidade=quantidade,
                    valor=valor
                )

                db.session.add(novo_registro)

        db.session.commit()

    except FileNotFoundError as e:
        log_register(objeto, f"Erro: {e}\n{traceback.format_exc()}")
        raise
    except Exception as e:
        log_register(objeto, f"Erro ao processar o arquivo {uuid}.csv: {e}\n{traceback.format_exc()}")
        raise RuntimeError(f"Erro ao processar o arquivo {uuid}.csv: {e}")

def get_exportacao(objeto, ano=None):
    try:
        latest_record = get_latest_record_by_object(objeto)

        uuid = latest_record.uuid
        record_date = latest_record.record_date
        object_modified_date = latest_record.object_modified_date

        query = db.session.query(Exportacao).filter(Exportacao.uuid == uuid, Exportacao.object == objeto)

        if ano:
            query = query.filter(Exportacao.ano == ano)

        paises = query.order_by(Exportacao.pais.asc(), Exportacao.ano.desc()).all()

        result = {
            'last_uuid': uuid,
            'record_date': record_date.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'object_modified_data': object_modified_date.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'exportacao': []
        }

        for pais in paises:
            ano_key = str(pais.ano)

            ano_json = next((item for item in result['exportacao'] if item['ano'] == ano_key), None)

            if not ano_json:
                ano_json = {
                    'ano': ano_key,
                    'objeto': objeto,
                    'quantidade_total': 0,
                    'valor_total': 0,
                    'paises': []
                }
                result['exportacao'].append(ano_json)

            ano_json['quantidade_total'] += pais.quantidade
            ano_json['valor_total'] += pais.valor

            pais_json = {
                'pais': pais.pais,
                'quantidade_pais': pais.quantidade,
                'valor_pais': pais.valor
            }

            ano_json['paises'].append(pais_json)

        return result

    except Exception as e:
        log_register(objeto, f"Erro ao consultar {objeto}: {e}\n{traceback.format_exc()}")
        raise RuntimeError(f"Erro ao consultar exportações: {e}")