from django.core.management.base import BaseCommand

from website.pages_db import list_site_pages, seed_site_pages


class Command(BaseCommand):
    help = 'Seed default site_pages (Biography, News, Research, etc.)'

    def handle(self, *args, **options):
        seed_site_pages()
        count = len(list_site_pages(admin=True))
        self.stdout.write(self.style.SUCCESS(f'Site pages ready ({count} pages).'))
