# Pereval app backend

> git clone https://github.com/iMWC-IXIVI/pereval_backend.git - клонирование проекта

> cd pereval_backend - переходим в папку с проектом

> python -m venv venv - создание виртуального окружения

> venv\scripts\activate - активация виртуального окружения

> pip install -r req.txt - установка зависимостей

> copy .env.example .env - копирование .env файла

> start .env - изменение .env файла

> cd app - переходим в папку с проектом

> uvicorn main:app --reload - запуск сервера

> alembic revision --autogenerate -m "some message" - создание миграций

> alembic upgrade head - накат миграций

# PSS ALEMBIC MANUAL

> alembic init -t async alembic - создание асинхронного alembic

> Далее в файле alembic.ini в переменной sqlalchemy.url записать ${DB_URL}, что бы в данной переменной была переменная окружения

> После перейти в файл env.py импортировать необходимые библиотеки, а именно dotenv, os. Base, которая ранее создавалась в models (declarative_base)

> config.set_section_option('alembic', 'sqlalchemy.url', os.getenv('DB_URL')) - добавить запись, потому что наши переменные окружения нахоядстя в файле .env, и их надо считать, что бы переменная не осталась пустой 

> alembic revision --autogenerate -m "some message" - создание миграционного файла

> alembic ubgrade head - накатывание миграций

> alembic downgrade <id revission or -1> - откат конкретной миграции или на 1