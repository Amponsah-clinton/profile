"""CRUD for site_pages navigation table."""

import re

from website.page_registry import BUILTIN_SEEDS, PAGE_REGISTRY
from website.supabase_client import get_supabase


def _sb(admin=False):
    return get_supabase(anon=not admin)


def slugify(value):
    value = value.lower().strip()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    return value.strip('-') or 'page'


def list_site_pages(enabled_only=False, admin=False):
    query = _sb(admin).table('site_pages').select('*').order('sort_order')
    if enabled_only:
        query = query.eq('is_enabled', True)
    return query.execute().data or []


def get_site_page(page_id, admin=False):
    result = _sb(admin).table('site_pages').select('*').eq('id', page_id).limit(1).execute()
    return result.data[0] if result.data else None


def get_site_page_by_slug(slug, admin=False):
    result = _sb(admin).table('site_pages').select('*').eq('slug', slug).limit(1).execute()
    return result.data[0] if result.data else None


def get_home_page():
    pages = list_site_pages(enabled_only=True)
    return pages[0] if pages else None


def get_page_by_type(page_type, admin=False):
    result = _sb(admin).table('site_pages').select('*').eq('page_type', page_type).limit(1).execute()
    return result.data[0] if result.data else None


def insert_site_page(data):
    if 'slug' not in data or not data['slug']:
        data['slug'] = slugify(data.get('label', 'page'))
    return _sb(True).table('site_pages').insert(data).execute()


def update_site_page(page_id, data):
    return _sb(True).table('site_pages').update(data).eq('id', page_id).execute()


def delete_site_page(page_id):
    page = get_site_page(page_id, admin=True)
    if not page:
        return None
    if PAGE_REGISTRY.get(page['page_type'], {}).get('builtin'):
        raise ValueError('Built-in pages cannot be deleted. Disable them instead.')
    return _sb(True).table('site_pages').delete().eq('id', page_id).execute()


def seed_site_pages():
    sb = _sb(True)
    for seed in BUILTIN_SEEDS:
        existing = sb.table('site_pages').select('id').eq('page_type', seed['page_type']).execute()
        if not existing.data:
            sb.table('site_pages').insert(seed).execute()


def build_public_nav():
    """Nav items for the public site sidebar."""
    home = get_home_page()
    home_id = home['id'] if home else None
    nav = []
    for page in list_site_pages(enabled_only=True):
        href = '/' if page['id'] == home_id else f"/{page['slug']}/"
        nav.append({
            'id': page['slug'],
            'slug': page['slug'],
            'label': page['label'],
            'href': href,
            'page_type': page['page_type'],
        })
    return nav


def build_dashboard_nav():
    """Sidebar sections for the admin dashboard."""
    site_items = [{'slug': '', 'label': 'Dashboard', 'icon': 'fa-home', 'url': 'dashboard_home'}]

    for page in list_site_pages(admin=True):
        reg = PAGE_REGISTRY.get(page['page_type'], PAGE_REGISTRY['custom'])
        item = {
            'slug': page['slug'],
            'label': page['label'],
            'icon': page.get('icon') or reg['icon'],
            'url': reg['dashboard_url'],
        }
        if page['page_type'] == 'custom':
            item['url_kwargs'] = {'page_id': page['id']}
        site_items.append(item)

    return [
        {'section': 'Site Pages', 'items': site_items},
        {'section': 'Manage', 'items': [
            {'slug': 'pages-manage', 'label': 'Manage Pages', 'icon': 'fa-sitemap', 'url': 'dashboard_pages_list'},
            {'slug': 'site', 'label': 'View Site', 'icon': 'fa-external-link-alt', 'url': 'site_home', 'external': True},
        ]},
    ]


def active_slug_for_type(page_type):
    page = get_page_by_type(page_type, admin=True)
    return page['slug'] if page else page_type
