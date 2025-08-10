import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.database import Base, get_db
from app.main import app

# Устанавливаем переменные окружения для тестов
@pytest.fixture(autouse=True)
def setup_test_env():
    """Автоматически устанавливает тестовое окружение для всех тестов"""
    os.environ["DATABASE_URL"] = "postgresql://user:password@localhost/testdb"
    yield
    # Очищаем переменные после тестов
    if "DATABASE_URL" in os.environ:
        del os.environ["DATABASE_URL"]

@pytest.fixture
def db_engine():
    """Создает тестовый движок БД"""
    database_url = "postgresql://user:password@localhost/testdb"
    engine = create_engine(database_url)
    yield engine
    engine.dispose()

@pytest.fixture
def db_session(db_engine):
    """Создает тестовую сессию БД с автоматической очисткой"""
    # Создаем все таблицы
    Base.metadata.create_all(bind=db_engine)
    
    # Создаем сессию
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    
    yield session
    
    # Очищаем после тестов
    session.close()
    Base.metadata.drop_all(bind=db_engine)

@pytest.fixture
def client(db_session):
    """Создает тестовый клиент с переопределенной зависимостью БД"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    
    # Восстанавливаем оригинальную зависимость
    app.dependency_overrides.clear()

@pytest.fixture
def sample_section(db_session):
    """Создает тестовую секцию"""
    from app.models import Section
    section = Section(name="Test Section")
    db_session.add(section)
    db_session.commit()
    db_session.refresh(section)
    return section

@pytest.fixture
def sample_question(db_session, sample_section):
    """Создает тестовый вопрос"""
    from app.models import Question
    question = Question(text="Test Question?", section_id=sample_section.id)
    db_session.add(question)
    db_session.commit()
    db_session.refresh(question)
    return question

@pytest.fixture
def sample_answers(db_session, sample_question):
    """Создает тестовые ответы"""
    from app.models import Answer
    answers = [
        Answer(text="Answer 1", is_correct=False, question_id=sample_question.id),
        Answer(text="Answer 2", is_correct=True, question_id=sample_question.id),
        Answer(text="Answer 3", is_correct=False, question_id=sample_question.id)
    ]
    for answer in answers:
        db_session.add(answer)
    db_session.commit()
    return answers
