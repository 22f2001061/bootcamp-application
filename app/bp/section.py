from flask import Blueprint, redirect, request, url_for, render_template, session, flash
from werkzeug.security import generate_password_hash


from app.db import db
from app.models import Section


bp = Blueprint(
    "section",
)
