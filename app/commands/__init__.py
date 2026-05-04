import click
from flask import Flask
import sqlalchemy as sa
from app import db
import models as m
from config import config
from app.services.gpt import ChatGPT
from app.logger import log

CFG = config()


def init(app: Flask):
    # flask cli context setup
    @app.shell_context_processor
    def get_context():
        """Objects exposed here will be automatically available from the shell."""
        return dict(
            app=app,
            db=db,
            sa=sa,
            m=m,
            # some_arg=some_arg,
        )

    @app.cli.command("get-users")
    def get_users():
        users = db.session.scalars(sa.select(m.User)).all()
        print(users)

    @app.cli.command()
    def create_admin():
        admin = m.User(
            name=CFG.ADMIN_USERNAME,
            email=CFG.ADMIN_EMAIL,
            password=CFG.ADMIN_PASSWORD,
            role=m.UserRole.ADMIN.value,
            is_active=True,
        ).save()
        print("Admin created: ", admin)
