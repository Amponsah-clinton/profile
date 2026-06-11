"""
Data-access helpers for profile content stored in Supabase.
"""

from website.supabase_client import get_supabase


def get_profile():
    """Fetch the main profile row (single-site)."""
    sb = get_supabase()
    result = sb.table('site_profile').select('*').limit(1).execute()
    return result.data[0] if result.data else None


def get_news(limit=20):
    sb = get_supabase()
    result = (
        sb.table('news_items')
        .select('*')
        .order('event_date', desc=True)
        .limit(limit)
        .execute()
    )
    return result.data or []


def get_research_interests():
    sb = get_supabase()
    result = (
        sb.table('research_interests')
        .select('*')
        .order('sort_order')
        .execute()
    )
    return result.data or []


def get_education():
    sb = get_supabase()
    result = (
        sb.table('education_entries')
        .select('*')
        .order('sort_order')
        .execute()
    )
    return result.data or []


def get_publications(pub_type=None):
    sb = get_supabase()
    query = sb.table('publications').select('*').order('year', desc=True).order('sort_order')
    if pub_type:
        query = query.eq('pub_type', pub_type)
    result = query.execute()
    return result.data or []


def get_teaching():
    sb = get_supabase()
    result = (
        sb.table('teaching_courses')
        .select('*')
        .order('sort_order')
        .execute()
    )
    return result.data or []


def get_awards():
    sb = get_supabase()
    result = (
        sb.table('awards')
        .select('*')
        .order('year', desc=True)
        .execute()
    )
    return result.data or []


def get_service():
    sb = get_supabase()
    result = (
        sb.table('service_entries')
        .select('*')
        .order('category')
        .order('sort_order')
        .execute()
    )
    return result.data or []


def get_site_context():
    """Bundle all homepage data; falls back gracefully if tables are empty."""
    return {
        'profile': get_profile(),
        'news': get_news(),
        'research_interests': get_research_interests(),
        'education': get_education(),
        'publications_journal': get_publications('journal'),
        'publications_conference': get_publications('conference'),
        'publications_workshop': get_publications('workshop'),
        'teaching': get_teaching(),
        'awards': get_awards(),
        'service': get_service(),
    }
