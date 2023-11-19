from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///reader.db')
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    grade = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    total_points = Column(Integer, default=0)
    profile_picture = Column(String)


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
    book_path = Column(String)


# class UserBookProgress(Base):
#     __tablename__ = "user_book_progress"
#     user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
#     book_id = Column(Integer, ForeignKey('books.id'), primary_key=True)
#     last_page_read = Column(Integer)

#
# class Quiz(Base):
#     __tablename__ = "quizzes"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.id'))
#     book_id = Column(Integer, ForeignKey('books.id'))
#     user = relationship("User", back_populates="quizzes")
#     book = relationship("Book", back_populates="quizzes")
#     questions = relationship("Question", back_populates="quiz")
#     completed = Column(Integer, default=0)
#
#
# class Question(Base):
#     __tablename__ = "questions"
#     id = Column(Integer, primary_key=True)
#     text = Column(String)
#     quiz_id = Column(Integer, ForeignKey('quizzes.id'))
#     quiz = relationship("Quiz", back_populates="questions")
#     answers = relationship("Answer", secondary=quiz_question_answer, back_populates="questions")
#
#
# class Answer(Base):
#     __tablename__ = "answers"
#     id = Column(Integer, primary_key=True)
#     text = Column(String)
#     is_correct = Column(Integer)
#     questions = relationship("Question", secondary=quiz_question_answer, back_populates="answers")


Base.metadata.create_all(engine)
