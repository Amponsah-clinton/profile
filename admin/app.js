// admin/app.js — full dashboard: auth + CRUD for all content + photo upload
import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm';

const sb = createClient(window.SUPABASE_URL, window.SUPABASE_ANON_KEY);

// ── State ─────────────────────────────────────────────────────────────────────
let currentSection = 'profile';
let cache = {};

// ── Helpers ───────────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');

function toast(msg, type = 'success') {
  const t = $('toast');
  t.textContent = msg;
  t.className = `toast show ${type}`;
  setTimeout(() => { t.className = 'toast hidden'; }, 3000);
}

function showSaved() {
  const si = $('save-indicator');
  si.style.display = 'inline';
  setTimeout(() => { si.style.display = 'none'; }, 2500);
}

// ── Modal ─────────────────────────────────────────────────────────────────────
let modalResolve = null;

function openModal(title, bodyHtml, { wide = false } = {}) {
  $('modal-title').textContent = title;
  $('modal-body').innerHTML = bodyHtml;
  $('modal').classList.remove('hidden');
  if (wide) $('modal').querySelector('.modal-box').style.maxWidth = '720px';
  $('modal').querySelector('.modal-box').querySelector('input, textarea')?.focus();
  return new Promise(resolve => { modalResolve = resolve; });
}

function closeModal(result) {
  $('modal').classList.add('hidden');
  $('modal').querySelector('.modal-box').style.maxWidth = '';
  if (modalResolve) { modalResolve(result); modalResolve = null; }
}

$('modal-close').addEventListener('click', () => closeModal(null));
$('modal-cancel').addEventListener('click', () => closeModal(null));
$('modal-save').addEventListener('click', () => closeModal('save'));

// ── Auth ──────────────────────────────────────────────────────────────────────
async function checkAuth() {
  const { data: { session } } = await sb.auth.getSession();
  if (session) { showDashboard(); await loadAll(); } else { showLogin(); }
  sb.auth.onAuthStateChange((event, session) => {
    if (event === 'SIGNED_IN')  { showDashboard(); loadAll(); }
    if (event === 'SIGNED_OUT') showLogin();
  });
}

$('login-form').addEventListener('submit', async e => {
  e.preventDefault();
  const btn = $('login-btn');
  btn.disabled = true; btn.textContent = 'Signing in…';
  const { error } = await sb.auth.signInWithPassword({
    email: $('login-email').value,
    password: $('login-password').value
  });
  if (error) {
    const el = $('login-error');
    el.textContent = error.message;
    el.style.display = 'block';
  }
  btn.disabled = false; btn.textContent = 'Sign In';
});

$('logout-btn').addEventListener('click', () => sb.auth.signOut());

function showLogin()     { $('login-screen').classList.remove('hidden'); $('dashboard').classList.add('hidden'); }
function showDashboard() { $('login-screen').classList.add('hidden');    $('dashboard').classList.remove('hidden'); }

// ── Data loading ──────────────────────────────────────────────────────────────
async function loadAll() {
  const [
    { data: profileRows },{ data: sections },
    { data: news },       { data: research },
    { data: education },  { data: pubs },
    { data: teaching },   { data: awards },
    { data: service },    { data: pages }
  ] = await Promise.all([
    sb.from('site_profile').select('*').order('id').limit(1),
    sb.from('site_sections').select('*').order('sort_order'),
    sb.from('news_items').select('*').order('sort_order'),
    sb.from('research_interests').select('*').order('sort_order'),
    sb.from('education_entries').select('*').order('sort_order'),
    sb.from('publications').select('*').order('sort_order'),
    sb.from('teaching_courses').select('*').order('sort_order'),
    sb.from('awards').select('*').order('sort_order'),
    sb.from('service_entries').select('*').order('sort_order'),
    sb.from('custom_pages').select('*').order('sort_order')
  ]);
  cache = {
    profile:   profileRows?.[0] ?? null,
    sections: sections  || [],
    news:     news      || [],
    research: research  || [],
    education:education || [],
    pubs:     pubs      || [],
    teaching: teaching  || [],
    awards:   awards    || [],
    service:  service   || [],
    pages:    pages     || []
  };
  navigateTo(currentSection);
}

// ── Sidebar nav ───────────────────────────────────────────────────────────────
document.querySelectorAll('.nav-item').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    navigateTo(btn.dataset.section);
  });
});

function navigateTo(section) {
  currentSection = section;
  const main = $('admin-main');
  switch (section) {
    case 'profile':      main.innerHTML = renderProfileEditor();      bindProfileEditor();      break;
    case 'social':       main.innerHTML = renderSocialEditor();       bindSocialEditor();       break;
    case 'sections':     main.innerHTML = renderSectionsEditor();     bindSectionsEditor();     break;
    case 'biography':    main.innerHTML = renderBiographyEditor();    bindBiographyEditor();    break;
    case 'news':         main.innerHTML = renderListEditor('news');    bindListEditor('news',     cache.news);     break;
    case 'research':     main.innerHTML = renderListEditor('research');bindListEditor('research', cache.research); break;
    case 'education':    main.innerHTML = renderEducationEditor();    bindEducationEditor();    break;
    case 'publications': main.innerHTML = renderPublicationsEditor(); bindPublicationsEditor(); break;
    case 'teaching':     main.innerHTML = renderTeachingEditor();     bindTeachingEditor();     break;
    case 'awards':       main.innerHTML = renderListEditor('awards'); bindListEditor('awards',   cache.awards);   break;
    case 'service':      main.innerHTML = renderServiceEditor();      bindServiceEditor();      break;
    case 'pages':        main.innerHTML = renderPagesEditor();        bindPagesEditor();        break;
  }
}

