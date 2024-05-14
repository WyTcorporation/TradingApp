    python -m venv venv
    .\venv\Scripts\activate

    pip install "fastapi[all]"
    https://github.com/tiangolo/fastapi?tab=readme-ov-file
    https://fastapi.tiangolo.com/#installation
    uvicorn main:app --reload (main - file name - run virt server)

    gunicorn main:app --workers 1 --worker[README.md](..%2F..%2FOSPanel%2Fbackups%2Faggregator%2FREADME.md)-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000 (production run server)

    pip install sqlalchemy alembic psycopg2

    alembic init migrations - Створемо всі не обхідні файли для міграції
    alembic revision --autogenerate -m "Database creation" - Генерація файлу міграції після підключення кофіга та env
    alembic upgrade 4f806872c49d - Мігруємо нашу створену міграцію. revision наш id для команди
    alembic upgrade head - Мігруємо останню
    
    https://fastapi-users.github.io/fastapi-users/latest/
    pip install 'fastapi-users[sqlalchemy]'
    For PostgreSQL: pip install asyncpg
    For SQLite: pip install aiosqlite

    https://github.com/zhanymkanov/fastapi-best-practices

    https://github.com/tporadowski/redis/releases/tag/v5.0.14.1
    https://github.com/long2ice/fastapi-cache
    pip install fastapi-cache2
    
    Черги
    pip install celery flower
    celery -A tasks.tasks:celery worker --loglevel=INFO --pool=solo - запустить worker
    celery -A tasks.tasks:celery flower - запустить flower візалізація worker
    http://localhost:5555/
    
    Unit Test
    pip install pytest pytest-asyncio

    pyproject.toml - Створимо файл для тестів з розташуванням нашої апки
    [tool.pytest.ini_options]
    pythonpath = [
        ".", "src",
    ]
    asyncio_mode="auto"

    conftest.py - Налаштування наших тестів
    
    pytest ./tests - запуск
    
    Весокети
    pip install websockets
    

    Docker 
    pip install gunicorn
    pip freeze > .\requirements.txt
    pip install -r .\requirements.txt
    

    docker build . -t fastapi_app:latest
    docker run -p 7329:8000 fastapi_app
    docker-compose build
    docker-compose up