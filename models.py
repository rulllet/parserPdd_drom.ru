from typing import Optional
from sqlmodel import Field, Relationship, SQLModel, Column, String


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))
    description: str

    questions: list['Question'] = Relationship(back_populates="category_name")


class Question(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ticket: int
    number: int
    title: str
    help: str
    image: str

    category_id: Optional[str] = Field(default=None, foreign_key="category.name")
    category_name: Optional[Category] = Relationship(back_populates="questions")

    answers: list['Answer'] = Relationship(back_populates="question_name")


class Answer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    correct_answer: bool

    question_id: Optional[int] = Field(default=None, foreign_key="question.id")
    question_name: Optional[Question] = Relationship(back_populates="answers")
