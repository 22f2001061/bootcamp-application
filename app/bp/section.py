from flask import Blueprint, redirect, request, url_for, render_template, session, flash

from app.db import db
from app.models import Section


bp = Blueprint(
    "section",
    __name__,
)


# CRUD
# base/sections -> list of all the sections
@bp.route("/sections")
def list_sections():
    sections = Section.query.all()
    return render_template("section/section_list.html", sections=sections)


@bp.route("/create/sections", methods=["GET", "POST"])
def create_and_list_sections():
    if request.method == "GET":
        return render_template("section/create_section.html")
    elif request.method == "POST":
        section_name = request.form.get("sectionName")
        new_section = Section(section_name=section_name)
        db.session.add(new_section)
        db.session.commit()
        flash(f"Section with name: {section_name} created successfully", "success")
        return redirect(url_for("section.list_sections"))


@bp.route("/edit/sections/<section_id>", methods=["GET", "POST"])
def edit_section(section_id):
    section = Section.query.filter_by(section_id=section_id).first()
    if request.method == "GET":
        return render_template("section/edit_section.html", section=section)
    if request.method == "POST":
        # handle edit operation.
        section_name = request.form.get("sectionName")
        section.section_name = section_name
        db.session.add(section)
        db.session.commit()
        flash(f"Section with id: {section.section_id} is edited successfully!", "info")
        return redirect(url_for("section.list_sections"))


@bp.route("/delete/sections/<section_id>", methods=["GET", "POST"])
def delete_section(section_id):
    section = Section.query.filter_by(section_id=section_id).first()
    if request.method == "GET":
        return render_template("section/confirm_delete.html", section=section)
    if request.method == "POST":
        # handle edit operation.
        if section:
            db.session.delete(section)
            db.session.commit()
            flash(
                f"Section with id: {section.section_id} is deleted successfully!",
                "success",
            )
        else:
            flash(f"Section with id: {section_id} is does not exit!", "warning")

        return redirect(url_for("section.list_sections"))


# Listing -> /sections (GET request)
# Create -> /sections (POST request)
# Retrieve -> /sections/<section_id>(GET)
# Update -> /sections/<section_id> (PUT)
# Delete -> /sections/<section_id> (DELETE)
