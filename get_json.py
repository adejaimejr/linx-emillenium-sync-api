import os
import requests
import json
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime
from log_config import setup_logger

logger = setup_logger('get_json')

def get_max_trans_id(collection):
    try:
        max_trans_id_doc = collection.find_one(sort=[("trans_id", -1)])
        max_trans_id = max_trans_id_doc['trans_id'] if max_trans_id_doc else 0
        logger.info(f"  ℹ Maior trans_id encontrado: {max_trans_id}")
        return max_trans_id
    except Exception as e:
        logger.error(f"  ✗ Erro ao obter o maior trans_id: {e}")
        return 0

def fetch_data_from_api(api_url, trans_id, username, password):
    try:
        api_url = api_url.replace('{{trans_id}}', str(trans_id))
        logger.info(f"  → Buscando dados da API...")
        logger.debug(f"  URL: {api_url}")
        
        response = requests.get(api_url, auth=(username, password))
        response.raise_for_status()
        
        data = response.json()
        items_count = len(data.get('value', []))
        logger.info(f"  ✓ Dados obtidos com sucesso: {items_count} registros")
        return data
    except requests.RequestException as e:
        logger.error(f"  ✗ Erro ao buscar dados da API: {e}")
        return None

def save_data_to_json(data, directory, collection_name):
    try:
        os.makedirs(directory, exist_ok=True)
        items = data.get('value', [])
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_path = os.path.join(directory, f'{collection_name}_{timestamp}.json')
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(items, file, ensure_ascii=False, indent=4)
        
        logger.info(f"  ✓ Dados salvos em: {file_path}")
        logger.info(f"  ℹ Total de registros: {len(items)}")
        return file_path
    except Exception as e:
        logger.error(f"  ✗ Erro ao salvar dados em JSON: {e}")
        return None

def main():
    start_time = datetime.now()
    load_dotenv()

    mongo_uri = os.getenv('MONGO_URI')
    username = os.getenv('API_USERNAME')
    password = os.getenv('API_PASSWORD')
    mongo_database = os.getenv('MONGO_DATABASE')

    try:
        client = MongoClient(mongo_uri)
        logger.info('\n  Conectando ao MongoDB...')
        client.admin.command('ping')
        logger.info('  ✓ Conectado ao MongoDB com sucesso')

        # Configuração das coleções
        collections = {
            'lancamentos': {
                'collection_name': 'lancamentos',
                'api_url': os.getenv('API_URL_LANCAMENTOS')
            },
            'geradores': {
                'collection_name': 'geradores',
                'api_url': os.getenv('API_URL_GERADORES')
            }
            # Adicione outras coleções conforme necessário
        }

        for key, config in collections.items():
            logger.info(f"\n{'-'*80}")
            logger.info(f"  Processando coleção: {key}")
            
            collection_name = config['collection_name']
            api_url = config['api_url']
            
            if not api_url:
                logger.error(f"  ✗ URL da API não configurada para {collection_name}")
                continue

            db = client[mongo_database]
            collection = db[collection_name]

            max_trans_id = get_max_trans_id(collection)
            data = fetch_data_from_api(api_url, max_trans_id, username, password)
            
            if data:
                saved_file = save_data_to_json(data, 'json', collection_name)
                if saved_file:
                    logger.info(f"  ✓ Processamento completo para {collection_name}")
                else:
                    logger.error(f"  ✗ Falha ao salvar dados para {collection_name}")
            else:
                logger.error(f"  ✗ Falha ao obter dados para {collection_name}")

    except Exception as e:
        logger.error(f'  ✗ Ocorreu um erro: {e}')
    finally:
        client.close()
        execution_time = datetime.now() - start_time
        
        logger.info(f"\n{'='*80}")
        logger.info(f"  Resumo da Execução:")
        logger.info(f"  ⏱ Tempo de execução: {execution_time}")
        logger.info(f"  ✓ Conexão com MongoDB fechada")
        logger.info(f"{'='*80}\n")

if __name__ == '__main__':
    main()