// ── Reorder helpers ───────────────────────────────────────────────────────────
async function reorder(table, orderField, items, idx, dir) {
  const swap = idx + dir;
  if (swap < 0 || swap >= items.length) return;
  const a = items[idx], b = items[swap];
  await Promise.all([
    sb.from(table).update({ [orderField]: b[orderField] }).eq('id', a.id),
    sb.from(table).update({ [orderField]: a[orderField] }).eq('id', b.id)
  ]);
  await loadAll();
}

function orderBtns(idx, total) {
  return `<div class="order-btns">
    <button class="btn-order btn-up"   data-idx="${idx}" ${idx === 0           ? 'disabled' : ''} title="Move up">▲</button>
    <button class="btn-order btn-down" data-idx="${idx}" ${idx === total - 1   ? 'disabled' : ''} title="Move down">▼</button>
  </div>`;
}

function toggleHtml(id, checked, label = 'Visible') {
  return `<label class="toggle-wrap">
    <span class="toggle">
      <input type="checkbox" id="${id}" ${checked ? 'checked' : ''}>
      <span class="toggle-track"></span>
      <span class="toggle-thumb"></span>
    </span>
    ${label}
  </label>`;
}

// helper: save to site_profile — always re-fetches the real row id to avoid duplicates
async function saveProfile(data) {
  const { data: rows } = await sb.from('site_profile').select('id').order('id').limit(1);
  const existingId = rows?.[0]?.id;
  if (existingId) {
    const { error } = await sb.from('site_profile').update(data).eq('id', existingId);
    return { error };
  }
  const { error } = await sb.from('site_profile').insert(data);
  return { error };
}

// ── PROFILE EDITOR ────────────────────────────────────────────────────────────
function renderProfileEditor() {
  const p = cache.profile || {};
  return `<div class="editor-header">
    <div><div class="editor-title">Profile Info</div><div class="editor-desc">Your name, photo, title, affiliation and contact details.</div></div>
  </div>
  <div class="profile-form">
    <div class="form-section-label">Photo</div>
    <div class="photo-upload-area" id="photo-drop">
      ${p.photo_url
        ? `<img class="photo-preview" id="photo-preview" src="${esc(p.photo_url)}" alt="Profile photo">`
        : `<div style="width:90px;height:112px;background:var(--bg-subtle);border-radius:4px;margin:0 auto 0.75rem;border:1px solid var(--rule)"></div>`}
      <p class="photo-upload-hint"><strong>Click or drag</strong> to upload a new photo</p>
      <p class="photo-upload-hint" style="font-size:0.73rem;margin-top:0.2rem">Saved to the <code>profile</code> Supabase Storage bucket</p>
      <p id="upload-progress" class="upload-progress" style="display:none">Uploading…</p>
      <input type="file" id="photo-file" accept="image/*" style="display:none">
    </div>

    <div class="form-section-label">Name</div>
    <div class="field-row">
      <div class="field-group"><label>Full Name</label><input id="p-name" type="text" value="${esc(p.full_name)}"></div>
      <div class="field-group"><label>Name (alternate / Chinese)</label><input id="p-name-alt" type="text" value="${esc(p.name_alt)}" placeholder="（姓名）"></div>
    </div>

    <div class="form-section-label">Position</div>
    <div class="field-group"><label>Title</label><input id="p-title" type="text" value="${esc(p.title)}"></div>

    <div class="form-section-label">Affiliation</div>
    <div class="field-group"><label>Primary Department / Lab</label><input id="p-dept1" type="text" value="${esc(p.department_1)}"></div>
    <div class="field-group"><label>Secondary Department (optional)</label><input id="p-dept2" type="text" value="${esc(p.department_2)}" placeholder="e.g. Department of Computer Science (Courtesy)"></div>
    <div class="field-group"><label>University / Institution</label><input id="p-university" type="text" value="${esc(p.university)}"></div>
    <div class="field-group"><label>Mailing Address</label><input id="p-address" type="text" value="${esc(p.address)}"></div>

    <div class="form-section-label">Contact</div>
    <div class="field-row">
      <div class="field-group"><label>Office</label><input id="p-office" type="text" value="${esc(p.office)}"></div>
      <div class="field-group"><label>Phone</label><input id="p-phone" type="tel" value="${esc(p.phone)}"></div>
    </div>
    <div class="field-group"><label>Email</label><input id="p-email" type="email" value="${esc(p.email)}"></div>

    <div style="margin-top:1.5rem">
      <button class="btn-primary" id="save-profile-btn">Save Profile</button>
    </div>
  </div>`;
}

