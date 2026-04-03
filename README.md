## Storage Inventory API (Lab #6)
Backend-система для управления инвентаризацией складских устройств. Переведена на NoSQL стек для обеспечения высокой гибкости схем данных.
---
### 🚀 Основной стек
**Framework:** FastAPI (Python 3.13)

**Database:** MongoDB 6.0 (через ODM Beanie)

**Caching/Sessions:** Redis 7

**Containerization:** Docker & Docker Compose

**Security: JWT** (Access/Refresh tokens) в HTTP-only куках + Yandex OAuth 2.0

---
### ✨ Ключевые фичи
Asynchronous: Полностью асинхронный код (Motor + Beanie).

Security: Защищенные эндпоинты с индикацией (замочки) в Swagger UI.

Session Management: Хранение активных сессий в Redis с автоматическим истечением срока (TTL).

Deployment: Быстрый запуск всей инфраструктуры одной командой.
---
### 🛠 Установка и запуск
1. Настройка окружения
Создайте файл .env в корне проекта и заполните его по образцу:

1.1 **База данных (MongoDB)**
```
DB_USER=mongoloid
DB_PASSWORD=your_password
DB_NAME=storage_db
MONGO_URI="mongodb://mongoloid:your_password@mongo:27017/storage_db?authSource=admin"
```
1.2 **Кэш (Redis)**
```
REDIS_HOST=redis
REDIS_PORT=6379
REDIS_PASSWORD=your_redis_password
```
1.3  **JWT**
```
JWT_ACCESS_SECRET=your_super_secret
ALGORITHM=HS256
```
2. Запуск через Docker Compose
   
Система автоматически поднимет приложение, базу данных и кеш:

```docker-compose up --build```
### 📖 Документация API
После запуска документация доступна по адресам:

**Swagger UI:** http://localhost:8000/api/docs

**ReDoc:** http://localhost:8000/redoc

**!Примечание:** Для доступа к эндпоинтам раздела Storage необходимо сначала авторизоваться через /auth/login. После успешного входа кука access_token будет установлена автоматически.

### 📁 Структура проекта
```app/main.py``` — Точка входа, настройка FastAPI и OpenAPI.

```app/api/``` — Роутеры и эндпоинты версии v1.

```app/db/``` — Инициализация подключения к MongoDB (Beanie).

```app/models/``` — Описание документов (User, StorageDevice).

```app/services/``` — Бизнес-логика (Auth, Cache, Storage).

```app/core/``` — Глобальные конфиги и хелперы безопасности.

### 📋 Важные команды для разработки
Очистка системы: ```docker-compose down -v.```

Просмотр логов: ```docker logs -f storage_api.```
