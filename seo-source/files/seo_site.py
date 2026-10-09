"""Public SEO / AI-answer layer for www.divinebilling.online.

One source of truth for the brand facts that search engines and LLMs read:
canonical URLs, Organization / SoftwareApplication JSON-LD, robots.txt,
sitemap.xml, llms.txt and the /faq page. Prices always come from the live
pricing tiers so the site, structured data and llms.txt never disagree.
"""
import json
import os
import re
import sys
from datetime import datetime

from flask import Response, abort, redirect, render_template, request, url_for
from markupsafe import Markup

APEX_HOST = 'divinebilling.online'
BRAND = 'DivineBilling'
COMPANY = 'Divine Online Solutions'
CONTACT_EMAIL = 'info@divineonlinesolutions.com'
COMPANY_URL = 'https://www.divineonline.solutions/'
DEMO_URL = 'https://demo.divinebilling.online'
LOGIN_URL = 'https://login.divinebilling.online'

# Entity sentence repeated verbatim across schema, llms.txt, FAQ and footer.
# "DivineBilling" collides with US medical-billing firms; say what we are not.
ENTITY_SUMMARY = (
    'DivineBilling is cloud billing and business-management software for South African '
    'SMEs, built by Divine Online Solutions in Cape Town. It combines invoicing and books, '
    'a free contractor portal, multi-company accounting, SARS-ready payroll and industry '
    'departments such as PSIRA security, K9, POS, butcher, utility metering and farming. '
    'Data is hosted in South Africa and processing is POPIA-aligned.'
)
NOT_MEDICAL = (
    'DivineBilling is not a medical billing service and is not affiliated with US '
    'healthcare billing companies with similar names.'
)

# Public pages, in sitemap priority order. Solution slugs are appended from SOLUTIONS_NAV.
SITEMAP_PATHS = ['/', '/pricing', '/modules', '/faq', '/solutions', '/for-bookkeepers',
                 '/roadmap', '/get-started', '/become-a-reseller', '/privacy', '/terms']

# Search titles for /solutions pages (keep under ~45 chars; " · DivineBilling" is appended).
VERTICAL_TITLES = {
    'finance': 'Billing & multi-company books for SA',
    'hr': 'HR software for site-based SA teams',
    'payroll': 'SA payroll software with EMP201',
    'security': 'PSIRA security company software',
    'k9': 'K9 working-dog management software',
    'sales': 'CRM, e-sign & VAT billing for SA',
    'marketing': 'Marketing campaigns, leads & ROI',
    'pos': 'Multi-store POS for SA shops',
    'central': 'Multi-shop stock & ordering software',
    'butcher': 'Butchery software: costing & FEFO',
    'utility': 'Utility metering & prepaid billing',
    'farming': 'Chicken & egg farm software for SA',
    'students': 'Student records, fees & attendance',
    'voting': 'Voting OS: party canvassing software',
    'bookkeepers': 'Multi-client software for SA bookkeepers',
}

# Robots groups: named AI/search crawlers get the same rules as "*" (a bot that
# matches a named group ignores the "*" group, so the rules are repeated).
AI_CRAWLERS = ('GPTBot', 'OAI-SearchBot', 'ChatGPT-User', 'ClaudeBot', 'Claude-SearchBot',
               'Claude-User', 'PerplexityBot', 'Perplexity-User', 'Google-Extended',
               'Applebot-Extended', 'Bingbot', 'Googlebot')
ROBOTS_DISALLOW = ('/admin', '/client', '/customer/', '/dashboard', '/reports/',
                   '/select-company', '/get-started/signup', '/status.json', '/api/')


def site_url():
    # Read from the env, not app.py, so the static freeze can run without the app.
    return os.environ.get('BILLALL_MARKETING_URL', 'https://www.divinebilling.online').strip().rstrip('/')


def canonical_url(path=None):
    path = (request.path if path is None else path) or '/'
    path = path.rstrip('/') or '/'
    return site_url() + path


def _abs(path):
    return site_url() + path


def _sitemap_paths():
    from marketing_site import SOLUTIONS_NAV
    paths = list(SITEMAP_PATHS)
    for row in SOLUTIONS_NAV:
        if row['id'] != 'bookkeepers':
            paths.append('/solutions/' + row['slug'])
    return paths


