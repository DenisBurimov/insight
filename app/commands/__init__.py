import click
from flask import Flask
import sqlalchemy as sa
from app import db, models as m
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

    @app.cli.command()
    def read_img():
        from app.services.gpt import gpt_service

        response = gpt_service.recognize("app/static/payments/payments_001.jpg")
        print(response)

    @app.cli.command()
    def get_payments():
        payments = db.session.scalars(sa.select(m.Payment)).all()

        if not payments:
            print("No payments found")
            return

        for payment in payments:
            print(payment)

    @app.cli.command()
    def delete_payments():
        payments = db.session.scalars(sa.select(m.Payment)).all()
        for payment in payments:
            db.session.delete(payment)

        try:
            db.session.commit()
            print("Payments deleted")
        except Exception as e:
            print(e)

    @app.cli.command()
    def ask_filters():
        from app.services.gpt import gpt_service

        question = "Скільки транзакцій де платник чи отримувач Іван Іванич Іванов?"
        res = gpt_service.get_filters(question)
        print(res)
