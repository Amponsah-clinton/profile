"""Fallback content when Supabase rows are empty."""

PROFILE = {
    'full_name': 'Amponsah Clinton',
    'name_alt': '',
    'title': 'MPhil Candidate, Computer Engineering',
    'department_1': 'Department of Computer & Electrical Engineering',
    'department_2': '',
    'university': 'University of Energy and Natural Resources',
    'address': 'Sunyani, Ghana',
    'office': '',
    'phone': '0556105897',
    'email': 'clinton.amponsah001@gmail.com',
    'photo_url': '',
    'biography': (
        'I am a research-oriented Computer Engineer with interests in computer networking, '
        'artificial intelligence, and privacy. I am currently pursuing an MPhil in Computer '
        'Engineering at the University of Energy and Natural Resources (UENR), Sunyani, where my '
        'work contributes to research in secure communication systems and intelligent technologies.\n\n'
        'Alongside my graduate studies, I work as a Researcher and Software Developer at Metascholar '
        'Consult Limited, building scalable software systems and conducting research in AI, digital '
        'systems, and secure computing. I previously served as a Teaching and Research Assistant in '
        'the IoT & DataCom Lab at UENR. I am experienced in academic writing, scholarly collaboration, '
        'undergraduate instruction, and software development, and I am passionate about developing '
        'efficient, intelligent, and privacy-aware computing systems through research and innovation.'
    ),
    'scholar_url': '',
    'linkedin_url': '',
    'github_url': 'https://github.com/Amponsah-clinton',
    'orcid_url': 'https://orcid.org/0009-0006-8414-9794',
    'cv_url': '',
    'cv_filename': '',
    'researchgate_url': '',
    'students_text': '',
    'students_email': '',
}

NEWS = [
    {'event_date': '2026-02-01', 'body': 'Serving as a reviewer for the <em>Journal of Electrical Systems and Information Technology</em> (Springer Nature).'},
    {'event_date': '2026-01-01', 'body': 'Began the M.Phil. in Computer Engineering at the University of Energy and Natural Resources.'},
    {'event_date': '2025-12-01', 'body': 'Co-authored &ldquo;Examining the Role of AI-Based Learning Tools in Higher Education&rdquo; in <em>SAP Social AI</em>. <a href="https://doi.org/10.62486/sai202529" rel="noopener noreferrer">https://doi.org/10.62486/sai202529</a>'},
    {'event_date': '2025-11-01', 'body': 'Two papers accepted for publication in the <em>South Asian Journal of AI</em>.'},
    {'event_date': '2025-10-01', 'body': 'Joined Metascholar Consult Limited as a Researcher &amp; Software Developer.'},
]

RESEARCH = [
    'Computer networking and secure communication systems',
    'Artificial intelligence and intelligent systems',
    'Privacy and privacy-aware computing',
    'Lightweight cryptography for secure IoT data transmission',
    'AI ethics, security, fairness, and bias mitigation',
    'Network attacks, vulnerabilities, and secure system design',
]

EDUCATION = [
    {'degree': 'M.Phil. in Computer Engineering, 2026–Present', 'institution': 'University of Energy and Natural Resources, Sunyani, Ghana'},
    {'degree': 'B.Sc. in Computer Engineering, 2019–2023', 'institution': 'University of Energy and Natural Resources, Sunyani, Ghana'},
    {'degree': 'WASSCE, 2013–2016', 'institution': 'Konongo Odumase Senior High School, Konongo, Ghana'},
]

PUBLICATIONS_JOURNAL = [
    {
        'pub_id': 'J1',
        'citation': (
            'A. Atianashie M., M. K. Kuffour, B. Kyiewu, and <strong>C. Amponsah</strong>, '
            '&ldquo;Examining the Role of AI-Based Learning Tools in Higher Education: A Critical Synthesis '
            'of Effects on Student Performance and Engagement,&rdquo; <em>SAP Social AI</em>, 2025. '
            '<a href="https://doi.org/10.62486/sai202529" rel="noopener noreferrer">https://doi.org/10.62486/sai202529</a>'
        ),
        'pdf_url': '', 'doi_url': '', 'award_note': '', 'year': 2025,
    },
    {
        'pub_id': 'J2',
        'citation': (
            '<strong>C. Amponsah</strong>, &ldquo;Who Bears the Cost of Fairness? Empirical Evidence from a '
            'Cross-Regional Bias Detection and Mitigation Pipeline in Machine Learning,&rdquo; '
            '<em>South Asian Journal of AI</em>.'
        ),
        'pdf_url': '', 'doi_url': '', 'award_note': 'Accepted / In Press', 'year': 2026,
    },
    {
        'pub_id': 'J3',
        'citation': (
            '<strong>C. Amponsah</strong>, &ldquo;Invisible Algorithms, Visible Inequality: Uncovering the '
            'Social Consequences of AI-Driven Decision Systems,&rdquo; <em>South Asian Journal of AI</em>.'
        ),
        'pdf_url': '', 'doi_url': '', 'award_note': 'Accepted / In Press', 'year': 2026,
    },
]

