# StockFlow
Sistema web de controle de estoque desenvolvido com Python (Flask) e MySQL, focado na organização de materiais e gestão de movimentações.


## Configuração de ambiente

Antes de executar o projeto, crie um arquivo `.env` na raiz do sistema com base no arquivo `.env.example`.

Exemplo:

```env
SECRET_KEY=coloque_uma_chave_grande_e_segura_aqui
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=sua_senha_do_banco
DB_NAME=stockflow
```

O arquivo `.env` não deve ser enviado para repositórios públicos, pois contém informações sensíveis da aplicação.
