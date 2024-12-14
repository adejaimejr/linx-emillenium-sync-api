# Linx e-Millenium Sync API

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![MongoDB](https://img.shields.io/badge/MongoDB-4.4%2B-green)
![License](https://img.shields.io/badge/license-MIT-blue)

Sistema de sincronização de dados entre a API do e-Millenium (Linx) e MongoDB, projetado para manter bases de dados atualizadas de forma eficiente e automatizada.

## 🚀 Funcionalidades

- Sincronização automática de dados do e-Millenium para MongoDB
- Suporte para múltiplas coleções (lançamentos, geradores, etc.)
- Sistema de logging configurável
- Controle de arquivos processados
- Tratamento de datas e campos específicos
- Modo de teste e produção configuráveis

## 📋 Pré-requisitos

- Python 3.8 ou superior
- MongoDB 4.4 ou superior
- Credenciais de acesso à API do e-Millenium
- Conexão com MongoDB configurada

## 🔧 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/linx-emillenium-sync-api.git
cd linx-emillenium-sync-api


2. Instale as dependências:

bash
pip install -r requirements.txt


3. Configure o arquivo `.env`:
env
MONGO_URI=sua_uri_mongodb
API_USERNAME=seu_usuario
API_PASSWORD=sua_senha
ENVIRONMENT=test
LOG_LEVEL=INFO
LOG_MODE=SINGLE


## 💻 Uso

Execute o script principal:
bash
python start.py


### Configurações de Log

- `LOG_LEVEL`: Define o nível de detalhamento dos logs
  - `DEBUG`: Logs detalhados para desenvolvimento
  - `INFO`: Logs básicos de operação (recomendado para produção)

- `LOG_MODE`: Define o modo de armazenamento dos logs
  - `SINGLE`: Mantém logs em arquivos únicos (application.log/debug.log)
  - `MULTIPLE`: Cria arquivos separados por execução

## 🗂 Estrutura do Projeto
linx-emillenium-sync-api/
├── start.py # Script principal
├── get_json.py # Obtém dados da API
├── sync.py # Sincroniza com MongoDB
├── log_config.py # Configuração de logs
├── requirements.txt # Dependências
├── .env # Configurações
└── logs/ # Diretório de logs


## 🔄 Fluxo de Dados

1. `get_json.py`: 
   - Conecta à API do e-Millenium
   - Obtém dados atualizados
   - Salva em arquivos JSON

2. `sync.py`:
   - Lê arquivos JSON
   - Processa e transforma dados
   - Sincroniza com MongoDB

## ⚙️ Configuração

### Coleções Suportadas

- Lançamentos
- Geradores
- (Outras coleções podem ser adicionadas conforme necessário)

### Variáveis de Ambiente

| Variável | Descrição | Exemplo |
|----------|-----------|---------|
| MONGO_URI | URI de conexão MongoDB | mongodb://localhost:27017 |
| API_USERNAME | Usuário da API | user |
| API_PASSWORD | Senha da API | pass |
| ENVIRONMENT | Ambiente (test/production) | test |
| LOG_LEVEL | Nível de log | INFO |
| LOG_MODE | Modo de log | SINGLE |

## 📊 Monitoramento

- Logs detalhados em `logs/`
- Controle de arquivos processados em `processed_files.md`
- Resumo de execução com estatísticas

## 🛠️ Desenvolvimento

Para contribuir com o projeto:

1. Fork o repositório
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 License

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👥 Autores

* **Seu Nome** - *Desenvolvimento Inicial* - [seu-usuario](https://github.com/seu-usuario)

## 🎁 Agradecimentos

* Linx pelo suporte à API
* Comunidade MongoDB
* Contribuidores do projeto

---
⌨️ com ❤️ por [seu-nome](https://github.com/seu-usuario)