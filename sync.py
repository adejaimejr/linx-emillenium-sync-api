import os
import json
import re
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime, timedelta
from log_config import setup_logger

logger = setup_logger('sync')

def parse_date(ms_string):
    if ms_string:
        match = re.match(r'/Date\((\d+)([+-]\d{3,4})?\)/', ms_string)
        if match:
            try:
                timestamp_ms = int(match.group(1))
                offset_str = match.group(2)
                offset_minutes = int(offset_str) if offset_str else 0

                timestamp_sec = int(timestamp_ms / 1000)
                date = datetime(1970, 1, 1) + timedelta(seconds=timestamp_sec)
                date += timedelta(minutes=offset_minutes)
                date_str = date.strftime('%Y-%m-%d')

                return timestamp_sec, date_str
            except Exception as e:
                logger.error(f"Erro ao converter data '{ms_string}': {e}")
                return None, None
        else:
            logger.warning(f"Formato de data não reconhecido: {ms_string}")
            return None, None
    return None, None

def get_processed_files():
    try:
        if os.path.exists('processed_files.md'):
            with open('processed_files.md', 'r') as file:
                processed_files = set(file.read().splitlines())
                logger.info(f"Arquivos processados carregados: {len(processed_files)} arquivos")
                logger.debug(f"Lista completa: {processed_files}")
                return processed_files
        else:
            logger.info("Nenhum arquivo processado encontrado.")
            return set()
    except Exception as e:
        logger.error(f"Erro ao carregar arquivos processados: {e}")
        return set()

def mark_file_as_processed(filename):
    try:
        with open('processed_files.md', 'a') as file:
            file.write(f"{filename}\n")
        logger.info(f"✓ Arquivo marcado como processado: {filename}")
    except Exception as e:
        logger.error(f"Erro ao marcar arquivo como processado: {e}")

def process_file(file_path, collection, chave):
    success_count = 0
    error_count = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            logger.info(f"Arquivo carregado: {file_path}")
            logger.info(f"Total de documentos: {len(data)}")

            for doc in data:
                try:
                    # Converter campos de data
                    for field in ['data', 'data_vencimento', 'data_pagamento']:
                        if field in doc:
                            timestamp, date_str = parse_date(doc[field])
                            if timestamp:
                                doc[f"{field}_timestamp"] = timestamp
                                doc[field] = date_str

                    # Criar novo documento com a chave como _id
                    new_doc = doc.copy()
                    if chave in new_doc:
                        new_doc['_id'] = new_doc[chave]

                    # Atualizar ou inserir documento
                    collection.replace_one(
                        {'_id': new_doc['_id']},
                        new_doc,
                        upsert=True
                    )
                    success_count += 1

                    if success_count % 100 == 0:
                        logger.info(f"↻ Processados {success_count} documentos...")
                except Exception as e:
                    error_count += 1
                    logger.error(f"✗ Erro ao processar documento {new_doc[chave]}: {e}")

            logger.info(f"\nResumo do processamento:")
            logger.info(f"✓ Documentos processados com sucesso: {success_count}")
            if error_count > 0:
                logger.error(f"✗ Documentos com erro: {error_count}")

    except Exception as e:
        logger.error(f"Erro ao processar arquivo {file_path}: {e}")

def main():
    load_dotenv()
    mongo_uri = os.getenv('MONGO_URI')
    environment = os.getenv('ENVIRONMENT', 'test').lower()
    mongo_database = os.getenv('MONGO_DATABASE')

    try:
        client = MongoClient(mongo_uri)
        logger.info('Conectando ao MongoDB...')
        client.admin.command('ping')
        logger.info('✓ Conectado ao MongoDB com sucesso')
    except Exception as e:
        logger.error(f"✗ Erro ao conectar ao MongoDB: {e}")
        return

    processed_files = get_processed_files()
    json_directory = 'json'

    if not os.path.exists(json_directory):
        logger.error(f"✗ Diretório {json_directory} não encontrado.")
        return

    files_processed = 0
    for filename in os.listdir(json_directory):
        if filename.endswith('.json') and filename not in processed_files:
            files_processed += 1
            base_collection_name = filename.split('_')[0]
            collection_name = base_collection_name if environment == 'production' else f"{base_collection_name}_teste"
            chave_key = f'COLLECTION_{base_collection_name.upper()}_CHAVE'
            chave = os.getenv(chave_key)

            if not chave:
                logger.warning(f"⚠ Chave não encontrada para a coleção {base_collection_name}")
                continue

            db = client[mongo_database]
            collection = db[collection_name]

            file_path = os.path.join(json_directory, filename)

            logger.info(f"\n{'-'*80}")
            logger.info(f"Processando: {filename}")
            logger.info(f"Coleção: {collection_name}")
            logger.info(f"Chave: {chave}")
            
            process_file(file_path, collection, chave)
            mark_file_as_processed(filename)

    client.close()
    logger.info(f"\n{'='*80}")
    logger.info(f"Resumo da Execução:")
    logger.info(f"✓ Arquivos processados: {files_processed}")
    logger.info(f"✓ Conexão com MongoDB fechada")
    logger.info(f"{'='*80}")

if __name__ == '__main__':
    main()