function bindProfileEditor() {
  const fileInput = $('photo-file');
  const drop = $('photo-drop');

  drop.addEventListener('dragover', e => { e.preventDefault(); drop.classList.add('dragover'); });
  drop.addEventListener('dragleave', () => drop.classList.remove('dragover'));
  drop.addEventListener('drop', async e => {
    e.preventDefault(); drop.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) await handlePhotoUpload(file);
  });
  drop.addEventListener('click', () => fileInput.click());
  fileInput.addEventListener('change', async () => {
    if (fileInput.files[0]) await handlePhotoUpload(fileInput.files[0]);
  });

  $('save-profile-btn').addEventListener('click', async () => {
    const btn = $('save-profile-btn');
    btn.disabled = true; btn.textContent = 'Saving…';
    const { error } = await saveProfile({
      full_name:    $('p-name').value.trim(),
      name_alt:     $('p-name-alt').value.trim(),
      title:        $('p-title').value.trim(),
      department_1: $('p-dept1').value.trim(),
      department_2: $('p-dept2').value.trim(),
      university:   $('p-university').value.trim(),
      address:      $('p-address').value.trim(),
      office:       $('p-office').value.trim(),
      phone:        $('p-phone').value.trim(),
      email:        $('p-email').value.trim(),
      updated_at:   new Date().toISOString()
    });
    btn.disabled = false; btn.textContent = 'Save Profile';
    if (error) { toast(error.message, 'error'); return; }
    toast('Profile saved'); showSaved();
    await loadAll();
  });
}

async function handlePhotoUpload(file) {
  const prog = $('upload-progress');
  prog.style.display = 'block'; prog.textContent = 'Uploading…';
  const ext = file.name.split('.').pop().toLowerCase();
  const filename = `avatar_${Date.now()}.${ext}`;
  const { error: upErr } = await sb.storage.from('profile').upload(filename, file, { upsert: true });
  if (upErr) { prog.style.display = 'none'; toast(upErr.message, 'error'); return; }
  const { data: { publicUrl } } = sb.storage.from('profile').getPublicUrl(filename);
  await saveProfile({ photo_url: publicUrl, updated_at: new Date().toISOString() });
  prog.textContent = 'Saved!';
  setTimeout(() => { prog.style.display = 'none'; }, 1500);
  const preview = $('photo-preview');
  if (preview) preview.src = publicUrl;
  else {
    const img = document.createElement('img');
    img.className = 'photo-preview'; img.id = 'photo-preview'; img.src = publicUrl; img.alt = 'Profile photo';
    $('photo-drop').prepend(img);
  }
  toast('Photo uploaded'); showSaved();
  if (cache.profile) cache.profile.photo_url = publicUrl;
}

// ── SOCIAL LINKS EDITOR ───────────────────────────────────────────────────────
function renderSocialEditor() {
  const p = cache.profile || {};
  return `<div class="editor-header">
    <div><div class="editor-title">Social Links</div><div class="editor-desc">Links shown in the header. Leave blank to hide a link.</div></div>
    <button class="btn-primary" id="save-social-btn">Save</button>
  </div>
  <div class="profile-form">
    <div class="field-group">
      <label>Google Scholar URL</label>
      <input id="s-scholar" type="url" value="${esc(p.scholar_url)}" placeholder="https://scholar.google.com/citations?user=…">
    </div>
    <div class="field-group">
      <label>ORCID URL</label>
      <input id="s-orcid" type="url" value="${esc(p.orcid_url)}" placeholder="https://orcid.org/0000-0000-0000-0000">
    </div>
    <div class="field-group">
      <label>ResearchGate URL</label>
      <input id="s-researchgate" type="url" value="${esc(p.researchgate_url)}" placeholder="https://www.researchgate.net/profile/…">
    </div>
    <div class="field-group">
      <label>LinkedIn URL</label>
      <input id="s-linkedin" type="url" value="${esc(p.linkedin_url)}" placeholder="https://www.linkedin.com/in/…">
    </div>
    <div class="field-group">
      <label>GitHub URL</label>
      <input id="s-github" type="url" value="${esc(p.github_url)}" placeholder="https://github.com/…">
    </div>
  </div>`;
}

function bindSocialEditor() {
  $('save-social-btn').addEventListener('click', async () => {
    const btn = $('save-social-btn');
    btn.disabled = true; btn.textContent = 'Saving…';
    const { error } = await saveProfile({
      scholar_url:      $('s-scholar').value.trim(),
      orcid_url:        $('s-orcid').value.trim(),
      researchgate_url: $('s-researchgate').value.trim(),
      linkedin_url:     $('s-linkedin').value.trim(),
      github_url:       $('s-github').value.trim(),
      updated_at:       new Date().toISOString()
    });
    btn.disabled = false; btn.textContent = 'Save';
    if (error) { toast(error.message, 'error'); return; }
    toast('Social links saved'); showSaved(); await loadAll();
  });
}

// ── SECTIONS EDITOR ───────────────────────────────────────────────────────────
function renderSectionsEditor() {
  const rows = cache.sections.map((s, i) => `
    <div class="section-row" data-id="${s.id}">
      ${orderBtns(i, cache.sections.length)}
      <input type="text" class="sec-label" data-id="${s.id}" value="${esc(s.label)}">
      <span class="section-slug">${esc(s.slug)}</span>
      ${toggleHtml(`vis-sec-${s.id}`, s.visible)}
    </div>`).join('');
  return `<div class="editor-header">
    <div><div class="editor-title">Section Names</div><div class="editor-desc">Rename sections, change their order, or hide them from the public site.</div></div>
    <button class="btn-primary" id="save-sections-btn">Save All</button>
  </div>
  <div class="item-list">${rows || '<div class="empty-state">No sections found. Run the SQL schema to seed defaults.</div>'}</div>`;
}

