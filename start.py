import subprocess
import os
from datetime import datetime
from log_config import setup_logger

logger = setup_logger('start')

def print_separator(char='=', length=80):
    logger.info(f"\n{char * length}")

def run_script(script_name):
    try:
        print_separator()
        logger.info(f"→ Executando {script_name}")
        print_separator('-')

        result = subprocess.run(
            ['python', script_name],
            capture_output=False,
            text=True,
            check=False
        )

        if result.returncode != 0:
            logger.error(f"❌ {script_name} falhou")
        else:
            logger.info(f"✅ {script_name} concluído")

    except Exception as e:
        logger.error(f"❌ Erro ao executar {script_name}: {str(e)}")

def main():
    start_time = datetime.now()

    try:
        logger.info("→ Iniciando processo de importação")
        
        run_script('get_json.py')
        run_script('sync.py')
        
        execution_time = datetime.now() - start_time
        
        print_separator()
        logger.info(f"Processo concluído em {execution_time}")
        print_separator()
        
    except Exception as e:
        logger.error(f"❌ Erro no processo: {str(e)}")

if __name__ == '__main__':
    main()