"""Fallback content when Supabase rows are empty."""

PROFILE = {
    'full_name': 'Your Name',
    'name_alt': '（姓名）',
    'title': 'Assistant Professor',
    'department_1': 'Department of Electrical and Computer Engineering',
    'department_2': 'Department of Computer Science (Courtesy)',
    'university': 'North Carolina State University',
    'address': '890 Oval Dr, Raleigh, NC 27695',
    'office': '3072 Engr Bldg II',
    'phone': '(919) 515-5128',
    'email': 'you@university.edu',
    'photo_url': '',
    'biography': (
        'I am an Assistant Professor in the Department of Electrical and Computer Engineering '
        'at North Carolina State University, where I direct the Intelligent Wireless Networking '
        '(iWN) Laboratory. My work addresses software-defined wireless systems, intelligent edge '
        'computing, and learning-driven network resource management, with applications in beyond-5G '
        'networks, Internet of Things deployments, and cyber-physical systems.\n\n'
        'Previously, I held postdoctoral and research appointments at institutions in the United '
        'States. I received the Ph.D. degree in Electrical and Computer Engineering from the '
        'Georgia Institute of Technology, and the B.S. and M.S. degrees in Electrical Engineering '
        'from the National Taiwan University.'
    ),
    'scholar_url': 'https://scholar.google.com/',
    'linkedin_url': 'https://www.linkedin.com/',
    'github_url': 'https://github.com/',
    'orcid_url': 'https://orcid.org/',
    'cv_url': '',
    'cv_filename': '',
    'researchgate_url': 'https://www.researchgate.net/',
    'students_text': (
        'I am recruiting self-motivated Ph.D. students in wireless communications and networking. '
        'Current openings emphasize 6G radio and intelligent networking, vehicular edge computing, '
        'wireless federated learning, and hardware/software co-design. A solid mathematical background '
        'is expected; prior experience in wireless communications, computer networks, or '
        'electromagnetics is welcome.\n\n'
        'To inquire, send your CV and transcripts by email.'
    ),
    'students_email': 'lab@university.edu',
}

NEWS = [
    {'event_date': '2025-06-01', 'body': 'Paper on federated learning for multi-mission UAV operations accepted for presentation at AFRL Summer VFRP.'},
    {'event_date': '2025-03-01', 'body': 'Two papers accepted at IEEE INFOCOM 2025.'},
    {'event_date': '2024-11-01', 'body': 'Runner-up, AFRL Software Defined Radio Challenge, for distributed multimedia transmission.'},
    {'event_date': '2024-07-01', 'body': 'Journal article on O-RAN resource management published in <em>IEEE Transactions on Mobile Computing</em>.'},
    {'event_date': '2024-05-01', 'body': 'Received Faculty Research Grant from NASA North Carolina Space Grant for 6G serverless computing architecture.'},
]

RESEARCH = [
    'Wireless software-defined networking and open RAN architectures',
    'Intelligent edge computing and network slicing',
    'Federated and distributed machine learning over wireless links',
    'Resource management for vehicular and UAV communication systems',
    'Underground and underwater wireless communications',
    'Security and reliability in IoT and cyber-physical systems',
]

EDUCATION = [
    {'degree': 'Ph.D., Electrical and Computer Engineering', 'institution': 'Georgia Institute of Technology, Atlanta, GA'},
    {'degree': 'M.S., Communications Engineering', 'institution': 'National Taiwan University, Taipei, Taiwan'},
    {'degree': 'B.S., Electrical Engineering', 'institution': 'National Taiwan University, Taipei, Taiwan'},
]

PUBLICATIONS_JOURNAL = [
    {'pub_id': 'J5', 'citation': '<strong>Your Name</strong>, A. Collaborator, and B. Collaborator, &ldquo;DRL-ORAN Platform for Large-Scale Networking Resource Management,&rdquo; <em>IEEE Transactions on Mobile Computing</em>, vol. 23, no. 8, pp. 7421&ndash;7436, 2024.', 'pdf_url': '#', 'doi_url': '#', 'award_note': ''},
    {'pub_id': 'J4', 'citation': 'C. Collaborator, <strong>Your Name</strong>, and D. Collaborator, &ldquo;QoS-Aware Adaptive Routing in Multi-Layer Hierarchical SDNs: A Reinforcement Learning Approach,&rdquo; <em>IEEE Transactions on Network and Service Management</em>, 2020.', 'pdf_url': '#', 'award_note': ''},
    {'pub_id': 'J3', 'citation': '<strong>Your Name</strong> and E. Collaborator, &ldquo;Application-Defined Networks for AI Systems at the Edge,&rdquo; <em>ACM Transactions on Sensor Networks</em>, 2019.', 'pdf_url': '#', 'award_note': ''},
]

