from flask import Blueprint, redirect, request, url_for, render_template, session, flash

from app.db import db
from app.models import Book, Section, User, BookIssue
from app.utils import login_required

from datetime import datetime

bp = Blueprint(
    "book_issue",
    __name__,
)


@bp.route("/request/books/<book_id>", methods=["GET", "POST"])
@login_required("student")
def request_book(book_id):
    if request.method == "POST":
        user_id = session.get("user_id")
        # earlier_issues = BookIssue.query.filter_by(user_id=user_id).all()
        new_issue = BookIssue(user_id=user_id, book_id=book_id)
        db.session.add(new_issue)
        db.session.commit()
        flash("Request to issue the book is sent.", "info")
        return redirect(url_for("homepage"))


@bp.route("/book-requests")
@login_required("admin")
def book_requests():
    book_requests = BookIssue.query.all()
    return render_template("book_requests.html", book_requests=book_requests)


@bp.route("/book-requests/<action>/<issue_id>", methods=["POST"])
@login_required("admin")
def accept_request(action, issue_id):
    if request.method == "POST":
        issue = BookIssue.query.get(issue_id)
        if issue:
            print(issue.status)
            if action.lower() == "accept":
                issue.date_issued = datetime.now()
                issue.status = "accepted"
                db.session.add(issue)
                db.session.commit()
                print("after edit")
                print(issue.status)
            elif action.lower() == "reject":
                issue.date_issued = datetime.now()
                issue.status = "rejected"
                db.session.add(issue)
                db.session.commit()

        return redirect(url_for("book_issue.book_requests"))


@bp.route("/my-books")
@login_required("student")
def my_books():
    user_id = session.get("user_id")
    # my_books = Book.query.join(BookIssue).filter(BookIssue.user_id == user_id).all()
    my_books = BookIssue.query.filter(BookIssue.user_id == user_id).all()

    return render_template("my_books.html", my_books=my_books)


# def generate_bar_chart():
#     # Sample data
#     categories = ['Books Borrowed', 'Books Returned', 'New Members', 'Active Members']
#     values = [random.randint(50, 150) for _ in categories]

#     # Create a bar chart
#     plt.figure(figsize=(10, 6))
#     plt.bar(categories, values, color='skyblue')
#     plt.xlabel('Categories')
#     plt.ylabel('Values')
#     plt.title('Library Statistics')

#     # Save the plot to a BytesIO object
#     img = io.BytesIO()
#     plt.savefig(img, format='png')
#     img.seek(0)  # Rewind the data

#     return img