function bindSectionsEditor() {
  $('admin-main').addEventListener('click', async e => {
    const upBtn   = e.target.closest('.btn-up');
    const downBtn = e.target.closest('.btn-down');
    if (upBtn)   reorder('site_sections', 'sort_order', cache.sections, +upBtn.dataset.idx,   -1);
    if (downBtn) reorder('site_sections', 'sort_order', cache.sections, +downBtn.dataset.idx,  1);
  });
  $('save-sections-btn').addEventListener('click', async () => {
    const btn = $('save-sections-btn');
    btn.disabled = true; btn.textContent = 'Saving…';
    const updates = cache.sections.map(s => {
      const labelEl = document.querySelector(`.sec-label[data-id="${s.id}"]`);
      const visEl   = document.getElementById(`vis-sec-${s.id}`);
      return sb.from('site_sections').update({
        label:   labelEl?.value.trim() || s.label,
        visible: visEl?.checked ?? s.visible
      }).eq('id', s.id);
    });
    await Promise.all(updates);
    btn.disabled = false; btn.textContent = 'Save All';
    toast('Sections saved'); showSaved(); await loadAll();
  });
}

// ── BIOGRAPHY EDITOR ──────────────────────────────────────────────────────────
function renderBiographyEditor() {
  const bio = cache.profile?.biography || '';
  return `<div class="editor-header">
    <div><div class="editor-title">Biography</div><div class="editor-desc">HTML supported. Use &lt;p&gt; tags for paragraphs, or separate paragraphs with a blank line.</div></div>
    <button class="btn-primary" id="save-bio-btn">Save</button>
  </div>
  <div class="bio-editor">
    <div class="field-group">
      <label>Content</label>
      <textarea id="bio-content" class="tall">${esc(bio)}</textarea>
    </div>
  </div>`;
}

function bindBiographyEditor() {
  $('save-bio-btn').addEventListener('click', async () => {
    const btn = $('save-bio-btn');
    btn.disabled = true; btn.textContent = 'Saving…';
    const { error } = await saveProfile({
      biography:  $('bio-content').value,
      updated_at: new Date().toISOString()
    });
    btn.disabled = false; btn.textContent = 'Save';
    if (error) { toast(error.message, 'error'); return; }
    toast('Biography saved'); showSaved(); await loadAll();
  });
}

// ── GENERIC LIST EDITOR (news, research, awards) ──────────────────────────────
const LIST_CONFIGS = {
  news: {
    table: 'news_items', orderField: 'sort_order',
    title: 'News Item', label: 'News', desc: 'News items shown on the public site.',
    displayTitle: i => {
      if (!i.event_date) return '—';
      return new Date(i.event_date + 'T00:00:00').toLocaleDateString('en-US', { year: 'numeric', month: 'short' });
    },
    displaySub: i => (i.body || '').replace(/<[^>]+>/g, '').slice(0, 80) + '…',
    hasVisible: true,
    fields: () => `
      <div class="field-group"><label>Date</label><input id="mf-date" type="date"></div>
      <div class="field-group"><label>Content (HTML allowed)</label><textarea id="mf-body" class="tall"></textarea></div>`,
    fromForm: () => ({ event_date: $('mf-date').value || null, body: $('mf-body').value }),
    fillForm: item => { $('mf-date').value = item.event_date || ''; $('mf-body').value = item.body || ''; }
  },
  research: {
    table: 'research_interests', orderField: 'sort_order',
    title: 'Research Interest', label: 'Research Interests', desc: 'Bullet-point research interests.',
    displayTitle: i => i.label,
    displaySub:   () => '',
    hasVisible: false,
    fields: () => `<div class="field-group"><label>Interest</label><input id="mf-label" type="text"></div>`,
    fromForm: () => ({ label: $('mf-label').value.trim() }),
    fillForm: item => { $('mf-label').value = item.label || ''; }
  },
  awards: {
    table: 'awards', orderField: 'sort_order',
    title: 'Award', label: 'Honors & Awards', desc: 'Award entries. HTML supported.',
    displayTitle: i => (i.label || '').replace(/<[^>]+>/g, '').slice(0, 80),
    displaySub:   i => i.year ? String(i.year) : '',
    hasVisible: false,
    fields: () => `
      <div class="field-group"><label>Award (HTML allowed)</label><textarea id="mf-label"></textarea></div>
      <div class="field-group"><label>Year (optional)</label><input id="mf-year" type="number" min="1900" max="2200" placeholder="2024"></div>`,
    fromForm: () => ({ label: $('mf-label').value, year: $('mf-year').value ? +$('mf-year').value : null }),
    fillForm: item => { $('mf-label').value = item.label || ''; $('mf-year').value = item.year || ''; }
  }
};

function renderListEditor(key) {
  const cfg   = LIST_CONFIGS[key];
  const items = cache[key] || [];
  const rows  = items.map((item, i) => `
    <div class="item-card">
      ${orderBtns(i, items.length)}
      <div class="item-card-body">
        <div class="item-card-title">${esc(cfg.displayTitle(item))}</div>
        ${cfg.displaySub(item) ? `<div class="item-card-sub">${esc(cfg.displaySub(item))}</div>` : ''}
      </div>
      <div class="item-card-actions">
        ${cfg.hasVisible ? toggleHtml(`vis-${key}-${item.id}`, item.visible) : ''}
        <button class="btn-secondary btn-edit" data-edit-item="${item.id}" data-list="${key}">Edit</button>
        <button class="btn-danger" data-del-item="${item.id}" data-list="${key}">Delete</button>
      </div>
    </div>`).join('');
  return `<div class="editor-header">
    <div><div class="editor-title">${cfg.label}</div><div class="editor-desc">${cfg.desc}</div></div>
    <button class="btn-primary" id="add-item-btn" data-list="${key}">+ Add</button>
  </div>
  <div class="item-list" id="item-list-${key}">${rows || '<div class="empty-state">No items yet.</div>'}</div>`;
}

