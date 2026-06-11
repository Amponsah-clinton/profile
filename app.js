// app.js — public page: fetches everything from Supabase and renders dynamically
import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2/+esm';

const sb = createClient(window.SUPABASE_URL, window.SUPABASE_ANON_KEY);

const SVG = {
  linkedin: `<path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/>`,
  github:   `<path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/>`
};

// ── Helpers ──────────────────────────────────────────────────────────────────
function esc(s) {
  return String(s ?? '')
    .replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')
    .replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}

// ── Main load ─────────────────────────────────────────────────────────────────
async function loadPage() {
  const [
    { data: profileRows },
    { data: sections },
    { data: news },
    { data: research },
    { data: education },
    { data: pubs },
    { data: teaching },
    { data: awards },
    { data: service },
    { data: pages }
  ] = await Promise.all([
    sb.from('site_profile').select('*').order('id').limit(1),
    sb.from('site_sections').select('*').order('sort_order'),
    sb.from('news_items').select('*').eq('visible', true).order('sort_order'),
    sb.from('research_interests').select('*').order('sort_order'),
    sb.from('education_entries').select('*').order('sort_order'),
    sb.from('publications').select('*').eq('visible', true).order('sort_order'),
    sb.from('teaching_courses').select('*').order('sort_order'),
    sb.from('awards').select('*').order('sort_order'),
    sb.from('service_entries').select('*').order('sort_order'),
    sb.from('custom_pages').select('*').eq('visible', true).order('sort_order')
  ]);

  const profile = profileRows?.[0] ?? null;

  renderHeader(profile);

  const visibleSections = (sections || []).filter(s => s.visible);
  renderNav(visibleSections, pages || []);
  renderMain(visibleSections, { profile, news, research, education, pubs, teaching, awards, service }, pages || []);

  if (profile?.full_name) document.title = `${profile.full_name} | Home`;

  const lu = document.getElementById('last-updated');
  if (lu && profile?.updated_at) {
    const d = new Date(profile.updated_at);
    lu.setAttribute('datetime', d.toISOString().slice(0, 10));
    lu.textContent = d.toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
  }

  document.getElementById('page-loading')?.remove();
  initNavObserver();
}

// ── Header ────────────────────────────────────────────────────────────────────
function renderHeader(p) {
  if (!p) return;

  const photo = document.getElementById('profile-photo');
  if (photo) {
    if (p.photo_url) {
      photo.src = p.photo_url;
      photo.onerror = () => { photo.hidden = true; photo.parentElement.classList.add('portrait--placeholder'); };
    } else {
      photo.hidden = true;
      photo.parentElement.classList.add('portrait--placeholder');
    }
  }

  const initials = document.getElementById('portrait-initials');
  if (initials) initials.textContent = (p.full_name || '').split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();

  set('profile-name', p.full_name);
  setShow('profile-name-alt', p.name_alt, p.name_alt);
  set('profile-title', p.title);

  // Build affiliation from individual columns
  const aff = document.getElementById('profile-affiliation');
  if (aff) {
    const lines = [p.department_1, p.department_2, p.university].filter(Boolean);
    aff.innerHTML = lines.map(a => `<span>${esc(a)}</span>`).join('');
  }

  setShow('contact-office', p.office, p.office);
  document.getElementById('contact-office-row')?.style.setProperty('display', p.office ? '' : 'none');

  if (p.phone) {
    set('contact-phone', p.phone);
    document.getElementById('contact-phone-link')?.setAttribute('href', `tel:${p.phone.replace(/\D/g, '')}`);
  }
  document.getElementById('contact-phone-row')?.style.setProperty('display', p.phone ? '' : 'none');

  if (p.email) {
    set('contact-email', p.email);
    document.getElementById('contact-email-link')?.setAttribute('href', `mailto:${p.email}`);
  }
  document.getElementById('contact-email-row')?.style.setProperty('display', p.email ? '' : 'none');

  // Build social links from site_profile URL columns
  const ul = document.getElementById('profile-links');
  if (ul) {
    const links = [];
    if (p.scholar_url)      links.push({ url: p.scholar_url,      label: 'Google Scholar', icon: `<i class="ai ai-google-scholar" aria-hidden="true"></i>` });
    if (p.orcid_url)        links.push({ url: p.orcid_url,        label: 'ORCID',          icon: `<i class="ai ai-orcid" aria-hidden="true"></i>` });
    if (p.researchgate_url) links.push({ url: p.researchgate_url, label: 'ResearchGate',   icon: `<i class="ai ai-researchgate" aria-hidden="true"></i>` });
    if (p.linkedin_url)     links.push({ url: p.linkedin_url,     label: 'LinkedIn',       icon: `<svg aria-hidden="true" viewBox="0 0 24 24" width="14" height="14" fill="currentColor">${SVG.linkedin}</svg>` });
    if (p.github_url)       links.push({ url: p.github_url,       label: 'GitHub',         icon: `<svg aria-hidden="true" viewBox="0 0 24 24" width="14" height="14" fill="currentColor">${SVG.github}</svg>` });
    ul.innerHTML = links.map(lk =>
      `<li><a href="${esc(lk.url)}" rel="noopener noreferrer">${lk.icon}<span>${esc(lk.label)}</span></a></li>`
    ).join('');
  }
}

