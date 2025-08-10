import pytest
import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db

# Добавляем путь к корневой директории проекта для импорта config
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

try:
    from config.database import config as app_config
    # Используем централизованную конфигурацию
    database_url = app_config.database_url
except ImportError:
    # Fallback для случаев, когда config недоступен
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError(
            "Отсутствует обязательная переменная: DATABASE_URL\n"
            "Скопируйте config/env.example в .env и заполните значения"
        )

@pytest.fixture(scope="session")
def engine():
    """Создать движок БД для тестов"""
    # Создаем движок
    engine = create_engine(database_url)
    
    # Создаем все таблицы
    from app.models import Base
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Удаляем все таблицы
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture
def db_session(engine):
    """Создать сессию БД для тестов"""
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Очищаем все данные перед каждым тестом
    from app.models import Base
    for table in reversed(Base.metadata.sorted_tables):
        session.execute(table.delete())
    session.commit()
    
    yield session
    
    # Очищаем все данные после каждого теста
    session.rollback()
    session.close()

@pytest.fixture
def client(db_session):
    """Создать тестовый клиент FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()

@pytest.fixture
def sample_section(db_session):
    """Создать тестовую секцию"""
    from app.models import Section
    section = Section(name="Test Section")
    db_session.add(section)
    db_session.commit()
    db_session.refresh(section)
    return section

@pytest.fixture
def sample_question(db_session, sample_section):
    """Создать тестовый вопрос"""
    from app.models import Question
    question = Question(text="Test Question?", section_id=sample_section.id)
    db_session.add(question)
    db_session.commit()
    db_session.refresh(question)
    return question
