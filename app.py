# import os
# from http.server import BaseHTTPRequestHandler, HTTPServer

# VERSION = os.getenv("APP_VERSION", "unknown")
# PORT = int(os.getenv("PORT", 8080))


# class Handler(BaseHTTPRequestHandler):
#     def do_GET(self):
#         self.send_response(200)
#         self.send_header("Content-Type", "text/plain")
#         self.end_headers()
#         self.wfile.write(f"version: {VERSION}\n".encode())

#     def log_message(self, format, *args):
#         pass  # suprimir logs de acceso


# if __name__ == "__main__":
#     print(f"Servidor iniciado en puerto {PORT}, version={VERSION}")
#     HTTPServer(("", PORT), Handler).serve_forever()
import os

import psycopg2
from fastapi import FastAPI, HTTPException

VERSION = os.getenv("APP_VERSION", "unknown")
DB_USER = os.getenv("DB_USER", "lg_process")
DB_PASS = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "poc_dev")
PSC_IP = os.getenv(
    "PSC_IP", "127.0.0.1"
)  # AlloyDB PSC IP en prod, Cloud SQL public IP en POC
PORT = int(os.getenv("DB_PORT", "5432"))
SCHEMA = "poc"

app = FastAPI()


def get_conn():
    # Conexión TCP directa — mismo patrón que service-hub/src/config.py (conn_sync)
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=PSC_IP, port=PORT
    )


@app.get("/version")
def version():
    return {"version": VERSION}


@app.get("/health")
def health():
    try:
        conn = get_conn()
        conn.close()
        return {"status": "ok", "db": "connected", "version": VERSION}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/schema")
def schema():
    """Estado actual del schema — úsalo para verificar qué migraciones se aplicaron."""
    conn = get_conn()
    try:
        cur = conn.cursor()

        cur.execute(
            """
            SELECT table_name, column_name, data_type
            FROM information_schema.columns
            WHERE table_schema = %s
            ORDER BY table_name, ordinal_position
        """,
            (SCHEMA,),
        )
        columns = cur.fetchall()

        cur.execute(
            """
            SELECT indexname, tablename
            FROM pg_indexes
            WHERE schemaname = %s
              AND indexname NOT LIKE '%%_pkey'
            ORDER BY tablename, indexname
        """,
            (SCHEMA,),
        )
        indexes = cur.fetchall()

        cur.execute(
            """
            SELECT tc.constraint_name, tc.table_name, kcu.column_name, ccu.table_name AS ref_table
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage kcu
                ON tc.constraint_name = kcu.constraint_name AND tc.table_schema = kcu.table_schema
            JOIN information_schema.constraint_column_usage ccu
                ON tc.constraint_name = ccu.constraint_name AND tc.table_schema = ccu.table_schema
            WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_schema = %s
            ORDER BY tc.table_name
        """,
            (SCHEMA,),
        )
        fks = cur.fetchall()

        cur.execute("""
            SELECT version_num FROM poc.alembic_version
        """)
        applied = [r[0] for r in cur.fetchall()]

        cur.close()

        tables = {}
        for tbl, col, dtype in columns:
            tables.setdefault(tbl, {"columns": [], "indexes": [], "foreign_keys": []})
            tables[tbl]["columns"].append({"name": col, "type": dtype})

        for idx_name, tbl in indexes:
            if tbl in tables:
                tables[tbl]["indexes"].append(idx_name)

        for fk_name, tbl, col, ref in fks:
            if tbl in tables:
                tables[tbl]["foreign_keys"].append(
                    {"constraint": fk_name, "column": col, "references": ref}
                )

        return {
            "version": VERSION,
            "schema": SCHEMA,
            "applied_migrations": sorted(applied),
            "tables": tables,
        }
    finally:
        conn.close()
