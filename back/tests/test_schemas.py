import pytest
from pydantic import ValidationError
from app.schemas import (
    AnswerBase, AnswerCreate, Answer,
    QuestionBase, QuestionCreate, Question,
    SectionBase, SectionCreate, Section,
    SectionInfo, TestPayload
)

class TestAnswerSchemas:
    """Тесты для схем ответов"""
    
    def test_answer_base_valid(self):
        """Тест валидной базовой схемы ответа"""
        data = {"text": "Test Answer", "is_correct": True}
        answer = AnswerBase(**data)
        assert answer.text == "Test Answer"
        assert answer.is_correct is True
    
    def test_answer_base_default_is_correct(self):
        """Тест значения по умолчанию для is_correct"""
        data = {"text": "Test Answer"}
        answer = AnswerBase(**data)
        assert answer.is_correct is False
    
    def test_answer_create(self):
        """Тест схемы создания ответа"""
        data = {"text": "Test Answer", "is_correct": True}
        answer = AnswerCreate(**data)
        assert answer.text == "Test Answer"
        assert answer.is_correct is True
    
    def test_answer_with_id(self):
        """Тест схемы ответа с ID"""
        data = {"id": 1, "text": "Test Answer", "is_correct": True}
        answer = Answer(**data)
        assert answer.id == 1
        assert answer.text == "Test Answer"
        assert answer.is_correct is True

class TestQuestionSchemas:
    """Тесты для схем вопросов"""
    
    def test_question_base_valid(self):
        """Тест валидной базовой схемы вопроса"""
        data = {"text": "What is 2+2?"}
        question = QuestionBase(**data)
        assert question.text == "What is 2+2?"
    
    def test_question_create_valid(self):
        """Тест валидной схемы создания вопроса"""
        data = {
            "text": "What is 2+2?",
            "answers": [
                {"text": "3", "is_correct": False},
                {"text": "4", "is_correct": True},
                {"text": "5", "is_correct": False}
            ]
        }
        question = QuestionCreate(**data)
        assert question.text == "What is 2+2?"
        assert len(question.answers) == 3
        assert question.answers[1].is_correct is True
    
    def test_question_with_id_and_answers(self):
        """Тест схемы вопроса с ID и ответами"""
        data = {
            "id": 1,
            "text": "What is 2+2?",
            "answers": [
                {"id": 1, "text": "3", "is_correct": False},
                {"id": 2, "text": "4", "is_correct": True}
            ]
        }
        question = Question(**data)
        assert question.id == 1
        assert question.text == "What is 2+2?"
        assert len(question.answers) == 2
        assert question.answers[1].id == 2

class TestSectionSchemas:
    """Тесты для схем секций"""
    
    def test_section_base_valid(self):
        """Тест валидной базовой схемы секции"""
        data = {"name": "Mathematics"}
        section = SectionBase(**data)
        assert section.name == "Mathematics"
    
    def test_section_create(self):
        """Тест схемы создания секции"""
        data = {"name": "Mathematics"}
        section = SectionCreate(**data)
        assert section.name == "Mathematics"
    
    def test_section_with_id_and_questions(self):
        """Тест схемы секции с ID и вопросами"""
        data = {
            "id": 1,
            "name": "Mathematics",
            "questions": [
                {"id": 1, "text": "What is 2+2?", "answers": []},
                {"id": 2, "text": "What is 3+3?", "answers": []}
            ]
        }
        section = Section(**data)
        assert section.id == 1
        assert section.name == "Mathematics"
        assert len(section.questions) == 2
    
    def test_section_info(self):
        """Тест схемы информации о секции"""
        data = {"id": 1, "name": "Mathematics"}
        section = SectionInfo(**data)
        assert section.id == 1
        assert section.name == "Mathematics"

class TestTestPayloadSchema:
    """Тесты для схемы создания теста"""
    
    def test_test_create_valid(self):
        """Тест валидной схемы создания теста"""
        data = {
            "section": "Mathematics",
            "question": "What is 2+2?",
            "answers": ["3", "4", "5"],
            "correct": 1
        }
        test = TestPayload(**data)
        assert test.section == "Mathematics"
        assert test.question == "What is 2+2?"
        assert test.answers == ["3", "4", "5"]
        assert test.correct == 1
