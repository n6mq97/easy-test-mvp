import pytest
from app.models import Section, Question, Answer
from app.schemas import TestPayload

class TestDatabaseIntegration:
    """Интеграционные тесты для проверки работы с базой данных"""
    
    def test_full_workflow_create_test(self, db_session):
        """Тест полного рабочего процесса создания теста"""
        # 1. Создаем секцию
        section = Section(name="Advanced Math")
        db_session.add(section)
        db_session.commit()
        db_session.refresh(section)
        
        assert section.id is not None
        assert section.name == "Advanced Math"
        
        # 2. Создаем вопрос
        question = Question(text="What is the derivative of x²?", section_id=section.id)
        db_session.add(question)
        db_session.commit()
        db_session.refresh(question)
        
        assert question.id is not None
        assert question.text == "What is the derivative of x²?"
        assert question.section_id == section.id
        
        # 3. Создаем ответы
        answers = [
            Answer(text="x", is_correct=False, question_id=question.id),
            Answer(text="2x", is_correct=True, question_id=question.id),
            Answer(text="x²", is_correct=False, question_id=question.id),
            Answer(text="2x²", is_correct=False, question_id=question.id)
        ]
        for answer in answers:
            db_session.add(answer)
        db_session.commit()
        
        # 4. Проверяем связи
        db_session.refresh(question)
        db_session.refresh(section)
        
        assert len(question.answers) == 4
        assert any(a.is_correct for a in question.answers)
        assert sum(1 for a in question.answers if a.is_correct) == 1
        
        assert len(section.questions) == 1
        assert section.questions[0].id == question.id
        
        # 5. Проверяем правильный ответ
        correct_answer = next(a for a in question.answers if a.is_correct)
        assert correct_answer.text == "2x"
    
    def test_multiple_sections_with_questions(self, db_session):
        """Тест создания нескольких секций с вопросами"""
        # Создаем секции
        sections_data = [
            ("Mathematics", ["What is 2+2?", "What is 3×3?"]),
            ("Physics", ["What is gravity?", "What is light?"]),
            ("History", ["Who was Napoleon?", "When was WWII?"])
        ]
        
        created_sections = []
        for section_name, questions_texts in sections_data:
            section = Section(name=section_name)
            db_session.add(section)
            db_session.commit()
            db_session.refresh(section)
            created_sections.append(section)
            
            # Создаем вопросы для секции
            for question_text in questions_texts:
                question = Question(text=question_text, section_id=section.id)
                db_session.add(question)
                db_session.commit()
                db_session.refresh(question)
                
                # Создаем ответы для каждого вопроса
                answers = [
                    Answer(text=f"Answer 1 for {question_text}", is_correct=False, question_id=question.id),
                    Answer(text=f"Answer 2 for {question_text}", is_correct=True, question_id=question.id),
                    Answer(text=f"Answer 3 for {question_text}", is_correct=False, question_id=question.id)
                ]
                for answer in answers:
                    db_session.add(answer)
                db_session.commit()
        
        # Проверяем результаты
        assert len(created_sections) == 3
        
        for section in created_sections:
            db_session.refresh(section)
            assert len(section.questions) == 2
            
            for question in section.questions:
                assert len(question.answers) == 3
                assert any(a.is_correct for a in question.answers)
                assert sum(1 for a in question.answers if a.is_correct) == 1
    
    def test_data_consistency(self, db_session):
        """Тест консистентности данных"""
        # Создаем тестовые данные
        section = Section(name="Test Section")
        db_session.add(section)
        db_session.commit()
        db_session.refresh(section)
        
        question = Question(text="Test Question", section_id=section.id)
        db_session.add(question)
        db_session.commit()
        db_session.refresh(question)
        
        answer = Answer(text="Test Answer", is_correct=True, question_id=question.id)
        db_session.add(answer)
        db_session.commit()
        db_session.refresh(answer)
        
        # Проверяем консистентность ID
        assert section.id > 0
        assert question.id > 0
        assert answer.id > 0
        
        # Проверяем связи
        assert question.section_id == section.id
        assert answer.question_id == question.id
        
        # Проверяем обратные связи
        db_session.refresh(section)
        db_session.refresh(question)
        
        assert section.questions[0].id == question.id
        assert question.answers[0].id == answer.id
        
        # Проверяем, что данные сохранились в БД
        saved_section = db_session.query(Section).filter_by(id=section.id).first()
        saved_question = db_session.query(Question).filter_by(id=question.id).first()
        saved_answer = db_session.query(Answer).filter_by(id=answer.id).first()
        
        assert saved_section is not None
        assert saved_question is not None
        assert saved_answer is not None
        
        assert saved_section.name == "Test Section"
        assert saved_question.text == "Test Question"
        assert saved_answer.text == "Test Answer"
        assert saved_answer.is_correct is True

class TestSchemaValidation:
    """Тесты валидации схем"""
    
    def test_test_create_schema_validation(self):
        """Тест валидации схемы создания теста"""
        # Валидные данные
        valid_data = {
            "section": "Math",
            "question": "What is 2+2?",
            "answers": ["3", "4", "5"],
            "correct": 1
        }
        test = TestPayload(**valid_data)
        assert test.section == "Math"
        assert test.question == "What is 2+2?"
        assert test.answers == ["3", "4", "5"]
        assert test.correct == 1
        
        # Проверяем граничные случаи
        edge_case_data = {
            "section": "A",  # Минимальная длина
            "question": "Q?",  # Минимальная длина
            "answers": ["A"],  # Минимальное количество ответов
            "correct": 0  # Первый ответ
        }
        test = TestPayload(**edge_case_data)
        assert test.correct == 0