def _build_date():
    loaded = sys.modules.get('app')
    if loaded is not None and getattr(loaded, 'APP_BUILD_DATE', None):
        return loaded.APP_BUILD_DATE
    try:
        text = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app.py'),
                    encoding='utf-8').read()
    except OSError:
        return None
    found = re.search(r'APP_BUILD_DATE\s*=\s*"([^"]+)"', text)
    return found.group(1) if found else None


def _lastmod():
    try:
        return datetime.strptime(_build_date(), '%d %b %Y').strftime('%Y-%m-%d')
    except (TypeError, ValueError):
        return None


def _zar(amount):
    from modules_data import format_zar
    return format_zar(amount)


def pricing_facts():
    """Live tier prices as plain facts (ex VAT)."""
    from modules_data import get_pricing_addons, get_pricing_tiers, tier_setup_display
    tiers = {t['id']: t for t in get_pricing_tiers()}
    addons = get_pricing_addons()
    extra_company = next((a['price'] for a in addons if a['name'] == 'Extra company'), 'R119')
    basic, std, pro = tiers.get('basic', {}), tiers.get('standard', {}), tiers.get('professional', {})
    std_monthly = std.get('monthly') or 0
    return {
        'basic': basic.get('monthly'),
        'basic_companies': basic.get('companies', 1),
        'basic_modules': basic.get('modules_pick'),
        'standard': std_monthly,
        'standard_intro': std.get('intro_monthly'),
        'standard_intro_months': std.get('intro_months'),
        'standard_companies': std.get('companies', 3),
        'standard_modules': std.get('modules_pick'),
        'standard_incl_vat': int(round(std_monthly * 1.15)),
        'professional': pro.get('monthly'),
        'professional_companies': pro.get('companies', 8),
        'setup': tier_setup_display(list(tiers.values())),
        'extra_company': extra_company,
    }


def brand_facts():
    """Short, quotable facts used on the homepage and in llms.txt."""
    from modules_data import module_catalog_stats
    p = pricing_facts()
    stats = module_catalog_stats()
    std_price = '{}/pm'.format(_zar(p['standard']))
    if p['standard_intro']:
        std_price = '{}/pm for {} months, then {}'.format(
            _zar(p['standard_intro']), p['standard_intro_months'], std_price)
    return [
        ('What it is', 'Cloud billing, books and business-management software for South African SMEs.'),
        ('Built by', '{}, Cape Town, South Africa.'.format(COMPANY)),
        ('Pricing (ex VAT)', 'Basic {}/pm (1 company) · Standard {} (3 companies) · Professional {}/pm '
                             '({} companies, all modules) · Enterprise quoted.'.format(
                                 _zar(p['basic']), std_price, _zar(p['professional']),
                                 p['professional_companies'])),
        ('Contractors', 'Unlimited contractor portal users, free on every plan — they never use a paid seat.'),
        ('Multi-company', 'Separate books per entity, a company switcher and group consolidation. '
                          'Extra companies {}/mo.'.format(p['extra_company'])),
        ('Modules', '{} live modules across {} departments: Finance, HR, Payroll (SARS EMP201), '
                    'Security (PSIRA), K9, Sales, Marketing, POS, Butcher, Utility, Farming, '
                    'Students and more.'.format(stats['live'], stats['departments'])),
        ('Hosting & privacy', 'Data hosted in South Africa, daily encrypted backups, POPIA-aligned processing.'),
        ('Try it', 'A live demo tenant opens in one click at demo.divinebilling.online — no sign-up.'),
        ('Not to be confused with', 'US medical or healthcare billing companies with similar names.'),
    ]


# ─── FAQ ─────────────────────────────────────────────────────────

