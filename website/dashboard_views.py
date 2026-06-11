import json

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from website import admin_db
from storage3.exceptions import StorageApiError

from website.storage_helpers import upload_profile_cv, upload_profile_photo
from website.dashboard_forms import (
    AwardForm,
    CustomContentForm,
    CustomPageForm,
    EducationForm,
    LabelForm,
    LoginForm,
    NewsForm,
    ProfileForm,
    PublicationForm,
    ServiceForm,
    SitePageForm,
)
from website.page_registry import PAGE_REGISTRY
from website import pages_db

def _dash_context(request, page_title, active=''):
    return {
        'page_title': page_title,
        'active_page': active,
        'nav_sections': pages_db.build_dashboard_nav(),
        'user': request.user,
    }


def dashboard_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard_home')

    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        identifier = form.cleaned_data['username'].strip()
        password = form.cleaned_data['password'].rstrip('.')

        user = authenticate(request, username=identifier, password=password)
        if user is None and '@' in identifier:
            try:
                account = User.objects.get(email__iexact=identifier)
                user = authenticate(request, username=account.username, password=password)
            except User.DoesNotExist:
                user = None
        if user is None:
            try:
                account = User.objects.get(username__iexact=identifier)
                user = authenticate(request, username=account.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return redirect('dashboard_home')
        messages.error(request, 'Invalid username, email, or password.')

    return render(request, 'dashboard/login.html', {'form': form})


@login_required(login_url='dashboard_login')
def dashboard_logout(request):
    logout(request)
    return redirect('dashboard_login')


@login_required(login_url='dashboard_login')
def dashboard_home(request):
    stats = admin_db.get_dashboard_stats()
    chart_labels = ['News', 'Research', 'Education', 'Publications', 'Teaching', 'Awards', 'Service']
    chart_values = [
        stats.get('news_items', 0),
        stats.get('research_interests', 0),
        stats.get('education_entries', 0),
        stats.get('publications', 0),
        stats.get('teaching_courses', 0),
        stats.get('awards', 0),
        stats.get('service_entries', 0),
    ]
    ctx = _dash_context(request, 'Dashboard', '')
    ctx.update({
        'stats': stats,
        'chart_labels_json': json.dumps(chart_labels),
        'chart_values_json': json.dumps(chart_values),
    })
    return render(request, 'dashboard/home.html', ctx)


@login_required(login_url='dashboard_login')
def dashboard_profile(request):
    profile = admin_db.get_profile()
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = {
                k: v for k, v in form.cleaned_data.items()
                if k not in ('photo', 'cv', 'remove_cv')
            }
            try:
                if form.cleaned_data.get('photo'):
                    data['photo_url'] = upload_profile_photo(form.cleaned_data['photo'])
                elif profile.get('photo_url'):
                    data['photo_url'] = profile['photo_url']

                if form.cleaned_data.get('remove_cv'):
                    data['cv_url'] = ''
                    data['cv_filename'] = ''
                elif form.cleaned_data.get('cv'):
                    data['cv_url'] = upload_profile_cv(form.cleaned_data['cv'])
                    data['cv_filename'] = form.cleaned_data['cv'].name
                else:
                    data['cv_url'] = profile.get('cv_url') or ''
                    data['cv_filename'] = profile.get('cv_filename') or ''
            except (ValueError, StorageApiError) as exc:
                messages.error(request, str(exc) if isinstance(exc, ValueError) else f'Upload failed: {exc}')
                ctx = _dash_context(request, 'Profile', pages_db.active_slug_for_type('biography'))
                ctx.update({
                    'form': form,
                    'photo_url': profile.get('photo_url', ''),
                    'cv_url': profile.get('cv_url', ''),
                    'cv_filename': profile.get('cv_filename', ''),
                })
                return render(request, 'dashboard/profile.html', ctx)

            admin_db.update_profile(data)
            messages.success(request, 'Profile updated.')
            return redirect('dashboard_profile')
    else:
        form = ProfileForm(initial=profile)

    page = pages_db.get_page_by_type('biography', admin=True)
    ctx = _dash_context(request, page['label'] if page else 'Profile', pages_db.active_slug_for_type('biography'))
    ctx.update({
        'form': form,
        'photo_url': profile.get('photo_url', ''),
        'cv_url': profile.get('cv_url', ''),
        'cv_filename': profile.get('cv_filename', ''),
    })
    return render(request, 'dashboard/profile.html', ctx)


def _crud_list(request, page_type, title, rows, add_url_name, url_prefix, columns):
    ctx = _dash_context(request, title, pages_db.active_slug_for_type(page_type))
    ctx.update({
        'rows': rows,
        'add_url': add_url_name,
        'title': title,
        'url_prefix': url_prefix,
        'columns': columns,
        'edit_url_name': f'dashboard_{url_prefix}_edit',
        'delete_url_name': f'dashboard_{url_prefix}_delete',
    })
    return render(request, 'dashboard/list.html', ctx)


def _crud_form(request, page_type, title, form_class, table, list_url_name, row_id=None, initial=None):
    row = admin_db.get_row(table, row_id) if row_id else None
    form = form_class(request.POST or None, initial=row or initial)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        if row_id:
            admin_db.update_row(table, row_id, data)
            messages.success(request, f'{title} updated.')
        else:
            admin_db.insert_row(table, data)
            messages.success(request, f'{title} added.')
        return redirect(list_url_name)
    ctx = _dash_context(request, f'Edit {title}' if row_id else f'Add {title}', pages_db.active_slug_for_type(page_type))
    ctx.update({'form': form, 'title': title, 'list_url': list_url_name})
    return render(request, 'dashboard/form.html', ctx)


@login_required(login_url='dashboard_login')
def dashboard_news_list(request):
    return _crud_list(
        request, 'news', 'News',
        admin_db.list_rows('news_items', 'event_date', desc=True),
        'dashboard_news_add', 'news',
        [('event_date', 'Date'), ('body', 'Content')],
    )


@login_required(login_url='dashboard_login')
def dashboard_news_add(request):
    return _crud_form(request, 'news', 'News', NewsForm, 'news_items', 'dashboard_news_list')


@login_required(login_url='dashboard_login')
def dashboard_news_edit(request, row_id):
    return _crud_form(request, 'news', 'News', NewsForm, 'news_items', 'dashboard_news_list', row_id)


@login_required(login_url='dashboard_login')
def dashboard_news_delete(request, row_id):
    admin_db.delete_row('news_items', row_id)
    messages.success(request, 'News item deleted.')
    return redirect('dashboard_news_list')


@login_required(login_url='dashboard_login')
def dashboard_research_list(request):
    return _crud_list(
        request, 'research', 'Research',
        admin_db.list_rows('research_interests'),
        'dashboard_research_add', 'research',
        [('label', 'Interest')],
    )


@login_required(login_url='dashboard_login')
def dashboard_research_add(request):
    return _crud_form(request, 'research', 'Research', LabelForm, 'research_interests', 'dashboard_research_list')


@login_required(login_url='dashboard_login')
def dashboard_research_edit(request, row_id):
    return _crud_form(request, 'research', 'Research', LabelForm, 'research_interests', 'dashboard_research_list', row_id)


@login_required(login_url='dashboard_login')
def dashboard_research_delete(request, row_id):
    admin_db.delete_row('research_interests', row_id)
    messages.success(request, 'Research item deleted.')
    return redirect('dashboard_research_list')


@login_required(login_url='dashboard_login')
def dashboard_education_list(request):
    return _crud_list(
        request, 'education', 'Education',
        admin_db.list_rows('education_entries'),
        'dashboard_education_add', 'education',
        [('degree', 'Degree'), ('institution', 'Institution')],
    )


@login_required(login_url='dashboard_login')
def dashboard_education_add(request):
    return _crud_form(request, 'education', 'Education', EducationForm, 'education_entries', 'dashboard_education_list')


@login_required(login_url='dashboard_login')
def dashboard_education_edit(request, row_id):
    return _crud_form(request, 'education', 'Education', EducationForm, 'education_entries', 'dashboard_education_list', row_id)


@login_required(login_url='dashboard_login')
def dashboard_education_delete(request, row_id):
    admin_db.delete_row('education_entries', row_id)
    messages.success(request, 'Education entry deleted.')
    return redirect('dashboard_education_list')


@login_required(login_url='dashboard_login')
def dashboard_publications_list(request):
    return _crud_list(
        request, 'publications', 'Publications',
        admin_db.list_publications(),
        'dashboard_publications_add', 'publications',
        [('pub_id', 'ID'), ('pub_type', 'Type'), ('year', 'Year')],
    )


@login_required(login_url='dashboard_login')
def dashboard_publications_add(request):
    return _crud_form(request, 'publications', 'Publication', PublicationForm, 'publications', 'dashboard_publications_list')


@login_required(login_url='dashboard_login')
def dashboard_publications_edit(request, row_id):
    return _crud_form(request, 'publications', 'Publication', PublicationForm, 'publications', 'dashboard_publications_list', row_id)


@login_required(login_url='dashboard_login')
def dashboard_publications_delete(request, row_id):
    admin_db.delete_row('publications', row_id)
    messages.success(request, 'Publication deleted.')
    return redirect('dashboard_publications_list')


@login_required(login_url='dashboard_login')
def dashboard_teaching_list(request):
    return _crud_list(
        request, 'teaching', 'Teaching',
        admin_db.list_rows('teaching_courses'),
        'dashboard_teaching_add', 'teaching',
        [('label', 'Course')],
    )


@login_required(login_url='dashboard_login')
def dashboard_teaching_add(request):
    return _crud_form(request, 'teaching', 'Teaching', LabelForm, 'teaching_courses', 'dashboard_teaching_list')


@login_required(login_url='dashboard_login')
def dashboard_teaching_edit(request, row_id):
    return _crud_form(request, 'teaching', 'Teaching', LabelForm, 'teaching_courses', 'dashboard_teaching_list', row_id)


@login_required(login_url='dashboard_login')
def dashboard_teaching_delete(request, row_id):
    admin_db.delete_row('teaching_courses', row_id)
    messages.success(request, 'Teaching entry deleted.')
    return redirect('dashboard_teaching_list')


@login_required(login_url='dashboard_login')
def dashboard_awards_list(request):
    return _crud_list(
        request, 'awards', 'Awards',
        admin_db.list_rows('awards'),
        'dashboard_awards_add', 'awards',
        [('year', 'Year'), ('label', 'Award')],
    )


@login_required(login_url='dashboard_login')
def dashboard_awards_add(request):
    return _crud_form(request, 'awards', 'Award', AwardForm, 'awards', 'dashboard_awards_list')


@login_required(login_url='dashboard_login')
def dashboard_awards_edit(request, row_id):
    return _crud_form(request, 'awards', 'Award', AwardForm, 'awards', 'dashboard_awards_list', row_id)


@login_required(login_url='dashboard_login')
def dashboard_awards_delete(request, row_id):
    admin_db.delete_row('awards', row_id)
    messages.success(request, 'Award deleted.')
    return redirect('dashboard_awards_list')


@login_required(login_url='dashboard_login')
def dashboard_service_list(request):
    return _crud_list(
        request, 'service', 'Service',
        admin_db.list_rows('service_entries'),
        'dashboard_service_add', 'service',
        [('category', 'Category'), ('label', 'Entry')],
    )


@login_required(login_url='dashboard_login')
def dashboard_service_add(request):
    return _crud_form(request, 'service', 'Service', ServiceForm, 'service_entries', 'dashboard_service_list')


@login_required(login_url='dashboard_login')
def dashboard_service_edit(request, row_id):
    return _crud_form(request, 'service', 'Service', ServiceForm, 'service_entries', 'dashboard_service_list', row_id)


@login_required(login_url='dashboard_login')
def dashboard_service_delete(request, row_id):
    admin_db.delete_row('service_entries', row_id)
    messages.success(request, 'Service entry deleted.')
    return redirect('dashboard_service_list')


@login_required(login_url='dashboard_login')
def dashboard_pages_list(request):
    pages = pages_db.list_site_pages(admin=True)
    home = pages_db.get_home_page()
    ctx = _dash_context(request, 'Manage Pages', 'pages-manage')
    ctx.update({'pages': pages, 'home_page_id': home['id'] if home else None})
    return render(request, 'dashboard/pages_list.html', ctx)


@login_required(login_url='dashboard_login')
def dashboard_page_edit(request, page_id):
    page = pages_db.get_site_page(page_id, admin=True)
    if not page:
        raise Http404

    form = SitePageForm(request.POST or None, initial=page)
    if request.method == 'POST' and form.is_valid():
        pages_db.update_site_page(page_id, form.cleaned_data)
        messages.success(request, f'Page "{form.cleaned_data["label"]}" updated.')
        return redirect('dashboard_pages_list')

    reg = PAGE_REGISTRY.get(page['page_type'], {})
    ctx = _dash_context(request, f'Edit: {page["label"]}', page['slug'])
    ctx.update({'form': form, 'page': page, 'is_builtin': reg.get('builtin', False)})
    return render(request, 'dashboard/page_edit.html', ctx)


@login_required(login_url='dashboard_login')
def dashboard_page_add(request):
    form = CustomPageForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        data['page_type'] = 'custom'
        pages_db.insert_site_page(data)
        messages.success(request, f'Page "{data["label"]}" created.')
        return redirect('dashboard_pages_list')

    ctx = _dash_context(request, 'Add Custom Page', 'pages-manage')
    ctx.update({'form': form})
    return render(request, 'dashboard/page_add.html', ctx)


@login_required(login_url='dashboard_login')
def dashboard_page_delete(request, page_id):
    try:
        pages_db.delete_site_page(page_id)
        messages.success(request, 'Page deleted.')
    except ValueError as exc:
        messages.error(request, str(exc))
    return redirect('dashboard_pages_list')


@login_required(login_url='dashboard_login')
def dashboard_page_content(request, page_id):
    page = pages_db.get_site_page(page_id, admin=True)
    if not page or page['page_type'] != 'custom':
        raise Http404

    form = CustomContentForm(request.POST or None, initial={'custom_content': page.get('custom_content', '')})
    if request.method == 'POST' and form.is_valid():
        pages_db.update_site_page(page_id, {'custom_content': form.cleaned_data['custom_content']})
        messages.success(request, 'Page content saved.')
        return redirect('dashboard_page_content', page_id=page_id)

    ctx = _dash_context(request, page['label'], page['slug'])
    ctx.update({'form': form, 'page': page})
    return render(request, 'dashboard/page_content.html', ctx)
