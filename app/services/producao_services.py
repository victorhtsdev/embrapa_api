import os
import pandas as pd
from app.extensions import db
from app.models.producao import Producao
from app.management.init_variables import get_latest_record_by_object


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
        print(f"Arquivo {uuid}.csv lido e registros inseridos com sucesso.")

    except FileNotFoundError as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro ao processar o arquivo {uuid}.csv: {e}")

def get_producao(ano=None):
    try:
        latest_record = get_latest_record_by_object("producao")

        uuid = latest_record.uuid
        record_date = latest_record.record_date
        object_modified_date = latest_record.object_modified_date

        query = db.session.query(Producao).filter(Producao.uuid == uuid)

        if ano:
            query = query.filter(Producao.ano == ano)

        totalizadores = query.filter(Producao.tipo == 'T').order_by(Producao.id.asc(), Producao.ano.desc()).all()

        resultado = {
            'uuid': uuid,
            'record_date': record_date,
            'object_modified_data': object_modified_date,
            'producao': {}
        }
        ano_atual = None

        for totalizador in totalizadores:
            ano_key = str(totalizador.ano)

            if ano_key != ano_atual:
                ano_atual = ano_key
                if ano_key not in resultado['producao']:
                    resultado['producao'][ano_key] = {
                        'total': 0,  # Inicializa a soma total para o ano
                    }

            resultado['producao'][ano_key]['total'] += totalizador.quantidade

            resultado['producao'][ano_key][totalizador.produto] = {
                'quantidade': totalizador.quantidade,
                'itens': []
            }

            itens_query = db.session.query(Producao).filter(
                Producao.uuid == uuid,
                Producao.ano == totalizador.ano,
                Producao.totalizador == totalizador.produto,
                Producao.tipo == 'I'
            ).all()

            for item in itens_query:
                item_data = {
                    'produto': item.produto,
                    'quantidade': item.quantidade
                }
                resultado['producao'][ano_key][totalizador.produto]['itens'].append(item_data)

        return resultado

    except Exception as e:
        raise RuntimeError(f"Erro ao consultar produções: {e}")