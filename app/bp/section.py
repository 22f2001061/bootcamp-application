from flask import Blueprint, redirect, request, url_for, render_template, session, flash
from werkzeug.security import generate_password_hash


from app.db import db
from app.models import Section


bp = Blueprint(
    "section",
    __name__,
)

# CRUD
# base/sections -> list of all the sections

# Listing -> /sections (GET request)
# Create -> /sections (POST request)


@bp.route("/sections", methods=["GET", "POST"])
def create_and_list_sections():
    if request.method == "GET":
        sections = Section.query.all()
        return render_template("create_section.html", sections=sections)
    elif request.method == "POST":
        section_name = request.form.get("sectionName")
        new_section = Section(section_name=section_name)
        db.session.add(new_section)
        db.session.commit()
        return redirect(url_for("section.create_and_list_sections"))


# Retrieve -> /sections/<section_id>(GET)
# Update -> /sections/<section_id> (PUT)
# Delete -> /sections/<section_id> (DELETE)
