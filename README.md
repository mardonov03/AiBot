1. заруск проекта:
    1.1. запустите Docker вручную
    1.2 зайдиту в папку с docker-compose.yml
    1.3 запустите docker-compose.yml через терминал: docker-compose --env-file ./fast/.env up --build (на сервере желательно с sudo)


пример fast/.env фала:
    DB_USER=postgres
    DB_PASS=your_db_password
    DB_NAME=your_db_name
    DB_HOST=db
    DB_PORT=5432
    REDIS_HOST=redis
    REDIS_PORT=6379

пример tgbot/.env фала:
    BOT_TOKEN=your_bot_token
    API=http://api:8099
    AGREEMENT_URL_RU=https://telegra.ph/...
    AGREEMENT_URL_EN=https://telegra.ph/...
    AGREEMENT_URL_UZ=https://telegra.ph/...