from django.core.management.base import BaseCommand

from website import defaults
from website.supabase_client import get_supabase


class Command(BaseCommand):
    help = 'Seed Supabase tables with default homepage content'

    def handle(self, *args, **options):
        sb = get_supabase(anon=False)

        profile_data = {
            **defaults.PROFILE,
            'students_email': defaults.PROFILE.get('students_email', 'lab@university.edu'),
            'researchgate_url': defaults.PROFILE.get('researchgate_url', ''),
        }
        existing = sb.table('site_profile').select('id').limit(1).execute()
        if existing.data:
            sb.table('site_profile').update(profile_data).eq('id', existing.data[0]['id']).execute()
        else:
            sb.table('site_profile').insert(profile_data).execute()

        sb.table('news_items').delete().neq('id', 0).execute()
        sb.table('news_items').insert([
            {'event_date': n['event_date'], 'body': n['body'], 'sort_order': i}
            for i, n in enumerate(defaults.NEWS)
        ]).execute()

        sb.table('research_interests').delete().neq('id', 0).execute()
        sb.table('research_interests').insert([
            {'label': label, 'sort_order': i} for i, label in enumerate(defaults.RESEARCH)
        ]).execute()

        sb.table('education_entries').delete().neq('id', 0).execute()
        sb.table('education_entries').insert([
            {**entry, 'sort_order': i} for i, entry in enumerate(defaults.EDUCATION)
        ]).execute()

        sb.table('publications').delete().neq('id', 0).execute()
        pubs = []
        for i, p in enumerate(defaults.PUBLICATIONS_JOURNAL):
            pubs.append({**p, 'pub_type': 'journal', 'sort_order': i, 'year': 2024})
        for i, p in enumerate(defaults.PUBLICATIONS_CONFERENCE):
            pubs.append({**p, 'pub_type': 'conference', 'sort_order': i, 'year': 2025})
        for i, p in enumerate(defaults.PUBLICATIONS_WORKSHOP):
            pubs.append({**p, 'pub_type': 'workshop', 'sort_order': i, 'year': 2022})
        sb.table('publications').insert(pubs).execute()

        sb.table('teaching_courses').delete().neq('id', 0).execute()
        sb.table('teaching_courses').insert([
            {'label': c, 'sort_order': i} for i, c in enumerate(defaults.TEACHING)
        ]).execute()

        sb.table('awards').delete().neq('id', 0).execute()
        sb.table('awards').insert([
            {'label': a, 'sort_order': i} for i, a in enumerate(defaults.AWARDS)
        ]).execute()

        sb.table('service_entries').delete().neq('id', 0).execute()
        service_rows = []
        order = 0
        for category, items in defaults.SERVICE.items():
            for item in items:
                service_rows.append({'category': category, 'label': item, 'sort_order': order})
                order += 1
        sb.table('service_entries').insert(service_rows).execute()

        self.stdout.write(self.style.SUCCESS('Homepage content seeded in Supabase.'))
