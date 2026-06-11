"""Merge Supabase rows with local defaults for template rendering."""

from collections import defaultdict

from website import defaults
from website.pages_db import build_public_nav, list_site_pages
from website.supabase_helpers import get_site_context


def _merge_profile(row):
    profile = dict(defaults.PROFILE)
    if row:
        for key, value in row.items():
            if value is not None:          # allow '' so cleared fields actually clear
                profile[key] = value
    return profile


def _merge_list(db_rows, default_rows, label_key='label', body_key=None):
    if db_rows:
        if body_key:
            return db_rows
        return [row.get(label_key, '') for row in db_rows if row.get(label_key)]
    return default_rows


def _group_service(rows):
    if not rows:
        return defaults.SERVICE

    grouped = defaultdict(list)
    for row in rows:
        grouped[row['category']].append(row['label'])
    return dict(grouped)


def build_home_context():
    """Return a complete, template-ready context dict."""
    try:
        raw = get_site_context()
        from_db = bool(raw.get('profile'))
    except Exception:
        raw = {}
        from_db = False

    profile = _merge_profile(raw.get('profile'))

    news = raw.get('news') or defaults.NEWS
    research = _merge_list(raw.get('research_interests'), defaults.RESEARCH)
    education = raw.get('education') or defaults.EDUCATION

    pubs_journal = raw.get('publications_journal') or defaults.PUBLICATIONS_JOURNAL
    pubs_conference = raw.get('publications_conference') or defaults.PUBLICATIONS_CONFERENCE
    pubs_workshop = raw.get('publications_workshop') or defaults.PUBLICATIONS_WORKSHOP

    teaching = _merge_list(raw.get('teaching'), defaults.TEACHING)
    awards = raw.get('awards') or [{'label': item} for item in defaults.AWARDS]
    service = _group_service(raw.get('service'))

    bio_paragraphs = [p.strip() for p in profile.get('biography', '').split('\n\n') if p.strip()]
    students_paragraphs = [p.strip() for p in profile.get('students_text', '').split('\n\n') if p.strip()]

    return {
        'from_db': from_db,
        'profile': profile,
        'bio_paragraphs': bio_paragraphs,
        'students_paragraphs': students_paragraphs,
        'news': news,
        'research_interests': research,
        'education': education,
        'publications_journal': pubs_journal,
        'publications_conference': pubs_conference,
        'publications_workshop': pubs_workshop,
        'teaching': teaching,
        'awards': awards,
        'service': service,
        'sections': _build_sections(),
        'teaching_institution': profile.get('university', ''),
    }


def _build_sections():
    try:
        nav = build_public_nav()
        if nav:
            return nav
    except Exception:
        pass
    if list_site_pages():
        return build_public_nav()
    return [
        {'id': s['id'], 'slug': s['id'], 'label': s['label'], 'href': f"/{s['id']}/" if s['id'] != 'biography' else '/'}
        for s in defaults.SECTIONS
    ]
