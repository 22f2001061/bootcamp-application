from flask import Blueprint, redirect, request, url_for, render_template, session, flash

from app.db import db
from app.models import Book, Section, User
from app.utils import login_required

bp = Blueprint(
    "book_issue",
    __name__,
)


# @bp.route('/request/books/<book_id>')
# def request_book(book_id):


@bp.route("/book-requests")
@login_required("admin")
def book_requests():
    return render_template("book_requests.html")


@bp.route("/my-books")
@login_required("student")
def my_books():
    return render_template("my_books.html")
