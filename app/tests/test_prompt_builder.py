# app/tests/test_prompt_builder.py

from app.agent.prompt_builder import build_system_prompt
from app.db.db import list_tables

def test_prompt_includes_table_names():
    prompt = build_system_prompt()
    tablas = list_tables()
    assert any(tabla in prompt for tabla in tablas), "El prompt debe mencionar alguna tabla"