function bindListEditor(key, items) {
  const cfg = LIST_CONFIGS[key];
  $('admin-main').addEventListener('click', async e => {
    const addBtn  = e.target.closest(`#add-item-btn[data-list="${key}"]`);
    const editBtn = e.target.closest(`[data-edit-item][data-list="${key}"]`);
    const delBtn  = e.target.closest(`[data-del-item][data-list="${key}"]`);
    const upBtn   = e.target.closest('.btn-up');
    const downBtn = e.target.closest('.btn-down');

    if (addBtn) {
      const result = await openModal(`Add ${cfg.title}`, cfg.fields());
      if (result !== 'save') return;
      const data = cfg.fromForm();
      data.sort_order = items.length + 1;
      await sb.from(cfg.table).insert(data);
      toast('Added'); showSaved(); await loadAll();
    }
    if (editBtn) {
      const item = items.find(i => String(i.id) === editBtn.dataset.editItem);
      if (!item) return;
      const result = await openModal(`Edit ${cfg.title}`, cfg.fields());
      cfg.fillForm(item);
      if (result !== 'save') return;
      await sb.from(cfg.table).update(cfg.fromForm()).eq('id', item.id);
      toast('Saved'); showSaved(); await loadAll();
    }
    if (delBtn) {
      if (!confirm('Delete this item?')) return;
      await sb.from(cfg.table).delete().eq('id', delBtn.dataset.delItem);
      toast('Deleted'); await loadAll();
    }
    if (upBtn)   reorder(cfg.table, cfg.orderField, items, +upBtn.dataset.idx,  -1);
    if (downBtn) reorder(cfg.table, cfg.orderField, items, +downBtn.dataset.idx,  1);
  });
  if (cfg.hasVisible) {
    $('admin-main').addEventListener('change', async e => {
      const toggle = e.target.id?.startsWith(`vis-${key}-`) ? e.target : null;
      if (toggle) {
        const id = toggle.id.replace(`vis-${key}-`, '');
        await sb.from(cfg.table).update({ visible: toggle.checked }).eq('id', id);
        showSaved();
      }
    });
  }
}

// ── EDUCATION EDITOR ──────────────────────────────────────────────────────────
function renderEducationEditor() {
  const items = cache.education;
  const rows  = items.map((e, i) => `
    <div class="item-card">
      ${orderBtns(i, items.length)}
      <div class="item-card-body">
        <div class="item-card-title">${esc(e.degree)}</div>
        <div class="item-card-sub">${esc(e.institution)}</div>
      </div>
      <div class="item-card-actions">
        <button class="btn-secondary btn-edit" data-id="${e.id}">Edit</button>
        <button class="btn-danger" data-del="${e.id}">Delete</button>
      </div>
    </div>`).join('');
  return `<div class="editor-header">
    <div><div class="editor-title">Education</div></div>
    <button class="btn-primary" id="add-edu-btn">+ Add</button>
  </div>
  <div class="item-list">${rows || '<div class="empty-state">No education entries.</div>'}</div>`;
}

function bindEducationEditor() {
  const fields  = () => `
    <div class="field-group"><label>Degree</label><input id="edu-degree" type="text" placeholder="Ph.D., Electrical Engineering"></div>
    <div class="field-group"><label>Institution</label><input id="edu-inst" type="text" placeholder="University Name, City, Country"></div>`;
  const fromForm = () => ({ degree: $('edu-degree').value.trim(), institution: $('edu-inst').value.trim() });
  const fill     = item => { $('edu-degree').value = item.degree || ''; $('edu-inst').value = item.institution || ''; };

  $('admin-main').addEventListener('click', async e => {
    if (e.target.closest('#add-edu-btn')) {
      const result = await openModal('Add Education', fields());
      if (result !== 'save') return;
      await sb.from('education_entries').insert({ ...fromForm(), sort_order: cache.education.length + 1 });
      toast('Added'); showSaved(); await loadAll();
    }
    const editBtn = e.target.closest('.btn-edit[data-id]');
    if (editBtn) {
      const item = cache.education.find(e => String(e.id) === editBtn.dataset.id);
      if (!item) return;
      const result = await openModal('Edit Education', fields());
      fill(item);
      if (result !== 'save') return;
      await sb.from('education_entries').update(fromForm()).eq('id', item.id);
      toast('Saved'); showSaved(); await loadAll();
    }
    const delBtn = e.target.closest('[data-del]');
    if (delBtn && delBtn.closest('.item-card')) {
      if (!confirm('Delete?')) return;
      await sb.from('education_entries').delete().eq('id', delBtn.dataset.del);
      toast('Deleted'); await loadAll();
    }
    const upBtn   = e.target.closest('.btn-up');
    const downBtn = e.target.closest('.btn-down');
    if (upBtn)   reorder('education_entries', 'sort_order', cache.education, +upBtn.dataset.idx,  -1);
    if (downBtn) reorder('education_entries', 'sort_order', cache.education, +downBtn.dataset.idx,  1);
  });
}

// ── PUBLICATIONS EDITOR ───────────────────────────────────────────────────────
let activePubTab = 'journal';

