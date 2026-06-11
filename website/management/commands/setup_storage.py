import os
from pathlib import Path

import psycopg2
from django.conf import settings
from django.core.management.base import BaseCommand

from website.storage_helpers import ensure_storage_bucket


class Command(BaseCommand):
    help = 'Create Supabase storage bucket "profile" and apply storage policies'

    def handle(self, *args, **options):
        ensure_storage_bucket()
        self.stdout.write(self.style.SUCCESS('Storage bucket ensured via API.'))

        sql_path = Path(settings.BASE_DIR) / 'supabase' / 'storage.sql'
        if not sql_path.exists():
            return

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
                cur.execute(sql_path.read_text(encoding='utf-8'))
            self.stdout.write(self.style.SUCCESS('Storage policies applied.'))
        finally:
            conn.close()
