from django.core.management.base import BaseCommand

from website import defaults, pages_db
from website.supabase_client import get_supabase

# Profile media that the dashboard uploads — never overwrite these from defaults.
MEDIA_FIELDS = ('photo_url', 'cv_url', 'cv_filename')


class Command(BaseCommand):
    help = 'Seed Supabase tables with homepage content from website/defaults.py'

    def handle(self, *args, **options):
        sb = get_supabase(anon=False)

        # ── Profile (preserve any uploaded photo / CV) ───────────────────
        profile_data = {k: v for k, v in defaults.PROFILE.items() if k not in MEDIA_FIELDS}
        existing = sb.table('site_profile').select('*').limit(1).execute()
        if existing.data:
            row = existing.data[0]
            for field in MEDIA_FIELDS:
                if row.get(field):
                    profile_data[field] = row[field]
            sb.table('site_profile').update(profile_data).eq('id', row['id']).execute()
        else:
            sb.table('site_profile').insert(profile_data).execute()

        # ── News ─────────────────────────────────────────────────────────
        sb.table('news_items').delete().neq('id', 0).execute()
        sb.table('news_items').insert([
            {'event_date': n['event_date'], 'body': n['body'], 'sort_order': i}
            for i, n in enumerate(defaults.NEWS)
        ]).execute()

        # ── Research interests ───────────────────────────────────────────
        sb.table('research_interests').delete().neq('id', 0).execute()
        sb.table('research_interests').insert([
            {'label': label, 'sort_order': i} for i, label in enumerate(defaults.RESEARCH)
        ]).execute()

        # ── Education ────────────────────────────────────────────────────
        sb.table('education_entries').delete().neq('id', 0).execute()
        sb.table('education_entries').insert([
            {**entry, 'sort_order': i} for i, entry in enumerate(defaults.EDUCATION)
        ]).execute()

        # ── Publications (each carries its own pub_type / year) ──────────
        sb.table('publications').delete().neq('id', 0).execute()
        pubs = []
        groups = (
            ('journal', defaults.PUBLICATIONS_JOURNAL),
            ('conference', defaults.PUBLICATIONS_CONFERENCE),
            ('workshop', defaults.PUBLICATIONS_WORKSHOP),
        )
        for pub_type, items in groups:
            for i, p in enumerate(items):
                pubs.append({'pub_type': pub_type, 'sort_order': i, **p})
        if pubs:
            sb.table('publications').insert(pubs).execute()

        # ── Teaching ─────────────────────────────────────────────────────
        sb.table('teaching_courses').delete().neq('id', 0).execute()
        sb.table('teaching_courses').insert([
            {'label': c, 'sort_order': i} for i, c in enumerate(defaults.TEACHING)
        ]).execute()

        # ── Certifications (stored in the "awards" table) ────────────────
        sb.table('awards').delete().neq('id', 0).execute()
        sb.table('awards').insert([
            {'label': a, 'sort_order': i} for i, a in enumerate(defaults.AWARDS)
        ]).execute()

        # ── Service ──────────────────────────────────────────────────────
        sb.table('service_entries').delete().neq('id', 0).execute()
        service_rows = []
        order = 0
        for category, items in defaults.SERVICE.items():
            for item in items:
                service_rows.append({'category': category, 'label': item, 'sort_order': order})
                order += 1
        sb.table('service_entries').insert(service_rows).execute()

        # ── Navigation pages ─────────────────────────────────────────────
        self._seed_pages()

        self.stdout.write(self.style.SUCCESS('Site content seeded in Supabase.'))

    def _seed_pages(self):
        """Ensure built-in pages exist, relabel Awards -> Certifications, and
        add the Experience / Projects custom pages."""
        pages_db.seed_site_pages()

        # Repurpose the built-in "awards" page as "Certifications".
        awards_page = pages_db.get_page_by_type('awards', admin=True)
        if awards_page:
            pages_db.update_site_page(awards_page['id'], {
                'label': 'Certifications',
                'slug': 'certifications',
                'icon': 'fa-certificate',
            })

        # Custom pages: slug, label, icon, sort_order, content.
        custom_pages = [
            ('experience', 'Experience', 'fa-briefcase', 45, defaults.EXPERIENCE_CONTENT),
            ('projects', 'Projects', 'fa-diagram-project', 46, defaults.PROJECTS_CONTENT),
        ]
        for slug, label, icon, sort_order, content in custom_pages:
            existing = pages_db.get_site_page_by_slug(slug, admin=True)
            data = {
                'label': label,
                'slug': slug,
                'page_type': 'custom',
                'icon': icon,
                'sort_order': sort_order,
                'is_enabled': True,
                'custom_content': content,
            }
            if existing:
                pages_db.update_site_page(existing['id'], data)
            else:
                pages_db.insert_site_page(data)