PUBLICATIONS_CONFERENCE = [
    {'pub_id': 'C8', 'citation': '<strong>Your Name</strong>, F. Collaborator, and G. Collaborator, &ldquo;Federated Learning over Open RAN: Architecture and Prototype,&rdquo; in <em>Proc. IEEE INFOCOM</em>, 2025.', 'pdf_url': '#', 'slides_url': '#', 'award_note': ''},
    {'pub_id': 'C7', 'citation': 'H. Collaborator and <strong>Your Name</strong>, &ldquo;Signal Interference Management in O-RAN xAPP Design,&rdquo; in <em>Proc. IEEE ICC</em>, 2021.', 'pdf_url': '#', 'award_note': ''},
    {'pub_id': 'C6', 'citation': '<strong>Your Name</strong>, I. Collaborator, and J. Collaborator, &ldquo;Home Network Intelligent Scheduling Control,&rdquo; in <em>Proc. IEEE GLOBECOM</em>, 2021.', 'pdf_url': '#', 'award_note': 'Best Paper Award Runner-up'},
]

PUBLICATIONS_WORKSHOP = [
    {'pub_id': 'W1', 'citation': '<strong>Your Name</strong> and K. Collaborator, &ldquo;Demo: A Prototype Platform for 5G Edge Analytics,&rdquo; in <em>Proc. ACM MobiCom Demo</em>, 2022.', 'pdf_url': '#', 'award_note': ''},
]

TEACHING = [
    'ECE 566 — Wireless Networking and Mobile Computing (Fall 2024, Spring 2025)',
    'ECE 792 — Special Topics: Open RAN and Network Softwarization (Spring 2024)',
    'ECE 302 — Introduction to Communication Systems (Fall 2023)',
]

AWARDS = [
    '<strong>Awardee</strong>, Summer Visiting Faculty Research Program (VFRP), Air Force Research Laboratory, 2025.',
    '<strong>Runner-up</strong>, Software Defined Radio Challenge, AFRL, 2024.',
    '<strong>AI4AI Research Award</strong>, Meta, 2022.',
    '<strong>Faculty Research Grant</strong>, NASA North Carolina Space Grant, 2022.',
    '<strong>Distinguished TPC Member Award</strong>, IEEE INFOCOM, 2020.',
    '<strong>Researcher of the Year</strong>, Broadband Wireless Networking Laboratory, Georgia Institute of Technology, 2015.',
]

SERVICE = {
    'Technical Program Committees': [
        'IEEE INFOCOM (2020&ndash;present; Distinguished TPC Member, 2020)',
        'IEEE ICC, IEEE GLOBECOM, ACM MobiCom',
    ],
    'Journal Reviewing': [
        '<em>IEEE/ACM Transactions on Networking</em>',
        '<em>IEEE Transactions on Mobile Computing</em>',
        '<em>IEEE Transactions on Wireless Communications</em>',
    ],
}

SECTIONS = [
    {'id': 'biography', 'label': 'Biography', 'url_name': 'biography'},
    {'id': 'news', 'label': 'News', 'url_name': 'news'},
    {'id': 'research', 'label': 'Research', 'url_name': 'research'},
    {'id': 'education', 'label': 'Education', 'url_name': 'education'},
    {'id': 'publications', 'label': 'Publications', 'url_name': 'publications'},
    {'id': 'teaching', 'label': 'Teaching', 'url_name': 'teaching'},
    {'id': 'awards', 'label': 'Honors & Awards', 'url_name': 'awards'},
    {'id': 'service', 'label': 'Service', 'url_name': 'service'},
]