function renderPublicationsEditor() {
  const byType   = type => cache.pubs.filter(p => p.pub_type === type);
  const renderTab = type => {
    const items = byType(type);
    return `<div class="pub-tab-panel" id="pub-panel-${type}" ${type !== activePubTab ? 'style="display:none"' : ''}>
      <div style="margin-bottom:0.75rem"><button class="btn-primary btn-add-pub" data-type="${type}">+ Add</button></div>
      <div class="item-list">${items.map((p, i) => `
        <div class="item-card">
          ${orderBtns(i, items.length)}
          <div class="item-card-body">
            <div class="item-card-title">${esc(p.pub_id)} · ${(p.citation || '').replace(/<[^>]+>/g,'').slice(0,70)}…</div>
            ${p.award_note ? `<div class="item-card-sub" style="color:var(--accent-mid)">${esc(p.award_note)}</div>` : ''}
          </div>
          <div class="item-card-actions">
            ${toggleHtml(`vis-pub-${p.id}`, p.visible)}
            <button class="btn-secondary btn-edit-pub" data-id="${p.id}" data-type="${type}">Edit</button>
            <button class="btn-danger btn-del-pub" data-id="${p.id}">Delete</button>
          </div>
        </div>`).join('') || '<div class="empty-state">No entries.</div>'}
      </div>
    </div>`;
  };
  return `<div class="editor-header">
    <div><div class="editor-title">Publications</div><div class="editor-desc">HTML is supported in the Citation field (for &lt;em&gt;, &lt;strong&gt;, &amp;ldquo;, etc.).</div></div>
  </div>
  <div class="pub-tabs">
    <button class="pub-tab ${activePubTab==='journal'    ? 'active' : ''}" data-tab="journal">Journals</button>
    <button class="pub-tab ${activePubTab==='conference' ? 'active' : ''}" data-tab="conference">Conferences</button>
    <button class="pub-tab ${activePubTab==='workshop'   ? 'active' : ''}" data-tab="workshop">Preprints</button>
  </div>
  ${renderTab('journal')}${renderTab('conference')}${renderTab('workshop')}`;
}

function pubFields() {
  return `
    <div class="field-row">
      <div class="field-group"><label>Publication ID</label><input id="pub-id" type="text" placeholder="J5 / C8 / W1"></div>
      <div class="field-group"><label>Year</label><input id="pub-year" type="number" min="1900" max="2200" placeholder="2024"></div>
    </div>
    <div class="field-group"><label>Full Citation (HTML)</label><textarea id="pub-citation" class="tall" placeholder="Authors, &amp;ldquo;Title,&amp;rdquo; &lt;em&gt;Venue&lt;/em&gt;, Year."></textarea></div>
    <div class="field-group"><label>Award Note (leave blank if none)</label><input id="pub-award" type="text"></div>
    <div class="field-row">
      <div class="field-group"><label>PDF URL</label><input id="pub-pdf" type="url"></div>
      <div class="field-group"><label>DOI URL</label><input id="pub-doi" type="url"></div>
    </div>
    <div class="field-group"><label>Slides URL</label><input id="pub-slides" type="url"></div>`;
}

function pubFromForm(type) {
  return {
    pub_type:   type,
    pub_id:     $('pub-id').value.trim(),
    citation:   $('pub-citation').value,
    award_note: $('pub-award').value.trim(),
    pdf_url:    $('pub-pdf').value.trim(),
    doi_url:    $('pub-doi').value.trim(),
    slides_url: $('pub-slides').value.trim(),
    year:       $('pub-year').value ? +$('pub-year').value : null
  };
}

function fillPubForm(p) {
  $('pub-id').value      = p.pub_id    || '';
  $('pub-citation').value = p.citation  || '';
  $('pub-award').value   = p.award_note || '';
  $('pub-pdf').value     = p.pdf_url   || '';
  $('pub-doi').value     = p.doi_url   || '';
  $('pub-slides').value  = p.slides_url || '';
  $('pub-year').value    = p.year      || '';
}

function bindPublicationsEditor() {
  $('admin-main').addEventListener('click', async e => {
    const tab = e.target.closest('.pub-tab');
    if (tab) {
      activePubTab = tab.dataset.tab;
      document.querySelectorAll('.pub-tab').forEach(t => t.classList.toggle('active', t.dataset.tab === activePubTab));
      document.querySelectorAll('.pub-tab-panel').forEach(p => p.style.display = p.id === `pub-panel-${activePubTab}` ? '' : 'none');
    }
    const addBtn = e.target.closest('.btn-add-pub');
    if (addBtn) {
      const type   = addBtn.dataset.type;
      const result = await openModal(`Add ${type} publication`, pubFields(), { wide: true });
      if (result !== 'save') return;
      await sb.from('publications').insert({ ...pubFromForm(type), sort_order: cache.pubs.length + 1 });
      toast('Added'); showSaved(); await loadAll();
    }
    const editBtn = e.target.closest('.btn-edit-pub');
    if (editBtn) {
      const p      = cache.pubs.find(p => String(p.id) === editBtn.dataset.id);
      if (!p) return;
      const result = await openModal('Edit Publication', pubFields(), { wide: true });
      fillPubForm(p);
      if (result !== 'save') return;
      await sb.from('publications').update(pubFromForm(p.pub_type)).eq('id', p.id);
      toast('Saved'); showSaved(); await loadAll();
    }
    const delBtn = e.target.closest('.btn-del-pub');
    if (delBtn) {
      if (!confirm('Delete publication?')) return;
      await sb.from('publications').delete().eq('id', delBtn.dataset.id);
      toast('Deleted'); await loadAll();
    }
    const upBtn   = e.target.closest('.btn-up');
    const downBtn = e.target.closest('.btn-down');
    if (upBtn || downBtn) {
      const typed = cache.pubs.filter(p => p.pub_type === activePubTab);
      const idx   = +(upBtn || downBtn).dataset.idx;
      reorder('publications', 'sort_order', typed, idx, upBtn ? -1 : 1);
    }
  });
  $('admin-main').addEventListener('change', async e => {
    const m = e.target.id?.match(/^vis-pub-(.+)$/);
    if (m) { await sb.from('publications').update({ visible: e.target.checked }).eq('id', m[1]); showSaved(); }
  });
}