PUBLICATIONS_CONFERENCE = []

PUBLICATIONS_WORKSHOP = []

TEACHING = [
    'Computer Literacy (CENG 101)',
    'Information Theory (CENG 201)',
    'Secure Network Systems (CENG 413)',
]

# Repurposed as "Certifications" (see seed_content / site_pages rename).
AWARDS = [
    '<strong>Huawei Routing &amp; Switching Associate</strong> &mdash; Huawei',
    '<strong>Understanding Research Methods</strong> &mdash; University of London. <a href="https://coursera.org/share/b127257498ae8cdd9d7fea30ea4d22f1" rel="noopener noreferrer">View certificate</a>',
    '<strong>Foundations of UX Design</strong> &mdash; Google. <a href="https://coursera.org/share/5c61189e35553b4aacd075c9d2798098" rel="noopener noreferrer">View certificate</a>',
    '<strong>Data, Security, and Privacy</strong> &mdash; University of California, Irvine. <a href="https://coursera.org/share/bac9fe877747022cb54941aa0a451dde" rel="noopener noreferrer">View certificate</a>',
    '<strong>Django Web Framework</strong> &mdash; Meta. <a href="https://coursera.org/share/e0bd8ffeb766fa196f1f4ce6a8d5ccff" rel="noopener noreferrer">View certificate</a>',
    '<strong>Programming for Everybody</strong> &mdash; University of Michigan. <a href="https://coursera.org/share/03d2db62a37ec9dc443c891874728752" rel="noopener noreferrer">View certificate</a>',
]

SERVICE = {
    'Peer Review': [
        'Reviewer, <em>Journal of Electrical Systems and Information Technology</em>, Springer Nature (2026)',
    ],
    'Community Engagement': [
        'Co-Founder, <strong>Veritas Foundation</strong>, Kumasi (2021&ndash;Present) &mdash; educational support and mentorship for underprivileged students.',
    ],
}

# Custom-page content (rendered as escaped plain-text paragraphs; blank line = new paragraph).
EXPERIENCE_CONTENT = (
    '<strong>Researcher &amp; Software Developer</strong> — Metascholar Consult Limited, Sunyani, Ghana (Oct 2025 – Present). '
    'Conducting academic and industry-oriented research in artificial intelligence, digital systems, and '
    'secure computing; designing and developing scalable software systems and web platforms; supporting '
    'literature reviews, technical writing, data analysis, and the preparation of manuscripts and research '
    'proposals; and building backends, database integrations, and APIs using Python, Django, and JavaScript.\n\n'
    '<strong>Teaching &amp; Research Assistant, IoT &amp; DataCom Lab (National Service)</strong> — University of Energy and Natural '
    'Resources, Sunyani, Ghana (May 2023 – Sep 2025). Assisted in teaching undergraduate courses including '
    'Computer Literacy (CENG 101), Information Theory (CENG 201), and Secure Network Systems (CENG 413); '
    'facilitated tutorials, laboratory sessions, and assignments; and supported faculty research, data '
    'analysis, and technical documentation.\n\n'
    '<strong>Researcher (Internship)</strong> — HackScience Technologies, Accra, Ghana (Aug 2022 – Dec 2023). Researched the '
    'ethical and security implications of AI systems; investigated AI-related network attacks, vulnerabilities, '
    'and secure system practices; and contributed to software innovation and collaborative research projects.\n\n'
    '<strong>Engineering Laboratory Assistant</strong> — IoT &amp; DataCom Lab, University of Energy and Natural Resources, Sunyani, '
    'Ghana (Feb 2022 – Jul 2023). Supported practical engineering laboratory sessions, configured networking '
    'devices, troubleshot technical issues, and maintained laboratory equipment.'
)

PROJECTS_CONTENT = (
    '<strong>Swarm Robots in Environmental Monitoring</strong> — RVIS Lab, UENR (2023). Participated in the design and '
    'evaluation of intelligent robotic systems for environmental data collection and monitoring.\n\n'
    '<strong>AI-Based Web Platform for Job Listing in Ghana</strong> (2023). Developed an intelligent web platform to support '
    'employment opportunities and digital recruitment services in Ghana.\n\n'
    '<strong>Lightweight Cryptography for Secure IoT Data Transmission</strong> — IoT &amp; DataCom Lab, UENR (2022). Research '
    'focused on efficient cryptographic mechanisms for secure, low-resource IoT environments.'
)

SECTIONS = [
    {'id': 'biography', 'label': 'Biography', 'url_name': 'biography'},
    {'id': 'news', 'label': 'News', 'url_name': 'news'},
    {'id': 'research', 'label': 'Research', 'url_name': 'research'},
    {'id': 'education', 'label': 'Education', 'url_name': 'education'},
    {'id': 'publications', 'label': 'Publications', 'url_name': 'publications'},
    {'id': 'teaching', 'label': 'Teaching', 'url_name': 'teaching'},
    {'id': 'awards', 'label': 'Certifications', 'url_name': 'awards'},
    {'id': 'service', 'label': 'Service', 'url_name': 'service'},
]
