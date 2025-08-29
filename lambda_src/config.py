from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    app_name: str = "QShelter Odoo-3cx API"
    admin_email: str = "efagenevalentine@gmail.com"
    database_name: str = str(os.getenv("ODOO_DB"))
    password: str = str(os.getenv("ODOO_PASSWORD"))
    username: str = str(os.getenv("ODOO_USERNAME"))
    url: str = str(os.getenv("ODOO_URL"))


settings = Settings()
