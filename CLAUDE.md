# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# First-time setup (run in order)
python manage.py migrate                    # Create SQLite tables for Django auth/sessions
python manage.py create_dashboard_user      # Create the admin login (reads from .env)
python manage.py seed_pages                 # Seed site_pages table in Supabase

# Run the dev server
python manage.py runserver                  # Django site at http://127.0.0.1:8000/

# Other management commands
python manage.py test_supabase              # Verify Supabase connection
python manage.py setup_supabase             # One-time Supabase table/RLS setup
python manage.py setup_storage              # Create 'profile' storage bucket
python manage.py seed_content               # Seed sample content rows
```

The static JS frontend (`index.html` / `admin/index.html`) needs no server — open directly in a browser. It reads its Supabase credentials from `config.js` (not `.env`).

## Architecture: Two Coexisting Systems

There are **two completely independent frontends** sharing the same Supabase database:

### 1. Django site (`http://127.0.0.1:8000/`)
Server-rendered. URLs route through `academic_profile/urls.py` → `website/urls.py` → `views.py`. Every request calls `build_home_context()` in `context_builders.py`, which fetches live data from Supabase via `supabase_helpers.py` and merges it with `defaults.py` fallbacks. Templates live in `templates/`.

Admin dashboard is at `/dashboard/` (login required). It reads/writes Supabase using the **service role key** via `admin_db.py`. The public site reads with the **anon key** via `supabase_helpers.py`.

### 2. Static JS frontend (`index.html` / `admin/index.html`)
Pure JavaScript ES modules. `app.js` renders the public page; `admin/app.js` is the JS admin. Both import the Supabase JS client via CDN ESM and read credentials from `config.js` (`window.SUPABASE_URL` / `window.SUPABASE_ANON_KEY`). Changes made here do NOT affect the Django site, and vice versa — they are separate rendering layers on the same DB.

## Supabase Schema

The authoritative schema is `sql/schema.sql` (unified, idempotent, safe to re-run). The older `supabase/schema.sql` is a subset — prefer `sql/schema.sql`.

Key tables:
- `site_profile` — singleton row (always use `.limit(1)`, never `.single()`)
- `site_pages` — navigation structure; seeded by `python manage.py seed_pages`; drives the URL slug system
- `news_items`, `research_interests`, `education_entries`, `publications`, `teaching_courses`, `awards`, `service_entries` — content tables
- `site_sections`, `custom_pages` — used by the JS admin only

All tables have RLS: public SELECT for anonymous, full access for authenticated. The DO block in `sql/schema.sql` drops and recreates policies by querying `pg_policies` — this is the idempotent pattern to follow for any RLS changes.

## Page Routing (Django)

Pages are driven by the `site_pages` Supabase table, not hardcoded routes. `page_registry.py` maps `page_type` strings (`biography`, `news`, `custom`, etc.) to templates and dashboard URLs. `pages_db.py` is the CRUD layer for `site_pages`. The root URL serves the lowest `sort_order` enabled page.

## Key Design Rules

**`_merge_profile` in `context_builders.py`**: uses `if value is not None:` (NOT `not in (None, '')`). Empty string means the user cleared a field; it must propagate through so the template `{% if field %}` guard hides it correctly.

**Profile singleton**: always fetch with `.limit(1)` and access `data[0]`. Never use `.single()` — it silently returns `null` for 2+ rows (possible if seed ran multiple times).

**`admin_db.py` vs `supabase_helpers.py`**: `admin_db.py` uses the service role key and is write-capable (used by Django dashboard). `supabase_helpers.py` uses the anon key and is read-only (used by the public site).

**Teaching/Service grouping**: stored as flat rows in DB (`teaching_courses.institution`, `service_entries.category`), grouped at render time — in Python via `collections.defaultdict` (`context_builders.py`), in JS via `Map` (`app.js`).

**Social links**: stored as URL columns directly on `site_profile` (`scholar_url`, `researchgate_url`, `linkedin_url`, `github_url`, `orcid_url`). There is no separate `social_links` table.

## Environment

All credentials live in `.env`. For the JS static site, credentials must also be set in `config.js` (separate file, not read by Django).

Required `.env` keys: `SUPABASE_URL`, `SUPABASE_KEY` (anon), `SUPABASE_SERVICE_KEY`, `SECRET_KEY`, `DASHBOARD_USERNAME`, `DASHBOARD_EMAIL`, `DASHBOARD_PASSWORD`.
