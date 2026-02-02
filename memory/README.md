# Agent Memory - MongoDB

Shared MongoDB instance for agent memory and state management.

## Quick Start

```bash
docker-compose up -d
```

## Access

- **MongoDB**: `mongodb://admin:admin123@localhost:27017`
- **Mongo Express UI**: http://localhost:8081 (admin/admin123)

## Connection String

```python
MONGODB_URI = "mongodb://admin:admin123@localhost:27017/agent_memory?authSource=admin"
```

## Stop

```bash
docker-compose down
```

## Clean Data

```bash
docker-compose down -v
```
