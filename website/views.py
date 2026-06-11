import logging

from django.http import Http404
from django.shortcuts import redirect, render

from website.context_builders import build_home_context
from website import defaults
from website.page_registry import PAGE_REGISTRY
from website.pages_db import get_home_page, get_site_page_by_slug

logger = logging.getLogger(__name__)


def _fallback_context():
    return {
        'from_db': False,
        'profile': defaults.PROFILE,
        'bio_paragraphs': defaults.PROFILE['biography'].split('\n\n'),
        'students_paragraphs': defaults.PROFILE['students_text'].split('\n\n'),
        'news': defaults.NEWS,
        'research_interests': defaults.RESEARCH,
        'education': defaults.EDUCATION,
        'publications_journal': defaults.PUBLICATIONS_JOURNAL,
        'publications_conference': defaults.PUBLICATIONS_CONFERENCE,
        'publications_workshop': defaults.PUBLICATIONS_WORKSHOP,
        'teaching': defaults.TEACHING,
        'awards': [{'label': a} for a in defaults.AWARDS],
        'service': defaults.SERVICE,
        'teaching_institution': defaults.PROFILE['university'],
    }


def _render_site_page(request, page):
    try:
        context = build_home_context()
    except Exception as exc:
        logger.warning('Failed to build page context: %s', exc)
        context = _fallback_context()

    reg = PAGE_REGISTRY.get(page['page_type'])
    if not reg:
        raise Http404

    context['current_page'] = page['slug']
    context['page_title'] = page['label']
    context['page_record'] = page

    if page['page_type'] == 'custom':
        context['custom_content'] = page.get('custom_content') or ''
        context['custom_paragraphs'] = [
            p.strip() for p in (page.get('custom_content') or '').split('\n\n') if p.strip()
        ]

    return render(request, reg['template'], context)


def site_page_root(request):
    page = get_home_page()
    if not page:
        raise Http404('No pages configured. Run: python manage.py seed_pages')
    return _render_site_page(request, page)


def site_page(request, slug):
    page = get_site_page_by_slug(slug)
    if not page or not page.get('is_enabled'):
        raise Http404

    home = get_home_page()
    if home and page['id'] == home['id'] and request.path != '/':
        return redirect('site_home')

    return _render_site_page(request, page)
