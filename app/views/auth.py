from flask import Blueprint, render_template, url_for, redirect, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app import forms as f, db
from app.models import User
from app.logger import log
from config import config

CFG = config()

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["GET", "POST"])
def login():
    form: f.LoginForm = f.LoginForm(request.form)
    if form.validate_on_submit():

        user: User = User.authenticate(form.user_id.data, form.password.data)

        log(
            log.INFO,
            "Form submitted. User: [%s] [%s]",
            form.user_id.data,
            form.password.data,
        )
        if not user:
            flash("Wrong username or password.", "danger")
            log(log.ERROR, "User with such credentials is not found")
            return render_template("auth/login.html", form=form)

        login_user(user)
        log(log.INFO, "Login successful. current_user: [%s]", current_user.name)
        log(log.INFO, "Login successful")
        flash("Login successful.", "success")
        return redirect(url_for("news.get_all"))

    elif form.is_submitted():
        flash("Invalid credentials", "danger")
        log(log.ERROR, "Form submitted error: [%s]", form.errors)
    return render_template("auth/login.html", form=form)


@auth_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    log(log.INFO, "You were logged out.")
    session.clear()
    return redirect(url_for("auth.login"))
