"""
Supabase client singleton for the academic profile site.
"""

from django.conf import settings
from supabase import Client, create_client

_client = None
_admin_client = None


def get_supabase(anon=True) -> Client:
    """Return a cached Supabase client (anon or service role)."""
    global _client, _admin_client

    if anon:
        if _client is None:
            _client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        return _client

    if _admin_client is None:
        _admin_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_KEY)
    return _admin_client