def faq_groups():
    """FAQ content as (heading, [(question, answer_html)]). Divine prices are live."""
    p = pricing_facts()
    basic, std, pro = _zar(p['basic']), _zar(p['standard']), _zar(p['professional'])
    std_intro = ''
    if p['standard_intro']:
        std_intro = ' (intro {}/pm for the first {} months)'.format(
            _zar(p['standard_intro']), p['standard_intro_months'])
    pricing = url_for('public_pricing')
    modules = url_for('public_modules')
    sol = lambda slug: url_for('public_solutions_page', slug=slug)  # noqa: E731
    about = [
        ('What is DivineBilling?',
         '{} <a href="{}">Try the live demo</a> to see the real product.'.format(ENTITY_SUMMARY, DEMO_URL)),
        ('Is DivineBilling a medical billing company?',
         'No. {} DivineBilling is general business software for South African companies: invoicing, '
         'books, contractors, payroll and industry operations.'.format(NOT_MEDICAL)),
        ('Who makes DivineBilling?',
         'DivineBilling is built and operated by {}, a software company in Cape Town, South Africa. '
         'Divine Online Solutions runs its own billing, contractors and multi-company books on the '
         'same product. Contact: <a href="mailto:{e}">{e}</a>.'.format(COMPANY, e=CONTACT_EMAIL)),
        ('How much does DivineBilling cost?',
         'Basic is {}/pm for one company, Standard is {}/pm for three companies{}, Professional is '
         '{}/pm for {} companies with every live module, and Enterprise is quoted. Prices are ex VAT; '
         'annual billing gives 12 months for the price of 10. See <a href="{}">pricing</a>.'.format(
             basic, std, std_intro, pro, p['professional_companies'], pricing)),
        ('Do contractors pay for a seat?',
         'No. Contractors use the contractor portal free on every plan — unlimited users. They log '
         'timesheets, upload documents and submit invoices; you approve them from one queue. You pay '
         'only for office seats and companies.'),
        ('Where is my data hosted? Is it POPIA compliant?',
         'Data is hosted in South Africa with daily encrypted backups. Processing is aligned with the '
         'Protection of Personal Information Act (POPIA), and SA ID and passport numbers are masked '
         'by default. See the <a href="{}">privacy policy</a>.'.format(url_for('public_privacy'))),
        ('Can I run several companies in one login?',
         'Yes. Each company keeps separate books; you switch between them in seconds and can '
         'consolidate a group. Standard includes {} companies, Professional {}; extra companies are '
         '{}/mo.'.format(p['standard_companies'], p['professional_companies'], p['extra_company'])),
        ('Does it handle South African payroll and SARS EMP201?',
         'Yes. The <a href="{}">Payroll</a> department runs pay runs and payslips and totals PAYE, '
         'UIF and SDL for the monthly EMP201.'.format(sol('payroll'))),
        ('Is there software for PSIRA-registered security companies?',
         'Yes. The <a href="{}">Security</a> department covers post orders, a digital occurrence book, '
         'incidents, access control and rosters, linked to <a href="{}">HR</a> (PSIRA grades and '
         'expiry), <a href="{}">K9</a> and Payroll, with per-site invoicing.'.format(
             sol('security'), sol('hr'), sol('k9'))),
        ('Is DivineBilling suitable for bookkeepers and accountants?',
         'Yes. Bookkeepers manage many client companies from one login, and clients and contractors '
         'use their portals free. See <a href="{}">DivineBilling for bookkeepers</a>.'.format(
             url_for('public_for_bookkeepers'))),
        ('Can I try it before I pay?',
         'Yes. <a href="{}">The live demo</a> opens a seeded tenant in one click with no sign-up, and '
         'paid plans start with a free trial — no card required. All modules are listed on the '
         '<a href="{}">modules page</a>.'.format(DEMO_URL, modules)),
    ]
    compare = [
        ('Why DivineBilling instead of Xero?',
         '<a href="https://www.xero.com/za/" target="_blank" rel="noopener">Xero</a> is an excellent '
         'ledger. Its Starter plan was R450/mo incl VAT for one organisation (checked 20 August 2026), '
         'so three entities need three subscriptions (about R1&nbsp;350) before payroll and apps. '
         'DivineBilling Standard is {}/pm ex VAT (about R{} incl VAT) for three companies, with '
         'office seats, unlimited contractor users and industry modules included.'.format(
             std, p['standard_incl_vat'])),
        ('Why DivineBilling instead of Sage?',
         '<a href="https://www.sage.com/en-za/" target="_blank" rel="noopener">Sage Accounting</a> '
         'Start was from R240 incl VAT, with growth sold as extras — users R75, each extra company '
         'R410, inventory R415 (checked 20 August 2026). DivineBilling bundles POS, HR, payroll and '
         'industry departments in one product; an extra company or office seat is {}/mo.'.format(
             p['extra_company'])),
        ('Why DivineBilling instead of QuickBooks?',
         '<a href="https://quickbooks.intuit.com/za/" target="_blank" rel="noopener">QuickBooks</a> '
         'is a US product with a South African landing page; billing is often in USD and Simple Start '
         'covers one user. It has no PSIRA roster, prepaid metering or free field portal. '
         'DivineBilling bills in rand, hosts in South Africa and never charges a seat per contractor.'),
        ('Why DivineBilling instead of Wave?',
         '<a href="https://www.waveapps.com/" target="_blank" rel="noopener">Wave</a> is built for '
         'North American invoicing; Pro was US$19 per business and payroll is US/Canada only '
         '(checked 20 August 2026). It is not built around SARS, POPIA or rand billing.'),
        ('What do Xero, Sage and QuickBooks still do better?',
         'Xero and Sage have automated South African bank feeds and are what many accountants '
         'already use; DivineBilling imports bank CSV and PDF statements instead. If you run one '
         'trading entity with no field staff and your practice lives in Xero or Sage, stay there. '
         'DivineBilling fits when the operation — contractors, sites, tills, meters, flocks — is '
         'the hard part.'),
    ]
    return [('About DivineBilling', about), ('Compared with Xero, Sage, QuickBooks and Wave', compare)]


