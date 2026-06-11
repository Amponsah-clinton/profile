"""Supabase write operations for the dashboard (service role)."""

from website.supabase_client import get_supabase


def _admin():
    return get_supabase(anon=False)


def get_dashboard_stats():
    sb = _admin()
    tables = [
        'news_items', 'research_interests', 'education_entries',
        'publications', 'teaching_courses', 'awards', 'service_entries',
    ]
    stats = {}
    for table in tables:
        result = sb.table(table).select('id').execute()
        stats[table] = len(result.data or [])
    profile = sb.table('site_profile').select('full_name, updated_at').limit(1).execute()
    stats['profile'] = profile.data[0] if profile.data else None
    return stats


def get_profile():
    result = _admin().table('site_profile').select('*').limit(1).execute()
    return result.data[0] if result.data else {}


def update_profile(data):
    profile = get_profile()
    if profile.get('id'):
        return _admin().table('site_profile').update(data).eq('id', profile['id']).execute()
    return _admin().table('site_profile').insert(data).execute()


def list_rows(table, order_col='sort_order', desc=False):
    return _admin().table(table).select('*').order(order_col, desc=desc).execute().data or []


def get_row(table, row_id):
    result = _admin().table(table).select('*').eq('id', row_id).limit(1).execute()
    return result.data[0] if result.data else None


def insert_row(table, data):
    return _admin().table(table).insert(data).execute()


def update_row(table, row_id, data):
    return _admin().table(table).update(data).eq('id', row_id).execute()


def delete_row(table, row_id):
    return _admin().table(table).delete().eq('id', row_id).execute()


def list_publications():
    return _admin().table('publications').select('*').order('year', desc=True).order('sort_order').execute().data or []
