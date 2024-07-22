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
        title = request.form.get("bookTitle")
        description = request.form.get("description")
        book_content = request.form.get("bookContent")
        author_name = request.form.get("authorName")
        section_id = request.form.get("sectionId")

        new_book = Book(
            title=title,
            description=description,
            content=book_content,
            author=author_name,
            section_id=section_id,
        )
        db.session.add(new_book)
        db.session.commit()
        flash(f"New book with title: {title} is created!", "success")
        return redirect(url_for("book.list_books"))


@bp.route("/edit/books/<book_id>", methods=["GET", "POST"])
def edit_book(book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    if request.method == "GET":
        sections = Section.query.all()
        return render_template("book/edit.html", book=book, available_sections=sections)
    if request.method == "POST":
        title = request.form.get("bookTitle")
        description = request.form.get("description")
        book_content = request.form.get("bookContent")
        author_name = request.form.get("authorName")
        section_id = request.form.get("sectionId")
        book.title = title
        book.description = description
        book.content = book_content
        book.author = author_name
        book.section_id = section_id
        db.session.add(book)
        db.session.commit()
        flash(f"Book with title: {title} is edited successfully!", "info")
        return redirect(url_for("book.list_books"))


@bp.route("/delete/books/<book_id>", methods=["GET", "POST"])
def delete_book(book_id):
    book = Book.query.filter_by(book_id=book_id).first()
    if request.method == "GET":
        return render_template("book/confirm_delete.html", book=book)
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
