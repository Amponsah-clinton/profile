"""Maps page types to templates and dashboard routes."""

PAGE_REGISTRY = {
    'biography': {
        'default_label': 'Biography',
        'default_slug': 'biography',
        'icon': 'fa-user',
        'template': 'website/pages/biography.html',
        'dashboard_url': 'dashboard_profile',
        'builtin': True,
    },
    'news': {
        'default_label': 'News',
        'default_slug': 'news',
        'icon': 'fa-newspaper',
        'template': 'website/pages/news.html',
        'dashboard_url': 'dashboard_news_list',
        'builtin': True,
    },
    'research': {
        'default_label': 'Research',
        'default_slug': 'research',
        'icon': 'fa-flask',
        'template': 'website/pages/research.html',
        'dashboard_url': 'dashboard_research_list',
        'builtin': True,
    },
    'education': {
        'default_label': 'Education',
        'default_slug': 'education',
        'icon': 'fa-graduation-cap',
        'template': 'website/pages/education.html',
        'dashboard_url': 'dashboard_education_list',
        'builtin': True,
    },
    'publications': {
        'default_label': 'Publications',
        'default_slug': 'publications',
        'icon': 'fa-book',
        'template': 'website/pages/publications.html',
        'dashboard_url': 'dashboard_publications_list',
        'builtin': True,
    },
    'teaching': {
        'default_label': 'Teaching',
        'default_slug': 'teaching',
        'icon': 'fa-chalkboard-teacher',
        'template': 'website/pages/teaching.html',
        'dashboard_url': 'dashboard_teaching_list',
        'builtin': True,
    },
    'awards': {
        'default_label': 'Honors & Awards',
        'default_slug': 'awards',
        'icon': 'fa-trophy',
        'template': 'website/pages/awards.html',
        'dashboard_url': 'dashboard_awards_list',
        'builtin': True,
    },
    'service': {
        'default_label': 'Service',
        'default_slug': 'service',
        'icon': 'fa-hands-helping',
        'template': 'website/pages/service.html',
        'dashboard_url': 'dashboard_service_list',
        'builtin': True,
    },
    'custom': {
        'default_label': 'Custom Page',
        'default_slug': 'custom',
        'icon': 'fa-file-alt',
        'template': 'website/pages/custom.html',
        'dashboard_url': 'dashboard_page_content',
        'builtin': False,
    },
}

BUILTIN_SEEDS = [
    {'slug': info['default_slug'], 'label': info['default_label'], 'page_type': ptype,
     'sort_order': i * 10, 'icon': info['icon'], 'is_enabled': True}
    for i, (ptype, info) in enumerate(PAGE_REGISTRY.items()) if info['builtin']
]