function set(id, val) {
  const e = document.getElementById(id);
  if (e) e.textContent = val || '';
}

function setShow(id, val, cond) {
  const e = document.getElementById(id);
  if (!e) return;
  e.textContent = val || '';
  e.style.display = cond ? '' : 'none';
}

// ── Navigation ────────────────────────────────────────────────────────────────
function renderNav(sections, pages) {
  const nav = document.getElementById('section-nav');
  if (!nav) return;
  const all = [...sections, ...pages.map(p => ({ slug: p.slug, label: p.title }))];
  nav.innerHTML = all.map((s, i) =>
    `<li><a href="#${esc(s.slug)}"${i === 0 ? ' class="is-active"' : ''}>${esc(s.label)}</a></li>`
  ).join('');
}

// ── Main content ──────────────────────────────────────────────────────────────
function renderMain(sections, data, pages) {
  const main = document.getElementById('main');
  if (!main) return;
  main.innerHTML = '';
  for (const s of sections) {
    const node = buildSection(s, data);
    if (node) main.appendChild(node);
  }
  for (const p of pages) {
    main.appendChild(buildCustomPage(p));
  }
}

function buildSection(s, d) {
  switch (s.slug) {
    case 'biography':    return mkBiography(s, d.profile);
    case 'news':         return mkNews(s, d.news || []);
    case 'research':     return mkList(s, d.research || [], r => `<li>${esc(r.label)}</li>`, 'research-list');
    case 'education':    return mkEducation(s, d.education || []);
    case 'publications': return mkPublications(s, d.pubs || []);
    case 'teaching':     return mkTeaching(s, d.teaching || []);
    case 'awards':       return mkAwardsList(s, d.awards || []);
    case 'service':      return mkService(s, d.service || []);
    default:             return null;
  }
}

function mkSection(s, inner) {
  const sec = document.createElement('section');
  sec.id = s.slug; sec.className = 'section'; sec.tabIndex = -1;
  sec.innerHTML = `<h2 class="section-title"><span>${esc(s.label)}</span></h2>${inner}`;
  return sec;
}

function mkBiography(s, profile) {
  const raw = profile?.biography || '';
  // Support both HTML (contains tags) and plain text (paragraphs split by \n\n)
  const hasHtml = /<[a-z][\s\S]*>/i.test(raw);
  const html = hasHtml
    ? raw
    : raw.split('\n\n').filter(Boolean).map(p => `<p>${esc(p.trim())}</p>`).join('');
  return mkSection(s, `<div class="prose">${html || '<p>No biography yet.</p>'}</div>`);
}

function mkNews(s, items) {
  if (!items.length) return mkSection(s, '<p class="section-note">No news yet.</p>');
  const rows = items.map(n => {
    const d = n.event_date ? new Date(n.event_date + 'T00:00:00') : null;
    const iso   = n.event_date || '';
    const label = d ? d.toLocaleDateString('en-US', { year: 'numeric', month: 'short' }) : '';
    return `<tr><th scope="row"><time datetime="${esc(iso)}">${esc(label)}</time></th><td>${n.body}</td></tr>`;
  }).join('');
  return mkSection(s,
    `<table class="news-table"><caption class="visually-hidden">Recent updates</caption><tbody>${rows}</tbody></table>`);
}

function mkList(s, items, rowFn, cls) {
  const lis = items.map(rowFn).join('');
  return mkSection(s, `<ul class="${cls}">${lis}</ul>`);
}

function mkEducation(s, items) {
  const lis = items.map(e =>
    `<li><span class="timeline-degree">${esc(e.degree)}</span><span class="timeline-inst">${esc(e.institution)}</span></li>`
  ).join('');
  return mkSection(s, `<ol class="timeline">${lis}</ol>`);
}

