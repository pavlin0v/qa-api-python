# QA API Python

Тестовое задание API на Python (FastAPI).

### 1. Склонируйте репозиторий

```bash
git clone https://github.com/pavlin0v/qa-api-python
```

### 2. Настройка окружения

 На основе `.env.example` создайте файл `.env` в корне проекта.

 ```bash
 cp .env.example .env
 ```


### 3. Запуск контейнеров

Соберите и запустите контейнеры:

```bash
docker compose up -d --build
```

### Тесты (pytest_asyncio)

Для запуска тестов:

```bash
docker compose exec app pytest
```
