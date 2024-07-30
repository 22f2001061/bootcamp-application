from app.db import db
from datetime import time, datetime


class User(db.Model):
    __tablename__ = "users"
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    fname = db.Column(db.String, nullable=False)
    lname = db.Column(db.String)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    role = db.Column(db.String)


class Section(db.Model):
    __tablename__ = "sections"
    section_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    section_name = db.Column(db.String)
    # books = db.relationship("Book", backref="books", lazy=True)


class Book(db.Model):
    __tablename__ = "books"
    book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=True)
    content = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    # pages
    # thumbnail
    section_id = db.Column(
        db.Integer, db.ForeignKey("sections.section_id"), nullable=True
    )


class BookIssue(db.Model):
    __name__ = "book_issues"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.book_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    date_requested = db.Column(db.Date, default=datetime.now())
    date_issued = db.Column(db.Date, nullable=True)
    date_returned = db.Column(db.Date, nullable=True)
    status = db.Column(
        db.String, default="pending"
    )  # accepted, rejected, pending, revoked, returned