function mkPublications(s, items) {
  const grouped = { journal: [], conference: [], workshop: [] };
  for (const p of items) if (grouped[p.pub_type]) grouped[p.pub_type].push(p);
  const typeLabels = { journal: 'Journal Articles', conference: 'Conference Papers', workshop: 'Workshop & Demo Papers' };
  let html = `<p class="section-note">Representative works listed below.</p>`;
  for (const [type, label] of Object.entries(typeLabels)) {
    if (!grouped[type].length) continue;
    html += `<h3 class="subsection-title">${label}</h3><ol class="pub-list">`;
    for (const p of grouped[type]) {
      const award = p.award_note ? `<span class="pub-award">${esc(p.award_note)}</span>` : '';
      const lks = [
        p.pdf_url    && `<a href="${esc(p.pdf_url)}"    rel="noopener noreferrer">PDF</a>`,
        p.doi_url    && `<a href="${esc(p.doi_url)}"    rel="noopener noreferrer">DOI</a>`,
        p.slides_url && `<a href="${esc(p.slides_url)}" rel="noopener noreferrer">Slides</a>`
      ].filter(Boolean);
      const linksHtml = lks.length ? ` <span class="pub-links">[${lks.join('] [')}]</span>` : '';
      html += `<li><span class="pub-id">${esc(p.pub_id)}.</span><span class="pub-body">${p.citation}${award}${linksHtml}</span></li>`;
    }
    html += `</ol>`;
  }
  return mkSection(s, html);
}

function mkTeaching(s, items) {
  // Group by institution (preserving order of first occurrence)
  const grouped = new Map();
  const ungrouped = [];
  for (const t of items) {
    if (t.institution) {
      if (!grouped.has(t.institution)) grouped.set(t.institution, []);
      grouped.get(t.institution).push(t.label);
    } else {
      ungrouped.push(t.label);
    }
  }
  let html = '<div class="prose">';
  for (const [inst, labels] of grouped) {
    html += `<p><strong>${esc(inst)}</strong></p><ul>${labels.map(l => `<li>${esc(l)}</li>`).join('')}</ul>`;
  }
  if (ungrouped.length) {
    html += `<ul>${ungrouped.map(l => `<li>${esc(l)}</li>`).join('')}</ul>`;
  }
  return mkSection(s, html + '</div>');
}

function mkAwardsList(s, items) {
  const lis = items.map(a => `<li>${a.label}</li>`).join('');
  return mkSection(s, `<ul class="awards-list">${lis}</ul>`);
}

function mkService(s, items) {
  const grouped = new Map();
  for (const row of items) {
    if (!grouped.has(row.category)) grouped.set(row.category, []);
    grouped.get(row.category).push(row.label);
  }
  let html = '<div class="service-grid">';
  for (const [cat, labels] of grouped) {
    const lis = labels.map(l => `<li>${l}</li>`).join('');
    html += `<div><h3 class="subsection-title">${esc(cat)}</h3><ul>${lis}</ul></div>`;
  }
  return mkSection(s, html + '</div>');
}

function buildCustomPage(p) {
  return mkSection({ slug: p.slug, label: p.title }, `<div class="prose">${p.content}</div>`);
}

// ── Nav intersection observer ─────────────────────────────────────────────────
function initNavObserver() {
  const navLinks = document.querySelectorAll('.section-nav a');
  const navToggle = document.querySelector('.nav-toggle');
  const sectionNav = document.getElementById('section-nav');

  const sections = [];
  navLinks.forEach(link => {
    const id = link.getAttribute('href');
    if (id?.startsWith('#')) {
      const sec = document.querySelector(id);
      if (sec) sections.push({ id, el: sec, link });
    }
  });

  if ('IntersectionObserver' in window && sections.length) {
    const obs = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          navLinks.forEach(l => {
            const active = l.getAttribute('href') === '#' + entry.target.id;
            l.classList.toggle('is-active', active);
            active ? l.setAttribute('aria-current', 'location') : l.removeAttribute('aria-current');
          });
        }
      });
    }, { rootMargin: '-20% 0px -65% 0px', threshold: 0 });
    sections.forEach(s => obs.observe(s.el));
  }

  navLinks.forEach(link => {
    link.addEventListener('click', () => {
      if (window.matchMedia('(max-width:800px)').matches && sectionNav) {
        sectionNav.classList.remove('is-open');
        navToggle?.setAttribute('aria-expanded', 'false');
      }
    });
  });

  navToggle?.addEventListener('click', () => {
    const expanded = navToggle.getAttribute('aria-expanded') === 'true';
    navToggle.setAttribute('aria-expanded', String(!expanded));
    sectionNav?.classList.toggle('is-open', !expanded);
  });
}

// ── Boot ──────────────────────────────────────────────────────────────────────
if (!window.SUPABASE_URL || window.SUPABASE_URL.includes('YOUR_PROJECT')) {
  document.getElementById('page-loading').textContent =
    'Configure your Supabase credentials in config.js to load content.';
} else {
  loadPage().catch(err => {
    console.error(err);
    document.getElementById('page-loading').textContent = 'Failed to load content. Check console.';
  });
}
