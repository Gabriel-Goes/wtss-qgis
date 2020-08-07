from json import loads as json_loads
from pathlib import Path

from .config import Config

schemas_folder = Path(Config.BASE_DIR) / 'json-schemas'

def load_schema(file_name):
    """
    Open file and parses as JSON file
    Args:
        file_name (str): File name of JSON Schema
    Returns:
        JSON schema parsed as Python object (dict)
    Raises:
        json.JSONDecodeError When file is not valid JSON object
    """
    schema_file = schemas_folder / file_name

    with schema_file.open() as f:
        return json_loads(f.read())


# Schemas
services_storage_schema = load_schema('services_schema.json')
