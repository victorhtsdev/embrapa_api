import os
import pandas as pd
from app.extensions import db
from app.models.producao import Producao
from app.management.init_variables import get_latest_record_by_object
from app.management.log_manager import log_register
import traceback

def insert_producao_by_uuid(uuid):
    try:
        file_trace = os.path.join('app', 'trace', 'producao')
        file_path = os.path.join(file_trace, f"{uuid}.csv")

        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Arquivo {uuid}.csv não encontrado na pasta {file_trace}")

        df = pd.read_csv(file_path, delimiter=';')

        totalizador = ''

        for _, row in df.iterrows():
            id = row['id']
            control = row['control']
            produto = row['produto']

            if produto.isupper():
                tipo = 'T'
                totalizador = produto
            else:
                tipo = 'I'

            anos_colunas = [col for col in df.columns if col.isdigit()]

            for ano in anos_colunas:
                quantidade = row[ano]
                novo_registro = Producao(
                    uuid=uuid,
                    id=id,
                    control=control,
                    produto=produto,
                    ano=int(ano),
                    quantidade=quantidade,
                    tipo=tipo,
                    totalizador=totalizador if tipo == 'I' else ''
                )

                db.session.add(novo_registro)

        db.session.commit()

    except FileNotFoundError as e:
        log_register('producao', f"Erro: {e}\n{traceback.format_exc()}")
        raise
    except Exception as e:
        log_register('producao', f"Erro ao processar o arquivo {uuid}.csv: {e}\n{traceback.format_exc()}")
        raise RuntimeError(f"Erro ao processar o arquivo {uuid}.csv: {e}")

def get_producao(ano=None):
    try:
        latest_record = get_latest_record_by_object("producao")

        uuid = latest_record.uuid
        record_date = latest_record.record_date
        object_modified_date = latest_record.object_modified_date

        query = db.session.query(Producao).filter(Producao.uuid == uuid)

        if ano:
            query = query.filter(Producao.ano == ano)

        tipo_produtos = query.filter(Producao.tipo == 'T').order_by(Producao.id.asc(), Producao.ano.desc()).all()

        result = {
            'last_uuid': uuid,
            'record_date': record_date.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'object_modified_data': object_modified_date.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'producao': []
        }

        for tipo_produto in tipo_produtos:
            ano_key = str(tipo_produto.ano)

            ano_json = next((item for item in result['producao'] if item['ano'] == ano_key), None)

            if not ano_json:
                ano_json = {
                    'ano': ano_key,
                    'quantidade_total': 0,
                    'tipos': []
                }
                result['producao'].append(ano_json)

            ano_json['quantidade_total'] += tipo_produto.quantidade

            tipo_produto_json = {
                'tipo_produto': tipo_produto.produto,
                'itens': [],
                'quantidade_tipo': tipo_produto.quantidade
            }

            item_query = db.session.query(Producao).filter(
                Producao.uuid == uuid,
                Producao.ano == tipo_produto.ano,
                Producao.totalizador == tipo_produto.produto,
                Producao.tipo == 'I'
            ).all()

            for item in item_query:
                item_data = {
                    'produto': item.produto,
                    'quantidade_produto': item.quantidade
                }
                tipo_produto_json['itens'].append(item_data)

            ano_json['tipos'].append(tipo_produto_json)

        return result

    except Exception as e:
        log_register('producao', f"Erro ao consultar producao: {e}\n{traceback.format_exc()}")
        raise RuntimeError(f"Erro ao consultar produções: {e}")

