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
- Processamento em lote de dados
- Sistema de retry para falhas de conexão
- Validação automática de dados

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
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure o arquivo `.env`:
```env
MONGO_URI=sua_uri_mongodb
API_USERNAME=seu_usuario
API_PASSWORD=sua_senha
ENVIRONMENT=test
LOG_LEVEL=INFO
LOG_MODE=SINGLE
MONGO_DATABASE=emillenium_sync
```

## 💻 Uso

Execute o script principal:
```bash
python start.py
```

### Configurações de Log

- `LOG_LEVEL`: Define o nível de detalhamento dos logs
  - `DEBUG`: Logs detalhados para desenvolvimento
  - `INFO`: Logs básicos de operação (recomendado para produção)

- `LOG_MODE`: Define o modo de armazenamento dos logs
  - `SINGLE`: Mantém logs em arquivos únicos (application.log/debug.log)
  - `MULTIPLE`: Cria arquivos separados por execução

## 💡 Boas Práticas

- Mantenha o arquivo `.env` sempre local e nunca o compartilhe
- Use o modo `test` antes de executar em produção
- Monitore os logs regularmente
- Faça backup do MongoDB antes de sincronizações grandes
- Configure adequadamente os timeouts da API

## ❗ Tratamento de Erros

O sistema possui tratamento para:
- Falhas de conexão com a API
- Erros de autenticação
- Problemas de formato de dados
- Timeouts de conexão
- Erros de validação de dados

## 🔍 Debugging

Para debug mais detalhado:
1. Configure `LOG_LEVEL=DEBUG` no `.env`
2. Verifique os logs em `logs/debug.log`
3. Use o modo de teste com `ENVIRONMENT=test`

## 🗂 Estrutura do Projeto
```
linx-emillenium-sync-api/
├── start.py           # Script principal
├── get_json.py        # Obtém dados da API
├── sync.py           # Sincroniza com MongoDB
├── log_config.py     # Configuração de logs
├── requirements.txt  # Dependências
├── .env             # Configurações
└── logs/            # Diretório de logs
```

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
| MONGO_URI | URI de conexão MongoDB | mongodb://localhost:27017/database |
| API_USERNAME | Usuário da API e-Millenium | seu.usuario |
| API_PASSWORD | Senha da API e-Millenium | sua.senha |
| ENVIRONMENT | Ambiente de execução (test/production) | production |
| LOG_LEVEL | Nível de detalhamento dos logs | INFO |
| LOG_MODE | Modo de armazenamento dos logs | SINGLE |
| API_URL | URL base da API e-Millenium | https://api.emillenium.com.br |
| MONGO_DATABASE | Nome do banco de dados MongoDB | emillenium_sync |
| MONGO_COLLECTION | Nome da coleção padrão | lancamentos |

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

* **Adejaime Junior** - *Desenvolvimento* - [adejaimejr](https://github.com/adejaimejr)

## ⌨️ Desenvolvido com ❤️ por [i92Tech](https://i92tecnologia.com.br)