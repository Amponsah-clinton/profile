import mimetypes
import time
import uuid

from django.conf import settings

from website.supabase_client import get_supabase

ALLOWED_IMAGE_TYPES = {'image/jpeg', 'image/png', 'image/webp', 'image/gif'}
ALLOWED_CV_TYPES = {
    'application/pdf': 'pdf',
    'application/msword': 'doc',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document': 'docx',
}
MAX_CV_BYTES = 10 * 1024 * 1024


def ensure_storage_bucket():
    """Create the public storage bucket if it does not exist."""
    sb = get_supabase(anon=False)
    bucket = settings.SUPABASE_STORAGE_BUCKET
    try:
        sb.storage.create_bucket(bucket, options={'public': True})
    except Exception:
        pass  # bucket already exists


def upload_profile_photo(uploaded_file):
    """Upload image to Supabase Storage and return the public URL."""
    ensure_storage_bucket()

    content_type = uploaded_file.content_type or mimetypes.guess_type(uploaded_file.name)[0]
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise ValueError('Please upload a JPEG, PNG, WebP, or GIF image.')

    if uploaded_file.size > 5 * 1024 * 1024:
        raise ValueError('Image must be 5 MB or smaller.')

    ext = uploaded_file.name.rsplit('.', 1)[-1].lower() if '.' in uploaded_file.name else 'jpg'
    if ext not in ('jpg', 'jpeg', 'png', 'webp', 'gif'):
        ext = 'jpg'

    filename = f"photos/{uuid.uuid4().hex}_{int(time.time())}.{ext}"
    bucket = settings.SUPABASE_STORAGE_BUCKET
    sb = get_supabase(anon=False)

    file_bytes = uploaded_file.read()
    sb.storage.from_(bucket).upload(
        filename,
        file_bytes,
        file_options={'content-type': content_type, 'upsert': 'true'},
    )

    result = sb.storage.from_(bucket).get_public_url(filename)
    if isinstance(result, dict):
        return result.get('publicUrl') or result.get('publicURL') or str(result)
    return result


def upload_profile_cv(uploaded_file):
    """Upload CV document to Supabase Storage and return the public URL."""
    ensure_storage_bucket()

    content_type = uploaded_file.content_type or mimetypes.guess_type(uploaded_file.name)[0]
    ext = None
    if content_type in ALLOWED_CV_TYPES:
        ext = ALLOWED_CV_TYPES[content_type]
    elif uploaded_file.name and '.' in uploaded_file.name:
        guessed = uploaded_file.name.rsplit('.', 1)[-1].lower()
        if guessed in ('pdf', 'doc', 'docx'):
            ext = guessed
            content_type = {
                'pdf': 'application/pdf',
                'doc': 'application/msword',
                'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            }[guessed]

    if not ext:
        raise ValueError('Please upload a PDF or Word document (.pdf, .doc, .docx).')

    if uploaded_file.size > MAX_CV_BYTES:
        raise ValueError('CV must be 10 MB or smaller.')

    filename = f"cv/{uuid.uuid4().hex}_{int(time.time())}.{ext}"
    bucket = settings.SUPABASE_STORAGE_BUCKET
    sb = get_supabase(anon=False)

    file_bytes = uploaded_file.read()
    sb.storage.from_(bucket).upload(
        filename,
        file_bytes,
        file_options={'content-type': content_type, 'upsert': 'true'},
    )

    result = sb.storage.from_(bucket).get_public_url(filename)
    if isinstance(result, dict):
        return result.get('publicUrl') or result.get('publicURL') or str(result)
    return result
