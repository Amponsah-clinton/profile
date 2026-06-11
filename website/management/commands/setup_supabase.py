import os
from pathlib import Path

import psycopg2
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Apply supabase/schema.sql to the Supabase PostgreSQL database'

    def handle(self, *args, **options):
        schema_path = Path(settings.BASE_DIR) / 'supabase' / 'schema.sql'
        sql = schema_path.read_text(encoding='utf-8')

        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            dbname=os.getenv('DB_NAME', 'postgres'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT', '5432'),
            sslmode='require',
        )
        conn.autocommit = True
        try:
            with conn.cursor() as cur:
                cur.execute(sql)
            self.stdout.write(self.style.SUCCESS('Schema applied successfully.'))
        finally:
            conn.close()
