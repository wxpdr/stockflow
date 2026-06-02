# StockFlow

Sistema web para controle de estoque desenvolvido como MVP acadêmico do Projeto Integrador.

## Configuração local

1. Instale as dependências:

```bash
pip install -r requirements.txt
```

2. Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```env
SECRET_KEY=sua_chave_secreta_aqui
DB_HOST=localhost
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
DB_NAME=stockflow
FLASK_DEBUG=1
```

3. Execute o sistema:

```bash
python app.py
```

## Observação de segurança

O arquivo `.env` não deve ser enviado para repositórios públicos ou para o deploy. Em ambiente online, configure essas informações diretamente nas variáveis de ambiente da hospedagem.