def _strip_tags(html):
    text = re.sub(r'<[^>]+>', '', html).replace('&nbsp;', ' ')
    return re.sub(r'\s+', ' ', text).strip()


# ─── JSON-LD ─────────────────────────────────────────────────────

def _ld(obj):
    """Serialise JSON-LD safely for a <script> tag."""
    return Markup('<script type="application/ld+json">{}</script>'.format(
        json.dumps(obj, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')))


def _same_as():
    extra = [u.strip() for u in os.environ.get('SEO_SAME_AS', '').split(',') if u.strip()]
    return [COMPANY_URL] + extra


def site_jsonld():
    """Organization + WebSite + SoftwareApplication graph for every marketing page."""
    base = site_url()
    org_id, app_id = base + '/#organization', base + '/#software'
    p = pricing_facts()
    offers = []
    for name, price in (('Basic', p['basic']), ('Standard', p['standard']),
                        ('Professional', p['professional'])):
        if price is not None:
            offers.append({
                '@type': 'Offer', 'name': name, 'price': str(price), 'priceCurrency': 'ZAR',
                'url': base + '/pricing',
                'priceSpecification': {
                    '@type': 'UnitPriceSpecification', 'price': str(price), 'priceCurrency': 'ZAR',
                    'unitCode': 'MON', 'valueAddedTaxIncluded': False,
                },
            })
    graph = [
        {
            '@type': 'Organization', '@id': org_id, 'name': COMPANY,
            'url': COMPANY_URL, 'email': CONTACT_EMAIL,
            'logo': base + '/static/img/divinebilling-logo-lockup.png',
            'address': {'@type': 'PostalAddress', 'addressLocality': 'Cape Town',
                        'addressRegion': 'Western Cape', 'addressCountry': 'ZA'},
            'areaServed': {'@type': 'Country', 'name': 'South Africa'},
            'brand': {'@type': 'Brand', 'name': BRAND},
            'sameAs': _same_as(),
            'contactPoint': {'@type': 'ContactPoint', 'contactType': 'sales',
                             'email': CONTACT_EMAIL, 'areaServed': 'ZA',
                             'availableLanguage': ['English', 'Afrikaans']},
        },
        {
            '@type': 'WebSite', '@id': base + '/#website', 'url': base + '/', 'name': BRAND,
            'inLanguage': 'en-ZA', 'publisher': {'@id': org_id},
        },
        {
            '@type': 'SoftwareApplication', '@id': app_id, 'name': BRAND,
            'alternateName': ['Divine Billing', 'DivineBilling by Divine Online Solutions'],
            'url': base + '/', 'applicationCategory': 'BusinessApplication',
            'applicationSubCategory': 'Billing and accounting software',
            'operatingSystem': 'Web browser',
            'description': ENTITY_SUMMARY,
            'disambiguatingDescription': NOT_MEDICAL,
            'publisher': {'@id': org_id}, 'provider': {'@id': org_id},
            'areaServed': {'@type': 'Country', 'name': 'South Africa'},
            'inLanguage': ['en-ZA', 'af-ZA'],
            'featureList': [
                'Invoicing, quotes and customer portal', 'Free unlimited contractor portal',
                'Multi-company books and group consolidation', 'Payroll with SARS EMP201 totals',
                'PSIRA security operations and K9 management', 'Multi-store POS',
                'Utility metering and prepaid billing', 'South African data hosting, POPIA-aligned',
            ],
            'offers': {
                '@type': 'AggregateOffer', 'priceCurrency': 'ZAR',
                'lowPrice': str(p['basic']) if p['basic'] is not None else None,
                'highPrice': str(p['professional']) if p['professional'] is not None else None,
                'offerCount': len(offers), 'offers': offers,
            },
        },
    ]
    return _ld({'@context': 'https://schema.org', '@graph': graph})


def breadcrumb_jsonld(*crumbs):
    """crumbs: (name, path) pairs after Home."""
    items = [('Home', '/')] + list(crumbs)
    return _ld({
        '@context': 'https://schema.org', '@type': 'BreadcrumbList',
        'itemListElement': [
            {'@type': 'ListItem', 'position': i, 'name': n, 'item': canonical_url(path)}
            for i, (n, path) in enumerate(items, 1)
        ],
    })


def faq_jsonld(groups):
    return _ld({
        '@context': 'https://schema.org', '@type': 'FAQPage',
        'mainEntity': [
            {'@type': 'Question', 'name': q,
             'acceptedAnswer': {'@type': 'Answer', 'text': _strip_tags(a)}}
            for _, items in groups for q, a in items
        ],
    })


def guide_jsonld(guide):
    url = canonical_url('/guides/' + guide['slug'])
    org = {'@id': site_url() + '/#organization'}
    article = {
        '@context': 'https://schema.org', '@type': 'Article',
        'headline': guide['title'], 'description': guide['meta'],
        'datePublished': guide['published'], 'dateModified': guide['reviewed'],
        'author': {'@type': 'Organization', 'name': COMPANY, 'url': COMPANY_URL},
        'publisher': org, 'mainEntityOfPage': url, 'inLanguage': 'en-ZA',
        'about': {'@type': 'Country', 'name': 'South Africa'},
        'citation': [u for _, u in guide['sources']],
    }
    return Markup(_ld(article) + faq_jsonld([('', guide['faqs'])]) + breadcrumb_jsonld(
        ('Guides', '/guides'), (guide['title'], '/guides/' + guide['slug'])))


def render_guides_index(page_ctx):
    from guides_content import GUIDES
    return render_template('guides_index.html', **page_ctx(active_page='guides', guides=GUIDES))


def render_guide(page_ctx, slug):
    from guides_content import GUIDES, GUIDES_BY_SLUG
    guide = GUIDES_BY_SLUG[slug]
    related = [g for g in GUIDES if g['slug'] != slug]
    return render_template('guide_public.html', **page_ctx(
        active_page='guides', guide=guide, related=related, guide_ld=guide_jsonld(guide)))


# ─── robots / sitemap / llms.txt ─────────────────────────────────

def robots_body():
    rules = ['Allow: /'] + ['Disallow: {}'.format(p) for p in ROBOTS_DISALLOW]
    lines = ['# DivineBilling — South African billing software (not medical billing).',
             '# AI and search crawlers are welcome on public pages. See /llms.txt.', '']
    lines += ['User-agent: {}'.format(ua) for ua in AI_CRAWLERS] + rules + ['']
    lines += ['User-agent: *'] + rules + ['']
    lines.append('Sitemap: {}/sitemap.xml'.format(site_url()))
    return '\n'.join(lines) + '\n'


def sitemap_body():
    from guides_content import GUIDES
    lastmod = _lastmod()
    entries = [(p, lastmod) for p in _sitemap_paths()]
    entries.append(('/guides', max(g['reviewed'] for g in GUIDES)))
    entries += [('/guides/' + g['slug'], g['reviewed']) for g in GUIDES]
    rows = []
    for path, mod in entries:
        row = '  <url><loc>{}</loc>'.format(canonical_url(path))
        if mod:
            row += '<lastmod>{}</lastmod>'.format(mod)
        rows.append(row + '</url>')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + '\n'.join(rows) + '\n</urlset>\n')


def llms_body():
    """llms.txt (llmstxt.org): a plain-markdown brief for AI assistants."""
    from marketing_site import SOLUTIONS_NAV
    out = ['# DivineBilling', '', '> ' + ENTITY_SUMMARY + ' ' + NOT_MEDICAL, '']
    out += ['## Key facts', '']
    out += ['- **{}:** {}'.format(k, v) for k, v in brand_facts()]
    out += ['', '## Main pages', '',
            '- [Home]({}/): overview, plan builder and contact form'.format(site_url()),
            '- [Pricing]({}): tiers, add-ons and plan comparison (ZAR, ex VAT)'.format(_abs('/pricing')),
            '- [Modules]({}): every live module by department, plus the roadmap'.format(_abs('/modules')),
            '- [FAQ]({}): straight answers and comparison with Xero, Sage, QuickBooks and Wave'.format(_abs('/faq')),
            '- [Live demo]({}): a seeded demo tenant, no sign-up'.format(DEMO_URL),
            '', '## Departments', '']
    for row in SOLUTIONS_NAV:
        path = '/for-bookkeepers' if row['id'] == 'bookkeepers' else '/solutions/' + row['slug']
        out.append('- [{}]({}): {}'.format(row['label'], _abs(path), row['summary']))
    from guides_content import GUIDES
    out += ['', '## Guides for South African businesses', '']
    for g in GUIDES:
        out.append('- [{}]({}): {} (reviewed {})'.format(
            g['title'], _abs('/guides/' + g['slug']), g['summary'], g['reviewed']))
    out += ['', '## Questions and answers', '']
    for _, items in faq_groups():
        for q, a in items:
            out += ['### ' + q, '', _strip_tags(a), '']
    out += ['## Company', '',
            '- Divine Online Solutions, Cape Town, South Africa — {}'.format(COMPANY_URL),
            '- Contact: {}'.format(CONTACT_EMAIL),
            '- [Privacy policy]({})'.format(_abs('/privacy')),
            '- [Terms of use]({})'.format(_abs('/terms')), '']
    return '\n'.join(out)


# ─── Registration ────────────────────────────────────────────────

def vertical_title(page):
    return VERTICAL_TITLES.get(page.get('active_page'), page.get('title'))


def register_template_globals(app):
    app.add_template_global(vertical_title, 'seo_vertical_title')
    app.add_template_global(brand_facts, 'seo_brand_facts')
    app.add_template_global(canonical_url, 'seo_canonical')
    app.add_template_global(site_jsonld, 'seo_site_jsonld')
    app.add_template_global(breadcrumb_jsonld, 'seo_breadcrumb_jsonld')
    app.add_template_global(site_url, 'seo_site_url')


def render_faq(page_ctx):
    """page_ctx: the caller's marketing context builder (live app or static freeze)."""
    groups = faq_groups()
    return render_template(
        'faq_public.html',
        **page_ctx(active_page='faq', faq_groups=groups, faq_ld=faq_jsonld(groups)),
    )


def register_seo(app):
    register_template_globals(app)

    @app.before_request
    def _apex_to_www():
        """Fold divinebilling.online onto www so search engines see one host."""
        host = (request.host or '').split(':')[0].lower()
        if host != APEX_HOST or request.method not in ('GET', 'HEAD'):
            return None
        return redirect(site_url() + request.full_path.rstrip('?'), 301)

    @app.route('/llms.txt')
    def llms_txt():
        resp = Response(llms_body(), mimetype='text/markdown')
        resp.headers['Cache-Control'] = 'public, max-age=3600'
        return resp

    def _marketing_only():
        from app import is_login_only_host
        if is_login_only_host():
            return redirect(site_url() + request.path, 301)
        from demo_mode import is_demo_site
        if is_demo_site():
            return redirect(url_for('home'))
        return None

    @app.route('/guides')
    def public_guides():
        bounced = _marketing_only()
        if bounced:
            return bounced
        from marketing_site import _page_ctx
        return render_guides_index(_page_ctx)

    @app.route('/guides/<slug>')
    def public_guide(slug):
        from guides_content import GUIDES_BY_SLUG
        bounced = _marketing_only()
        if bounced:
            return bounced
        if slug not in GUIDES_BY_SLUG:
            abort(404)
        from marketing_site import _page_ctx
        return render_guide(_page_ctx, slug)

    @app.route('/faq')
    def public_faq():
        bounced = _marketing_only()
        if bounced:
            return bounced
        from marketing_site import _page_ctx
        return render_faq(_page_ctx)
