import logging
import os
from datetime import datetime
from dotenv import load_dotenv

def setup_logger(script_name):
    # Carregar configurações do .env
    load_dotenv()
    log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
    log_mode = os.getenv('LOG_MODE', 'SINGLE').upper()
    
    # Criar diretório de logs se não existir
    os.makedirs('logs', exist_ok=True)
    
    # Configurar logger
    logger = logging.getLogger(script_name)
    logger.setLevel(getattr(logging, log_level))
    
    # Remover handlers existentes para evitar duplicação
    logger.handlers = []
    
    # Formatador para logs
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_formatter = logging.Formatter('%(message)s')  # Formato simplificado para console
    
    if log_mode == 'SINGLE':
        if log_level == 'DEBUG':
            # Se LOG_LEVEL=DEBUG, grava tudo no debug.log
            file_handler = logging.FileHandler('logs/debug.log', encoding='utf-8', mode='a')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        else:
            # Se LOG_LEVEL=INFO (ou outro), grava no application.log
            file_handler = logging.FileHandler('logs/application.log', encoding='utf-8', mode='a')
            file_handler.setLevel(getattr(logging, log_level))
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
    else:
        # Logs separados por execução
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_handler = logging.FileHandler(f"logs/{script_name}_{timestamp}.log", encoding='utf-8')
        file_handler.setLevel(getattr(logging, log_level))
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Adicionar handler para console (apenas uma vez)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level))
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger