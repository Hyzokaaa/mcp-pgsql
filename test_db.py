# test_db.py
from db import run_query

if __name__ == "__main__":
    try:
        filas = run_query("SELECT * FROM car LIMIT 3;")
        print("Tipo de retorno:", type(filas))
        print("Contenido (hasta 3 filas):")
        for f in filas:
            print(f)                      # Cada f debe ser un dict
    except Exception as e:
        print("Hubo un error:", e)
