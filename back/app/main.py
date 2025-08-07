from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .database import SessionLocal, engine, get_db

from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(openapi_prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

@app.post("/tests/", response_model=List[schemas.Question])
def create_tests(tests: List[schemas.TestCreate], db: Session = Depends(get_db)):
    created_questions = []
    for test in tests:
        # Find or create section
        db_section = db.query(models.Section).filter(models.Section.name == test.section).first()
        if not db_section:
            db_section = models.Section(name=test.section)
            db.add(db_section)
            db.commit()
            db.refresh(db_section)

        # Create question
        db_question = models.Question(text=test.question, section_id=db_section.id)
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        # Create answers
        for i, answer_text in enumerate(test.answers):
            is_correct = (i == test.correct)
            db_answer = models.Answer(text=answer_text, is_correct=is_correct, question_id=db_question.id)
            db.add(db_answer)
        
        db.commit()
        db.refresh(db_question)
        created_questions.append(db_question)
    return created_questions

@app.get("/sections/", response_model=List[schemas.SectionInfo])
def read_sections(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    sections = db.query(models.Section).offset(skip).limit(limit).all()
    return sections

@app.get("/sections/{section_id}/tests/", response_model=List[schemas.Question])
def read_section_tests(section_id: int, db: Session = Depends(get_db)):
    questions = db.query(models.Question).filter(models.Question.section_id == section_id).all()
    if not questions:
        raise HTTPException(status_code=404, detail="Section not found or no tests in section")
    return questions

@app.get("/")
def read_root():
    return {"Hello": "World"}
