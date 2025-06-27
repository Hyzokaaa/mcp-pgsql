# app/tests/test_validators.py

import pytest
from app.db.validators import validate_select_only, InvalidQueryError

def test_valid_select():
    validate_select_only("SELECT * FROM car;")

@pytest.mark.parametrize("sql", [
    "SELECT * FROM car; DROP TABLE users;",
    "DELETE FROM car;",
    "SELECT * FROM car; -- comentario",
    "SELECT a; SELECT b;",
])
def test_invalid_queries(sql):
    with pytest.raises(InvalidQueryError):
        validate_select_only(sql)