// ── TEACHING EDITOR ───────────────────────────────────────────────────────────
function renderTeachingEditor() {
  const items = cache.teaching;
  const rows  = items.map((t, i) => `
    <div class="item-card">
      ${orderBtns(i, items.length)}
      <div class="item-card-body">
        <div class="item-card-title">${esc(t.label)}</div>
        ${t.institution ? `<div class="item-card-sub">${esc(t.institution)}</div>` : ''}
      </div>
      <div class="item-card-actions">
        <button class="btn-secondary btn-edit" data-id="${t.id}">Edit</button>
        <button class="btn-danger" data-del="${t.id}">Delete</button>
      </div>
    </div>`).join('');
  return `<div class="editor-header">
    <div><div class="editor-title">Teaching</div><div class="editor-desc">Each row is one course. Courses with the same institution name are grouped together on the public site.</div></div>
    <button class="btn-primary" id="add-teach-btn">+ Add Course</button>
  </div>
  <div class="item-list">${rows || '<div class="empty-state">No teaching entries.</div>'}</div>`;
}

function bindTeachingEditor() {
  const fields  = () => `
    <div class="field-group"><label>Course</label><input id="teach-label" type="text" placeholder="ECE 566 — Wireless Networking (Fall 2024)"></div>
    <div class="field-group"><label>Institution (optional — used for grouping)</label><input id="teach-inst" type="text" placeholder="North Carolina State University"></div>`;
  const fromForm = () => ({ label: $('teach-label').value.trim(), institution: $('teach-inst').value.trim() });
  const fill     = item => { $('teach-label').value = item.label || ''; $('teach-inst').value = item.institution || ''; };

  $('admin-main').addEventListener('click', async e => {
    if (e.target.closest('#add-teach-btn')) {
      const result = await openModal('Add Course', fields());
      if (result !== 'save') return;
      await sb.from('teaching_courses').insert({ ...fromForm(), sort_order: cache.teaching.length + 1 });
      toast('Added'); showSaved(); await loadAll();
    }
    const editBtn = e.target.closest('.btn-edit[data-id]');
    if (editBtn) {
      const item   = cache.teaching.find(t => String(t.id) === editBtn.dataset.id);
      if (!item) return;
      const result = await openModal('Edit Course', fields());
      fill(item);
      if (result !== 'save') return;
      await sb.from('teaching_courses').update(fromForm()).eq('id', item.id);
      toast('Saved'); showSaved(); await loadAll();
    }
    const delBtn = e.target.closest('[data-del]');
    if (delBtn && delBtn.closest('.item-card')) {
      if (!confirm('Delete?')) return;
      await sb.from('teaching_courses').delete().eq('id', delBtn.dataset.del);
      toast('Deleted'); await loadAll();
    }
    const upBtn   = e.target.closest('.btn-up');
    const downBtn = e.target.closest('.btn-down');
    if (upBtn)   reorder('teaching_courses', 'sort_order', cache.teaching, +upBtn.dataset.idx,  -1);
    if (downBtn) reorder('teaching_courses', 'sort_order', cache.teaching, +downBtn.dataset.idx,  1);
  });
}

// ── SERVICE EDITOR ────────────────────────────────────────────────────────────
function renderServiceEditor() {
  const items = cache.service;
  const rows  = items.map((s, i) => `
    <div class="item-card">
      ${orderBtns(i, items.length)}
      <div class="item-card-body">
        <div class="item-card-title">${esc(s.label)}</div>
        <div class="item-card-sub">${esc(s.category)}</div>
      </div>
      <div class="item-card-actions">
        <button class="btn-secondary btn-edit-srv" data-id="${s.id}">Edit</button>
        <button class="btn-danger btn-del-srv" data-id="${s.id}">Delete</button>
      </div>
    </div>`).join('');
  return `<div class="editor-header">
    <div><div class="editor-title">Professional Service</div><div class="editor-desc">Each row is one service item. Items with the same category are grouped on the public site.</div></div>
    <button class="btn-primary" id="add-srv-btn">+ Add Item</button>
  </div>
  <div class="item-list">${rows || '<div class="empty-state">No service entries.</div>'}</div>`;
}

