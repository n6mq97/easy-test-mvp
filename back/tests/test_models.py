import pytest
from app.models import Section, Question, Answer

def test_create_section(db_session):
    """Тест создания секции"""
    section = Section(name="Mathematics")
    db_session.add(section)
    db_session.commit()
    db_session.refresh(section)
    
    assert section.id is not None
    assert section.name == "Mathematics"
    assert len(section.questions) == 0

def test_create_question(db_session, sample_section):
    """Тест создания вопроса"""
    question = Question(text="What is 2+2?", section_id=sample_section.id)
    db_session.add(question)
    db_session.commit()
    db_session.refresh(question)
    
    assert question.id is not None
    assert question.text == "What is 2+2?"
    assert question.section_id == sample_section.id
    assert question.section.name == "Test Section"
    assert len(question.answers) == 0

def test_create_answer(db_session, sample_question):
    """Тест создания ответа"""
    answer = Answer(text="4", is_correct=True, question_id=sample_question.id)
    db_session.add(answer)
    db_session.commit()
    db_session.refresh(answer)
    
    assert answer.id is not None
    assert answer.text == "4"
    assert answer.is_correct is True
    assert answer.question_id == sample_question.id
    assert answer.question.text == "Test Question?"

def test_section_questions_relationship(db_session):
    """Тест связи секции с вопросами"""
    # Создаем секцию
    section = Section(name="Science")
    db_session.add(section)
    db_session.commit()
    
    # Создаем несколько вопросов
    questions = [
        Question(text="What is gravity?", section_id=section.id),
        Question(text="What is light?", section_id=section.id),
        Question(text="What is energy?", section_id=section.id)
    ]
    for question in questions:
        db_session.add(question)
    db_session.commit()
    
    # Проверяем связь
    db_session.refresh(section)
    assert len(section.questions) == 3
    assert all(q.section_id == section.id for q in section.questions)

def test_question_answers_relationship(db_session, sample_question):
    """Тест связи вопроса с ответами"""
    # Создаем несколько ответов
    answers = [
        Answer(text="Option A", is_correct=False, question_id=sample_question.id),
        Answer(text="Option B", is_correct=True, question_id=sample_question.id),
        Answer(text="Option C", is_correct=False, question_id=sample_question.id),
        Answer(text="Option D", is_correct=False, question_id=sample_question.id)
    ]
    for answer in answers:
        db_session.add(answer)
    db_session.commit()
    
    # Проверяем связь
    db_session.refresh(sample_question)
    assert len(sample_question.answers) == 4
    assert any(a.is_correct for a in sample_question.answers)
    assert sum(1 for a in sample_question.answers if a.is_correct) == 1

def test_unique_section_name(db_session):
    """Тест уникальности имени секции"""
    section1 = Section(name="Unique Section")
    db_session.add(section1)
    db_session.commit()
    
    # Пытаемся создать секцию с тем же именем
    section2 = Section(name="Unique Section")
    db_session.add(section2)
    
    # Должно вызвать ошибку уникальности
    with pytest.raises(Exception):
        db_session.commit()
    
    # Откатываем изменения
    db_session.rollback()

