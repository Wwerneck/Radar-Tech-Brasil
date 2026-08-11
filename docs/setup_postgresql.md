# Setup PostgreSQL

## Opção Recomendada: Docker Compose

Subir PostgreSQL local:

```powershell
docker compose up -d
```

Criar `.env` local com:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=radar_tech
DB_USER=postgres
DB_PASSWORD=postgres
```

Validar conexão:

```powershell
python -m src.check_database
```

Carregar tabelas, views, dimensão CBO tech e agregados mensais:

```powershell
python -m src.load
```

## Observações

- `.env` não deve ser versionado.
- O `docker-compose.yml` usa senha local simples apenas para ambiente de desenvolvimento.
- Em produção ou publicação real, use variáveis de ambiente seguras.

