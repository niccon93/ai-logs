import os
import time
import sys
import psycopg

DB_URL = os.getenv('DATABASE_URL', 'postgresql://ailog:ailog@db:5432/ailog')
timeout = float(os.getenv('PG_WAIT_TIMEOUT', '60'))
started = time.monotonic()

while True:
    try:
        with psycopg.connect(DB_URL) as conn:
            with conn.cursor() as cur:
                cur.execute('SELECT 1')
                cur.fetchone()
            print('Postgres is ready.')
            sys.exit(0)
    except Exception as e:
        if time.monotonic() - started > timeout:
            print(f'Timed out waiting for Postgres: {e}')
            sys.exit(1)
        time.sleep(1)
