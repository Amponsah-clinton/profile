from django.core.management.base import BaseCommand

from website.supabase_client import get_supabase


class Command(BaseCommand):
    help = 'Test Supabase API connection'

    def handle(self, *args, **options):
        from postgrest.exceptions import APIError

        sb = get_supabase()
        try:
            result = sb.table('site_profile').select('id, full_name').limit(1).execute()
        except APIError as exc:
            if 'Could not find the table' in str(exc):
                self.stdout.write(self.style.WARNING(
                    'API connected, but tables are missing. '
                    'Run supabase/schema.sql in the Supabase SQL Editor.'
                ))
                return
            raise

        if result.data:
            self.stdout.write(self.style.SUCCESS(f'OK — found profile: {result.data[0]}'))
        else:
            self.stdout.write(self.style.WARNING('Connected, but site_profile is empty.'))
