import re
from datetime import datetime

from django import template
from django.utils.html import mark_safe
from django.utils.safestring import mark_safe as _mark_safe

register = template.Library()


@register.filter
def initials(name):
    if not name:
        return 'YN'
    parts = [p for p in re.split(r'\s+', name.strip()) if p]
    if len(parts) >= 2:
        return (parts[0][0] + parts[-1][0]).upper()
    return name[:2].upper()


@register.filter
def tel_href(phone):
    if not phone:
        return ''
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 10:
        return f'+1{digits}'
    if digits:
        return f'+{digits}'
    return ''


@register.filter
def news_month(value):
    """Format ISO date or datetime as 'Jun 2025'."""
    if not value:
        return ''
    if isinstance(value, str):
        value = value[:10]
        dt = datetime.strptime(value, '%Y-%m-%d')
    else:
        dt = value
    return dt.strftime('%b %Y')


@register.filter
def news_datetime(value):
    if not value:
        return ''
    if isinstance(value, str):
        return value[:7]
    return value.strftime('%Y-%m')


@register.filter
def pub_label(pub_id):
    if not pub_id:
        return ''
    pid = str(pub_id).strip()
    if not pid.endswith('.'):
        pid += '.'
    return pid


@register.simple_tag
def pub_links(pub):
    """Render [PDF] [DOI] [Slides] link group for a publication row."""
    links = []
    if pub.get('pdf_url'):
        links.append(f'<a href="{pub["pdf_url"]}">PDF</a>')
    if pub.get('doi_url'):
        links.append(f'<a href="{pub["doi_url"]}">DOI</a>')
    if pub.get('slides_url'):
        links.append(f'<a href="{pub["slides_url"]}">Slides</a>')
    if not links:
        return ''
    return _mark_safe('[' + '] ['.join(links) + ']')


@register.filter
def get_item(mapping, key):
    if not mapping:
        return ''
    val = mapping.get(key, '')
    if isinstance(val, str) and len(val) > 100:
        return val[:100] + '…'
    return val


@register.filter
def award_text(item):
    if isinstance(item, dict):
        return mark_safe(item.get('label', ''))
    return mark_safe(item)
