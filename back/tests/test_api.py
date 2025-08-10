import pytest
from app.models import Section, Question, Answer

def test_create_tests_api(client, db_session):
    """Тест API создания тестов"""
    test_data = [{
        "section": "Mathematics",
        "question": "What is 2+2?",
        "answers": ["3", "4", "5"],
        "correct": 1
    }]
    
    response = client.post("/tests/", json=test_data)
    assert response.status_code == 200
    
    # Проверяем, что данные сохранились в БД
    sections = db_session.query(Section).all()
    assert len(sections) == 1
    assert sections[0].name == "Mathematics"
    
    questions = db_session.query(Question).all()
    assert len(questions) == 1
    assert questions[0].text == "What is 2+2?"
    assert questions[0].section_id == sections[0].id
    
    answers = db_session.query(Answer).all()
    assert len(answers) == 3
    assert answers[1].is_correct is True  # correct = 1 (второй ответ)
    assert answers[0].is_correct is False
    assert answers[2].is_correct is False

def test_create_multiple_tests_api(client, db_session):
    """Тест API создания нескольких тестов"""
    test_data = [
        {
            "section": "Science",
            "question": "What is gravity?",
            "answers": ["Force", "Energy", "Matter"],
            "correct": 0
        },
        {
            "section": "Science",
            "question": "What is light?",
            "answers": ["Wave", "Particle", "Both"],
            "correct": 2
        }
    ]
    
    response = client.post("/tests/", json=test_data)
    assert response.status_code == 200
    
    # Проверяем, что создалась одна секция
    sections = db_session.query(Section).all()
    assert len(sections) == 1
    assert sections[0].name == "Science"
    
    # Проверяем, что создались два вопроса
    questions = db_session.query(Question).all()
    assert len(questions) == 2
    assert questions[0].text == "What is gravity?"
    assert questions[1].text == "What is light?"
    
    # Проверяем ответы
    answers = db_session.query(Answer).all()
    assert len(answers) == 6  # 3 + 3
    
    # Проверяем правильные ответы
    gravity_answers = [a for a in answers if a.question_id == questions[0].id]
    light_answers = [a for a in answers if a.question_id == questions[1].id]
    
    assert gravity_answers[0].is_correct is True  # correct = 0
    assert light_answers[2].is_correct is True   # correct = 2

def test_read_sections_api(client, db_session):
    """Тест API получения секций"""
    # Создаем тестовые секции
    sections_data = ["Math", "Science", "History"]
    for name in sections_data:
        section = Section(name=name)
        db_session.add(section)
    db_session.commit()
    
    response = client.get("/sections/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 3
    assert all(section["name"] in sections_data for section in data)
    assert all("id" in section for section in data)

def test_read_sections_with_pagination(client, db_session):
    """Тест API получения секций с пагинацией"""
    # Создаем много секций
    for i in range(15):
        section = Section(name=f"Section {i}")
        db_session.add(section)
    db_session.commit()
    
    # Тестируем лимит
    response = client.get("/sections/?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    
    # Тестируем offset
    response = client.get("/sections/?skip=5&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5
    assert data[0]["name"] == "Section 5"

def test_read_section_tests_api(client, db_session):
    """Тест API получения тестов по секции"""
    # Создаем секцию с вопросами
    section = Section(name="Test Section")
    db_session.add(section)
    db_session.commit()
    
    questions = [
        Question(text="Question 1?", section_id=section.id),
        Question(text="Question 2?", section_id=section.id)
    ]
    for question in questions:
        db_session.add(question)
    db_session.commit()
    
    response = client.get(f"/sections/{section.id}/tests/")
    assert response.status_code == 200
    
    data = response.json()
    assert len(data) == 2
    assert data[0]["text"] == "Question 1?"
    assert data[1]["text"] == "Question 2?"

def test_read_section_tests_not_found(client, db_session):
    """Тест API получения тестов несуществующей секции"""
    response = client.get("/sections/999/tests/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Section not found or no tests in section"

def test_read_section_tests_empty_section(client, db_session):
    """Тест API получения тестов пустой секции"""
    # Создаем секцию без вопросов
    section = Section(name="Empty Section")
    db_session.add(section)
    db_session.commit()
    
    response = client.get(f"/sections/{section.id}/tests/")
    assert response.status_code == 404
    assert response.json()["detail"] == "Section not found or no tests in section"

def test_health_check_api(client):
    """Тест API проверки здоровья"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_root_api(client):
    """Тест корневого API"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