function bindServiceEditor() {
  const fields  = () => `
    <div class="field-group"><label>Category</label><input id="srv-cat" type="text" placeholder="Technical Program Committees"></div>
    <div class="field-group"><label>Item (HTML allowed)</label><textarea id="srv-label" rows="3" placeholder="IEEE INFOCOM (2020–present)"></textarea></div>`;
  const fromForm = () => ({ category: $('srv-cat').value.trim(), label: $('srv-label').value.trim() });
  const fill     = item => { $('srv-cat').value = item.category || ''; $('srv-label').value = item.label || ''; };

  $('admin-main').addEventListener('click', async e => {
    if (e.target.closest('#add-srv-btn')) {
      const result = await openModal('Add Service Item', fields());
      if (result !== 'save') return;
      await sb.from('service_entries').insert({ ...fromForm(), sort_order: cache.service.length + 1 });
      toast('Added'); showSaved(); await loadAll();
    }
    const editBtn = e.target.closest('.btn-edit-srv');
    if (editBtn) {
      const item   = cache.service.find(s => String(s.id) === editBtn.dataset.id);
      if (!item) return;
      const result = await openModal('Edit Service Item', fields());
      fill(item);
      if (result !== 'save') return;
      await sb.from('service_entries').update(fromForm()).eq('id', item.id);
      toast('Saved'); showSaved(); await loadAll();
    }
    const delBtn = e.target.closest('.btn-del-srv');
    if (delBtn) {
      if (!confirm('Delete?')) return;
      await sb.from('service_entries').delete().eq('id', delBtn.dataset.id);
      toast('Deleted'); await loadAll();
    }
    const upBtn   = e.target.closest('.btn-up');
    const downBtn = e.target.closest('.btn-down');
    if (upBtn)   reorder('service_entries', 'sort_order', cache.service, +upBtn.dataset.idx,  -1);
    if (downBtn) reorder('service_entries', 'sort_order', cache.service, +downBtn.dataset.idx,  1);
  });
}

// ── CUSTOM PAGES EDITOR ───────────────────────────────────────────────────────
function renderPagesEditor() {
  const rows = cache.pages.map((p, i) => `
    <div class="item-card">
      ${orderBtns(i, cache.pages.length)}
      <div class="item-card-body">
        <div class="item-card-title">${esc(p.title)}</div>
        <div class="item-card-sub">/${esc(p.slug)}</div>
      </div>
      <div class="item-card-actions">
        ${toggleHtml(`vis-page-${p.id}`, p.visible)}
        <button class="btn-secondary btn-edit-page" data-id="${p.id}">Edit</button>
        <button class="btn-danger btn-del-page" data-id="${p.id}">Delete</button>
      </div>
    </div>`).join('');
  return `<div class="editor-header">
    <div><div class="editor-title">Custom Pages</div><div class="editor-desc">Add extra sections (e.g. "Lab", "Gallery"). They appear in the nav after built-in sections.</div></div>
    <button class="btn-primary" id="add-page-btn">+ Add Page</button>
  </div>
  <div class="item-list">${rows || '<div class="empty-state">No custom pages yet.</div>'}</div>`;
}

function pageFields() {
  return `
    <div class="field-row">
      <div class="field-group"><label>Page Title</label><input id="pg-title" type="text" placeholder="Lab Members"></div>
      <div class="field-group"><label>Slug (URL key, no spaces)</label><input id="pg-slug" type="text" placeholder="lab"></div>
    </div>
    <div class="field-group"><label>Content (HTML)</label><textarea id="pg-content" class="tall"></textarea></div>`;
}

function bindPagesEditor() {
  $('admin-main').addEventListener('click', async e => {
    if (e.target.closest('#add-page-btn')) {
      const result = await openModal('Add Custom Page', pageFields(), { wide: true });
      if (result !== 'save') return;
      const slug = $('pg-slug').value.trim().toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
      await sb.from('custom_pages').insert({
        title: $('pg-title').value.trim(), slug, content: $('pg-content').value,
        sort_order: cache.pages.length + 1
      });
      toast('Page added'); showSaved(); await loadAll();
    }
    const editBtn = e.target.closest('.btn-edit-page');
    if (editBtn) {
      const p = cache.pages.find(p => String(p.id) === editBtn.dataset.id);
      if (!p) return;
      const result = await openModal('Edit Page', pageFields(), { wide: true });
      $('pg-title').value   = p.title   || '';
      $('pg-slug').value    = p.slug    || '';
      $('pg-content').value = p.content || '';
      if (result !== 'save') return;
      const slug = $('pg-slug').value.trim().toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
      await sb.from('custom_pages').update({
        title: $('pg-title').value.trim(), slug, content: $('pg-content').value
      }).eq('id', p.id);
      toast('Saved'); showSaved(); await loadAll();
    }
    const delBtn = e.target.closest('.btn-del-page');
    if (delBtn) {
      if (!confirm('Delete this page?')) return;
      await sb.from('custom_pages').delete().eq('id', delBtn.dataset.id);
      toast('Deleted'); await loadAll();
    }
    const upBtn   = e.target.closest('.btn-up');
    const downBtn = e.target.closest('.btn-down');
    if (upBtn)   reorder('custom_pages', 'sort_order', cache.pages, +upBtn.dataset.idx,  -1);
    if (downBtn) reorder('custom_pages', 'sort_order', cache.pages, +downBtn.dataset.idx,  1);
  });
  $('admin-main').addEventListener('change', async e => {
    const m = e.target.id?.match(/^vis-page-(.+)$/);
    if (m) { await sb.from('custom_pages').update({ visible: e.target.checked }).eq('id', m[1]); showSaved(); }
  });
}

// ── Boot ──────────────────────────────────────────────────────────────────────
checkAuth();
