from pydantic import BaseModel
from typing import List

class AnswerBase(BaseModel):
    text: str
    is_correct: bool = False

class AnswerCreate(AnswerBase):
    pass

class Answer(AnswerBase):
    id: int

    class Config:
        from_attributes = True

class QuestionBase(BaseModel):
    text: str

class QuestionCreate(QuestionBase):
    answers: List[AnswerCreate]

class Question(QuestionBase):
    id: int
    answers: List[Answer] = []

    class Config:
        from_attributes = True

class SectionBase(BaseModel):
    name: str

class SectionCreate(SectionBase):
    pass

class Section(SectionBase):
    id: int
    questions: List[Question] = []

    class Config:
        from_attributes = True

class SectionInfo(SectionBase):
    id: int

    class Config:
        from_attributes = True

class TestCreate(BaseModel):
    section: str
    question: str
    answers: List[str]
    correct: int
