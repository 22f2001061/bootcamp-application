from flask import Blueprint, redirect, request, url_for, render_template, session, flash

from app.db import db
from app.models import Book, Section


bp = Blueprint(
    "book",
    __name__,
)


# CRUD on Books
# base/books -> list of all the books
@bp.route("/books")
def list_books():
    books = Book.query.all()
    return render_template("book/list.html", books=books)


@bp.route("/create/books", methods=["GET", "POST"])
def create_and_list_books():
    sections = Section.query.all()
    if request.method == "GET":
        return render_template("book/create.html", available_sections=sections)
    elif request.method == "POST":
        book_name = request.form.get("bookName")
        new_book = Book(book_name=book_name)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for("book.create_and_list_books"))


@bp.route("/edit/books/<book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    if request.method == "GET":
        return render_template("edit_book.html", book=book)
    if request.method == "POST":
        # handle edit operation.
        book_name = request.form.get("bookName")
        book.book_name = book_name
        db.session.add(book)
        db.session.commit()
        flash(f"Book with id: {book.book_id} is edited successfully!", "info")
        return redirect(url_for("book.list_books"))


@bp.route("/delete/books/<book_id>", methods=["GET", "POST"])
def delete_book(book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    if request.method == "GET":
        return render_template("confirm_delete.html", book=book)
    if request.method == "POST":
        # handle edit operation.
        if book:
            db.session.delete(book)
            db.session.commit()
            flash(
                f"Book with id: {book.book_id} is deleted successfully!",
                "success",
            )
        else:
            flash(f"Book with id: {book_id} is does not exit!", "warning")

        return redirect(url_for("book.list_books"))
