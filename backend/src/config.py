import os


def _environment_varialble(variable_name: str, default: str | None = None) -> str:
    variable_value = os.environ.get(variable_name, default)
    
    if not variable_value:
        raise Exception(f"Variable {variable_name} not found")
    
    return variable_value


def database_host() -> str:
    return _environment_varialble("DATABASE_HOST")

def database_port() -> str:
    return _environment_varialble("DATABASE_PORT")

def database_name() -> str:
    return _environment_varialble("DATABASE_NAME")