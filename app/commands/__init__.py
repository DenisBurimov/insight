import click
from flask import Flask
import sqlalchemy as sa
from app import db, models as m
from config import config
from app.services.gpt import ChatGPT


CFG = config()
gpt = ChatGPT()


def init(app: Flask):
    # flask cli context setup
    @app.shell_context_processor
    def get_context():
        """Objects exposed here will be automatically available from the shell."""
        return dict(
            app=app,
            # some_arg=some_arg,
        )

    @app.cli.command()
    @click.option("--flag", type=bool)
    def sample(flag: bool):
        """Sample command"""

        print(f"Flag: {flag}")

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

    @app.cli.command("call-api")
    def call_api():
        import os
        import requests

        response = requests.get(
            "http://127.0.0.1:5050/api/v1/nssmc/parser_scheduler",
            headers={
                "Access-Token": os.environ.get("SCHEDULER_ACCESS_TOKEN"),
                "User-Agent": "Google-Cloud-Scheduler",
            },
        )
        print(response)
        print("API called successfully")
