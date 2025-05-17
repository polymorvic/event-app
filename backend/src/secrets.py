import os


def _secret_value(variable_name: str) -> str:
    return os.environ[variable_name]


def database_user() -> str:
    return _secret_value("DATABASE_USER")


def database_password() -> str:
    return _secret_value("DATABASE_PASSWORD")
